from django.urls import path,include
from . import views 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('stream', views.StreamPlatformVS,basename='streamplatform')


urlpatterns = [
    # path('list/', views.movie_list, name='movie-list'),
    # path('<int:pk>/', views.movie_detail, name='movie-detail')
    
    # path('list/', views.MovieListAV.as_view(), name='movie-list'),
    # path('<int:pk>/', views.MovieDetailAV.as_view(), name='movie-detail')
    
    path('list/', views.WatchListAV.as_view(), name='watchlist-list'),
    path('<int:pk>/', views.WatchListDetailAV.as_view(), name='watchlist-detail'),
    
    path('list2/', views.WatchListGV.as_view(), name='watch-list'), #For Filtering purpose we are creating this URL temporary 
    
    path('', include(router.urls)),
    
    
    # path('stream/', views.StreamPlatformListAV.as_view(), name='streamplatform-list'),
    # path('stream/<int:pk>/', views.StreamPlatformDetailAV.as_view(), name='streamplatform-detail'),
    
    # path('review/', views.ReviewList.as_view(), name='review-list'),
    # path('review/<int:pk>/', views.ReviewDetail.as_view(), name='review-detail'), 
    
    path('<int:pk>/review-create/', views.ReviewCreate.as_view(), name = 'review-create'),
    path('<int:pk>/reviews/', views.ReviewList.as_view(), name = 'review-list'),
    path('review/<int:pk>/', views.ReviewDetail.as_view(), name = 'review-detail'),
    
    # path('review/<str:username>/', views.UserReview.as_view(), name = 'user-review-detail'),
    path('review/', views.UserReview.as_view(), name = 'user-review-detail'),
]



#stream/1/review/ -- It needs to show all reviews for the movie id 1
