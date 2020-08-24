from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from app.models import *
from app.serializers import *
from app.scraper import IMDBScraper
from django.db import IntegrityError


class UpdateAdminOnly(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        method = request.method
        if method in SAFE_METHODS:
            return True
        else:
            if user.is_staff:
                return True
            else:
                return False


class UserViewSet(viewsets.ModelViewSet):
    """
    This API endpoint will allows the user to sign up for the app.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    http_method_names = ('post', 'head', 'options')

    def create(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        if serializer.is_valid():
            validatedData = serializer.validated_data
            userInstance = User.objects.create_user(**validatedData)
            userInstance.save()
            return Response(UserSerializer(userInstance).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskViewSet(viewsets.ModelViewSet):
    """
    This API endpoint will allow the staff users to populate \
    the Movie & Cast table by scraping the movies from the \
    given 'url' in request payload.
    """
    queryset = Task.objects.all().order_by('-createdDate')
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated & IsAdminUser,)
    http_method_names = ('get', 'post', 'head', 'options')

    def create(self, request, *args, **kwargs):
        task = request.data
        taskSerializer = TaskSerializer(data=task)
        if taskSerializer.is_valid():
            # Create task
            validatedData = taskSerializer.validated_data
            taskInstance = Task.objects.create(
                **validatedData, author=request.user)
            taskInstance.save()
            # Scrape movies
            imdbUrl = validatedData.get('imdbUrl')
            scraper = IMDBScraper(imdbUrl)
            movies = scraper.start()
            # Populate Movie table
            moviesInserted = 0
            for movie in movies:
                movie['taskId'] = taskInstance.id
                movieSerializer = MovieSerializer(data=movie)
                if movieSerializer.is_valid():
                    validatedData = movieSerializer.validated_data
                    movieInstance = Movie.objects.create(**validatedData)
                    movieInstance.save()
                    moviesInserted += 1
                    # Populate Cast table
                    stars = movie['stars']
                    for star in stars:
                        cast = {}
                        cast['movieId'] = movieInstance.id
                        cast['star'] = star
                        castSerializer = CastSerializer(data=cast)
                        if castSerializer.is_valid():
                            validatedData = castSerializer.validated_data
                            castInstance = Cast.objects.create(**validatedData)
                            castInstance.save()
                        else:
                            print(castSerializer.errors)
                else:
                    print(movieSerializer.errors)
            # Update task
            taskInstance.movieCount = moviesInserted
            taskInstance.save()
            return Response(TaskSerializer(taskInstance).data, status=status.HTTP_201_CREATED)
        else:
            return Response(taskSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieViewSet(viewsets.ModelViewSet):
    """
    This API endpoint will allow staff users to update the movies\
    and non staff users to list the movies.
    """

    queryset = Movie.objects.all().order_by('-rating')
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticated & UpdateAdminOnly,)
    http_method_names = ('get', 'put', 'head', 'options')


class CastViewSet(viewsets.ModelViewSet):

    queryset = Cast.objects.all()
    serializer_class = CastSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ('get', 'head', 'options')


class ActivityViewSet(viewsets.ModelViewSet):
    """
    This API endpoint allows the users to add and delete a specfic \
    movie to and from 'WATCH' or 'WATCHED' list respectively.
    """

    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ('get', 'post', 'delete', 'head', 'options')

    def create(self, request, *args, **kwargs):
        activity = request.data
        user = request.user
        serializer = ActivitySerializer(data=activity)
        if serializer.is_valid():
            validatedData = serializer.validated_data
            try:
                activityInstance = Activity.objects.create(
                    **validatedData, username=user)
                activityInstance.save()
                return Response(ActivitySerializer(activityInstance).data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                movieId = validatedData.get('movieId', None)
                newAction = validatedData.get('action', None)
                activityInstance = Activity.objects.get(
                    username=user, movieId=movieId)
                if activityInstance.action != newAction:
                    activityInstance.action = newAction
                    activityInstance.save()
                return Response(ActivitySerializer(activityInstance).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
