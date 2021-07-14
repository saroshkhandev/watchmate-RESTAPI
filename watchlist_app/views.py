# from django.shortcuts import render
# from .models import Movie
# from django.http import JsonResponse
# # Create your views here.

# def movie_list(request):
#     movies = Movie.objects.all()   #This a queryset -- which means fetching data from Movie Model to a temperory variable from which we can fetch value later on.
#     data = {
#         'Movies': list(movies.values())
#     }

#     return JsonResponse(data)

# def movie_detail(request, id):
#     movie = Movie.objects.get(pk=id)  #queryset and as well this time we're taking id as input too, and in our queryset we're passing that id as our primary key to just fetch that particular query, instead of all.
#     data = {
#         'name': movie.name,
#         'description': movie.description,
#         'active': movie.active
#     }

#     return JsonResponse(data)