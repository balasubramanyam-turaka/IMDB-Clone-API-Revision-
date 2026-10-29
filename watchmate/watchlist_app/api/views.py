from watchlist_app.models import  Review, WatchList, StreamPlatform
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import  WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from .throttling import ReviewCreateThrottle, ReviewListThrottle

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .pagination import WatchListPagination, WatchListLOPagination, WatchListCPagination

from .permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly


class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    
    # def get_queryset(self):
    #     username = self.kwargs['username'] #kwargs is a dictionary that contains the keyword arguments passed to the view. In this case, it will contain the username of the user for which we want to get the reviews. This username is passed in the url as a keyword argument. For example, if the url is /reviews/user/john/, then username will be john.
    #     return Review.objects.filter(review_user__username=username) #review_user is the related_name of the ForeignKey field in the Review model. It is used to get the related User object for a Review object. In this case, we are filtering the reviews based on the review_user's username which is equal to username.

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username)

class ReviewCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewCreateThrottle]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk =self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk) #watchlist is the related_name of the ForeignKey field in the Review model. It is used to get the related WatchList object for a Review object. In this case, we are getting the WatchList object for which we want to create a review. The pk is passed in the url as a keyword argument. For example, if the url is /stream/1/review-create/, then pk will be 1.
        
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user) #watchlist is the related_name of the ForeignKey field in the Review model. It is used to get the related WatchList object for a Review object.
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie!")
        
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating']) / 2 
        
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()
        
        
        serializer.save(watchlist=watchlist, review_user=review_user) 
        


class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    throttle_classes = [ReviewListThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    
    
    def get_queryset(self): #This will override the default queryset and will return only the reviews for the movie with id=pk.
        pk =self.kwargs['pk'] #kwargs is a dictionary that contains the keyword arguments passed to the view. In this case, it will contain the pk of the movie for which we want to get the reviews. This pk is passed in the url as a keyword argument. For example, if the url is /stream/1/review/, then pk will be 1.
        return Review.objects.filter(watchlist=pk)  #This will return all the reviews for the movie with id=pk. watchlist is the related_name of the ForeignKey field in the Review model. It is used to get the related WatchList object for a Review object. In this case, we are filtering the reviews based on the watchlist id which is equal to pk.

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'
    






# Mixins and GenericAPIView
# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer #serializer_class attribute name we can't change because we are using mixins. 
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    


# class ReviewDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    # queryset = Review.objects.all()
    # serializer_class = ReviewSerializer
    # def get(self, request, *args, **kwargs):
    #     return self.retrieve(request, *args, **kwargs)
    
    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)
    
    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)
    

class StreamPlatformVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    

# class StreamPlatformVS(viewsets.ReadOnlyModelViewSet):
#     queryset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer







#viewsets.ViewSets

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
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     def update(self, request, pk=None):
#         platform = get_object_or_404(StreamPlatform.objects.all(), pk=pk)
#         serializer = StreamPlatformSerializer(platform, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     def destroy(self, request, pk=None):
#         platform = get_object_or_404(StreamPlatform.objects.all(), pk=pk)
#         platform.delete()
#         return Response({'message': 'StreamPlatform deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)




#Class Based API Views

# class StreamPlatformListAV(APIView):
#     def get(self, request):
#         platforms = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(platforms, many=True )   # context={'request': request}
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# class StreamPlatformDetailAV(APIView):
#     def get(self, request, pk):
#         try:
#             platform =StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             return Response({'error': 'StreamPlatform not found.'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = StreamPlatformSerializer(platform )
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         platform = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(platform, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     def delete(self, request, pk):
#         platform = StreamPlatform.objects.get(pk=pk)
#         platform.delete()
#         return Response({'message': 'StreamPlatform deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

#Class Based API Views

class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request):
        watchlists = WatchList.objects.all()
        serializer = WatchListSerializer(watchlists, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:   
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

#For Filtering(Searching, Filtering and Ordering purpose we are creating a WatchList class using Generics View so ... For Testing Purpose we are creating this)

class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    # pagination_class = WatchListPagination
    # pagination_class = WatchListLOPagination
    pagination_class =  WatchListCPagination
    
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'platform__name']
    
    # filter_backends = [filters.SearchFilter]
    # search_fields=['^title', 'platform__name']
    
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg_rating']










        
class WatchListDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request,pk):
        try:
            watchlist = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'WatchList not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(watchlist)
        return Response(serializer.data)
    
    def put(self,request,pk):
        watchlist = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(watchlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        watchlist = WatchList.objects.get(pk=pk)
        watchlist.delete()
        return Response({'message': 'WatchList deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)





























# Function Based Views

# @api_view(['GET','POST'])
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
#             return Response(serializer.errors)
    


# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_detail(request, pk):
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'error': 'Movie not found.'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response({'message': 'Movie deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    