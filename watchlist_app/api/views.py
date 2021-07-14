#--------------------------------------HEADER START-----------------------------------------------#
from django.shortcuts import get_object_or_404
from rest_framework.response import Response # for returning responses
from rest_framework.exceptions import ValidationError # for returning Validation error response
from rest_framework import status # for giving status codes in responses
# from rest_framework.decorators import api_view
from rest_framework.views import APIView # for views using API view
from rest_framework import generics # for generic views
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly #permission classes.
# from rest_framework import mixins -- For views when mixins used
#------------------------------------------------------------------------------------------------#
#Importing Models and Serializers
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer

#Custom Permissions
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly

#-----------------------------------HEADER ENDS------------------------------------------------------------------#

#-----------------------------Views Using generic Views-------------------------------------#
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('id')
        watchlist = WatchList.objects.get(pk=pk)
        current_author = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, author=current_author)
        if review_queryset.exists():
            raise ValidationError("Your Review Already Exists")

        if watchlist.number_ratings == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2
        
        watchlist.number_ratings = watchlist.number_ratings + 1
        watchlist.save()
        serializer.save(watchlist=watchlist, author=current_author)

# When we have our id in different position in url as of normal conditions (usually in the last) 
# we have to manually find our pk(id) in the url with pk = self.kwargs['id'] it finds our id in keyword arguments.

class ReviewList(generics.ListCreateAPIView):
    # queryset = Review.objects.all()
    def get_queryset(self):
        pk = self.kwargs['id']
        return Review.objects.filter(watchlist=pk)
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    # we dont need permission classes in this because this class is read only already
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly]
    lookup_field = ('id')

# this lookup field attribute is used when we use another name for our primary key instead 
# of pk like id roll etc. then we have to pass lookup field which takes our another name 
# for primary key and then change that name to pk at runtime in the urls.



#----------------Views Using Mixins -------------------------------------------------------#
# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     lookup_field = ('id')

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request,*args, **kwargs):
#         return self.create(request, *args, **kwargs)

#--------------------Views using API view--------------------------------------------------#

# In API view we have to manually write get post functions and validate data 
# in each post response. In class based views you can create get post put delete methods
# instead of checking the request.method 


class WatchListAV(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        watchlist = WatchList.objects.all()
        serializer = WatchListSerializer(watchlist, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data) #passing request data into the serializer

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WatchDetailAV(APIView):

    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, id):
        try:
            watchlist = WatchList.objects.get(pk=id)
        except WatchList.DoesNotExist:
            return Response({'error': 'Content not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(watchlist)
        return Response(serializer.data)

    def put(self, request, id):
        watchlist = WatchList.objects.get(pk=id)
        serializer = WatchListSerializer(watchlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        watchlist = WatchList.objects.get(pk=id)
        watchlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#-----------------------------------Using Viewsets------------------------------------------#
# In normal viewset we have to create list retrieve create all functions manually
# for each task i.e., LIST DETAIL CREATE


# class StreamPlatformVS(viewsets.ViewSet):

#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         platform = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(platform)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#---------------------------------Using Model Viewset---------------------------------------#
# In case of ModelViewSet all functions are already built in for list detail and create 
# just have to pass queryset and serializer_class and lookup field or order_by if you
# use custom primary key name

class StreamPlatformVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = StreamPlatform.objects.all().order_by('id')
    serializer_class = StreamPlatformSerializer
    # lookup_field = 'id'
    # .order_by('id') -- does the same work as lookup_field it also passes our custom 
    # pk to drf to lookup


#--------------------------------API View Continuation-----------------------------------------#
'''In normal Api view classes you have to create every method manually for 
get post put create and also different list and detail av classes'''

# class StreamPlatformAV(APIView):

#     def get(self, request):
#         platforms = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(
#             platforms, many=True)
#         # serializer = StreamPlatformSerializer(platforms, many=True, context={'request': request})
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
        
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class StreamPlatformDetailAV(APIView):

#     def get(self, request, id):
#         try:
#             platform = StreamPlatform.objects.get(pk=id)
#         except StreamPlatform.DoesNotExist:
#             return Response({'error': 'Platform not found'}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = StreamPlatformSerializer(platform)
#         return Response(serializer.data)

#     def put(self, request, id):
#         platform = StreamPlatform.objects.get(pk=id)
#         serializer = StreamPlatformSerializer(platform, data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     def delete(self, request, id):
#         platform = StreamPlatform.objects.get(pk=id)
#         platform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#-------------------------------Function Based Views------------------------------------------#
# In function based views you have to use decorator @api_view(['GET','POST']) you can
# change the allowed methods by just passing them into that decorator
# Also manually you have to check that request method is post or get.

# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_detail(request, id):
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=id)
#         except Movie.DoesNotExist:
#             return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=id)
#         serializer = MovieSerializer(movie, data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=id)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#--------------------------------------END---------------------------------------------------#
