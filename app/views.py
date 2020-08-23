from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from app.models import *
from app.serializers import *
from app.scraper import IMDBScraper


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class TaskViewSet(viewsets.ModelViewSet):
    """
    Populates the Movie, Cast table by scraping the movies from the given 'url' in request payload.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        task = request.data
        taskSerializer = TaskSerializer(data=task)
        if taskSerializer.is_valid():
            # Create task
            validatedData = taskSerializer.validated_data
            taskInstance = Task.objects.create(**validatedData)
            taskInstance.save()
            # Scrape movies
            url = validatedData.get('url')
            scraper = IMDBScraper(url)
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

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    http_method_names = ['get','head']