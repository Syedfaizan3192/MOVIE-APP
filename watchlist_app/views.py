# from django.shortcuts import render
# from watchlist_app.models import Movies
# from django.http import JsonResponse
# # Create your views here.


# def Movie_list(request):
#     movie = Movies.objects.all()
#     data = {
#         'movies': list(movie.values())
#     }
#     return JsonResponse(data)


# def Movie_details(request, pk):
#     details = Movies.objects.get(pk=pk)
#     data = {'name': details.name,
#             'description': details.desription,
#             'active': details.active
#             }
#     return JsonResponse(data)