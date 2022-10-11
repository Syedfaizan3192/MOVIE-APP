from watchlist_app.models import WatchList
from watchlist_app.api.views import (MovieListView, MovieDetailsView, StreamvideoListView, StreamvideoDetailView,
                                     ReviewList, ReviewDetails, ReviewCreate, StremLListView, UserProfileFilter, WatchListPrac)
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('streams', StremLListView, basename="snippets")


urlpatterns = [
    path('list/', MovieListView.as_view(), name='movie-list'),
    path('<int:pk>', MovieDetailsView.as_view(), name='movie-details'),
    path("list2/", WatchListPrac.as_view(), name='watch-list'),

    # path('stream/',  StreamvideoListView.as_view(), name='Stream-videos'),
    # path('stream/<int:pk>', StreamvideoDetailView.as_view(), name='stream-details'),

    # ***********************for viewset check:****************************************
    path('', include(router.urls)),



    # path('review/', ReviewList.as_view(), name='review'),
    # path('review/<int:pk>', ReviewDetails.as_view(), name='review'),

    path('<int:pk>/review-create',
         ReviewCreate.as_view(), name='review-create'),
    path("<int:pk>/review/", ReviewList.as_view(), name='review-list'),
    path("review/<int:pk>", ReviewDetails.as_view(), name='review'),
    # path("reviews/<str:username>", UserProfileFilter.as_view(), name='review'),

    # for query params

    path("reviews/", UserProfileFilter.as_view(), name='review'),
]
