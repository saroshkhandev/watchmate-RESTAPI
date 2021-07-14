from django.urls import path, include
from watchlist_app.api import views
from rest_framework.routers import DefaultRouter

# from .. import views
# we have a router for both stream platform list and details
router = DefaultRouter()
router.register('stream', views.StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    #for class based views
    path('list/', views.WatchListAV.as_view(), name='movie-list'),
    path('<int:id>/', views.WatchDetailAV.as_view(), name='watch-detail'),

    path('',include(router.urls)),

#     path('stream/', views.StreamPlatformAV.as_view(), name='platform-list'),
#     path('stream/<int:id>', views.StreamPlatformDetailAV.as_view(),
#          name='platform-detail'),
    
    # path('review/', views.ReviewList.as_view(), name='review-list'),
    # path('review/<int:id>', views.ReviewDetail.as_view(), name='review-detail')


# these are the urls for looking the reviews of a particular movie
    path('<int:id>/review-create/', views.ReviewCreate.as_view(),
         name='review-create'), # have to pass id of that particular movie
    path('<int:id>/reviews/', views.ReviewList.as_view(),
         name='review-list'),  # have to pass id of that particular movie
    path('review/<int:id>/', views.ReviewDetail.as_view(),
         name='review-detail'),  # have to pass id of particular review of a movie



    #------------------------------------------------------
    #for function based views
    # path('list/', views.movie_list, name='movie-list'),
    # path('<int:id>/', views.movie_detail, name='movie-detail')
    
    
]
