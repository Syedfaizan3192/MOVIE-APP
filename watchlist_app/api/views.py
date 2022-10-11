from ast import Delete
from asyncio import streams
from distutils import errors
from operator import is_
from xml.dom import ValidationErr

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import mixins
# from rest_framework.decorators import api_view
from rest_framework import filters, generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.throttling import (AnonRateThrottle, ScopedRateThrottle,
                                       UserRateThrottle)
from rest_framework.views import APIView
from user_app.api.throttle import ReviewListThrottle
from watchlist_app.api.pagenition import (WatchListCpage, WatchListLOpage,
                                          WatchListpage)
from watchlist_app.api.permission import (IsAdminOrReadOnly,
                                          ReviewUSerOrReadOnly)
from watchlist_app.api.serializers import (Rviewserializers,
                                           StremVideosSerializers,
                                           WatchListserializers)
from watchlist_app.models import Review, StremVideos, WatchList

# ViewSet.ModelsViewset


# Filter Review Detial for the spcific user profile:
class UserProfileFilter(generics.ListAPIView):
    serializer_class = Rviewserializers

# Review by string

    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)

# Review by params (E.g: /?username=faizan) where ?username is the param:

    def get_queryset(self):
        username = self.request.query_params.get("username", None)
        return Review.objects.filter(review_user__username=username)


class StremLListView(viewsets.ModelViewSet):
    queryset = StremVideos.objects.all()
    serializer_class = StremVideosSerializers
    permission_classes = [IsAdminOrReadOnly]


# ViewSet


# class StremLListView (viewsets.ViewSet):
#     def list(self, request):
#         queryset = StremVideos.objects.all()
#         serializer = StremVideosSerializers(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StremVideos.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = StremVideosSerializers(user)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = StremVideosSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

#     def destroy(self, request):
#         stream = StremVideos.objects.get(pk=pk)
#         stream.delete()
#         return Response({'errors': 'Deleted'})

#     def update(self, request):
#         stream = StremVideos.objects.get(pk=pk)
#         serailizer = StremVideosSerializers(stream, data=request.data)
#         if serailizer.is_valid():
#             serailizer.save()
#             return Response(serailizer.data)
#         else:
#             return Response(serailizer.data)


# GENERIC VIEWS
class ReviewCreate(generics.CreateAPIView):
    serializer_class = Rviewserializers
    # Only Loggedin user can see this list
    permission_classes = [IsAuthenticated]
    # ************************************

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(
            WatchList=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You already done!")

        if WatchList.number_of_rating == 0:
            WatchList.avg_rating = serializer.validated_data['Rating']
        else:
            WatchList.avg_rating = (
                WatchList.avg_rating + serializer.validated_data['Rating']) / 2

        WatchList.number_of_rating = WatchList.number_of_rating + 1
        WatchList.save()

        serializer.save(WatchList=watchlist, review_user=review_user)


class ReviewList (generics.ListCreateAPIView):
    # queryset = Review.objects.all()
    serializer_class = Rviewserializers

    # Only Loggedin user can see this list
    permission_classes = [IsAuthenticated]
    # ************************************

    # Throttle
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]

    # Custom Throttle

    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    #  search filter using django-filter

    filter_backends = [DjangoFilterBackend]
    filter_fields = ['review_user__username', 'active']
# --------------------------------------------------------------
# Just for test purpose practice searching with django!
# --------------------------------------------------------------
# first checking using with filter backend:
# --------------------------------------------------------------
# class WatchListPrac (generics.ListAPIView):
#     queryset = WatchList.objects.all()
#     serializer_class = WatchListserializers
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['title', 'platform__name']
# --------------------------------------------------------------
# using search:
# --------------------------------------------------------------

# '^' Starts-with search.
# '=' Exact matches.
# '@' Full-text search. (Currently only supported Django's PostgreSQL backend.)
# '$' Regex search.
# --------------------------------------------------------------


class WatchListPrac (generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListserializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['^title', 'platform__name']
    pagination_class = WatchListCpage
# --------------------------------------------------------------

# ordering search:
# --------------------------------------------------------------

# class WatchListPrac (generics.ListAPIView):
#     queryset = WatchList.objects.all()
#     serializer_class = WatchListserializers
#     filter_backends = [filters.OrderingFilter]
#     ordering_fields = ['avg_rating']
# --------------------------------------------------------------


class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = Rviewserializers
    permission_classes = [ReviewUSerOrReadOnly]

    # throttle_classes = [UserRateThrottle, AnonRateThrottle]

    # Throttle
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "review_details"

    # Only can see without logged in but not update it or destroy it as it is ReadOnly this list - object-level Authentication

    # permission_classes = [IsAuthenticatedOrReadOnly]

    # ************************************


# GENERIC AND MIXINS
# class ReviewDetails (mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = Rviewserializers

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


# class ReviewList (mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = Rviewserializers

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


class StreamvideoListView(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        straeam = StremVideos.objects.all()
        seriailizer = StremVideosSerializers(straeam, many=True)
        return Response(seriailizer.data)

    def post(self, request):
        serailizer = StremVideosSerializers(data=request.data)
        if serailizer.is_valid():
            serailizer.save()
            return Response(serailizer.data)
        else:
            return Response(serailizer.errors)


class StreamvideoDetailView(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            stream = StremVideos.objects.get(pk=pk)
        except StremVideos.DoesNotExist:
            return Response({'errors': 'not found!'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StremVideosSerializers(stream)
        return Response(serializer.data)

    def put(self, request, pk):
        stream = StremVideos.objects.get(pk=pk)
        serailizer = StremVideosSerializers(stream, data=request.data)
        if serailizer.is_valid():
            serailizer.save()
            return Response(serailizer.data)
        else:
            return Response(serailizer.data)

    def delete(self, request, pk):
        stream = StremVideos.objects.get(pk=pk)
        stream.delete()
        return Response({'errors': 'Deleted'})


# CLASS BASED VIEW
class MovieListView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        movie = WatchList.objects.all()
        serializer = WatchListserializers(movie, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListserializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class MovieDetailsView(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({"errors": "Not Found!"}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListserializers(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListserializers(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response({"Deleted.....!!!"}, status=status.HTTP_200_OK)


# FUNCTION BASED VIEW


# @api_view(['GET', 'POST'])
# def Movie_list(request):
#     if request.method == 'GET':
#         movies = Movies.objects.all()
#         serializer = Movieserializers(movies, many=True)
#         return Response(serializer.data)
#     if request.method == "POST":
#         serializer = Movieserializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


# @api_view(["GET", "PUT", "DELETE"])
# def Movie_details(request, pk):
#     if request.method == "GET":
#         try:
#             movie = Movies.objects.get(pk=pk)
#         except:
#             return Response({'errors': "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = Movieserializers(movie)

#         return Response(serializer.data)
#     if request.method == "PUT":
#         movie = Movies.objects.get(pk=pk)
#         serializer = Movieserializers(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)

#     if request.method == "DELETE":
#         movie = Movies.objects.get(pk=pk)
#         movie.delete()
#         return Response({"Deleted.....!!!"}, status=status.HTTP_202_ACCEPTED)
