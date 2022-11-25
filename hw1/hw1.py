#Moeez Shahid - ms2978
#Mahad Rauf - mar648
#Fauzan Amjad - fa408
import math
from collections import defaultdict
from collections import Counter

# You may not add any other imports

# For each function, replace "pass" with your code

# --- TASK 1: READING DATA ---

# 1.1
def read_ratings_data(f):
    retDict = {}
    file = open(f)
    rating = file.readline().strip()
    while(rating):
        i = rating.split('|')
        if i[0] in retDict.keys():
            retDict[i[0]][i[2]] = i[1]
        else:
            retDict[i[0]] = {i[2]:i[1]}
        rating = file.readline().strip()
    for key in retDict.keys():
        retDict[key] = list(retDict[key].values())
    file.close()
    return retDict

# 1.2
def read_movie_genre(f):
    retDict = {}
    file = open(f)
    genre = file.readline().strip()
    while(genre):
        i = genre.split('|')
        retDict[i[2]] = i[0]
        genre = file.readline().strip()
    file.close()
    return retDict

# --- TASK 2: PROCESSING DATA ---

# 2.1
def create_genre_dict(d):
    retDict = {}
    for i in d.keys():
        if (d[i] in retDict.keys()):
            retDict[d[i]].append(i)
        else:
            retDict[d[i]] = [i]
    return retDict

# 2.2
def calculate_average_rating(d):
    retDict = {}
    for i in d.keys():
        ratings = d[i]
        ratingsAsNumbers = [float(j) for j in ratings]
        retDict[i] = sum(ratingsAsNumbers)/len(ratingsAsNumbers)
    return retDict

# --- TASK 3: RECOMMENDATION ---

# 3.1
def get_popular_movies(d, n=10):
    retDict = {}
    for w in sorted(d, key=d.get, reverse=True)[:n]:
        retDict[w] = d[w]
    return retDict

# 3.2
def filter_movies(d, thres_rating=3):
    retDict = {}
    for w in sorted(d, key=d.get, reverse=True):
        if(d[w] >= thres_rating):
            retDict[w] = d[w]
    return retDict

# 3.3
def get_popular_in_genre(genre, genre_to_movies, movie_to_average_rating, n=5):
    filtered_dict = {}
    return_dict = {}
    
    for keys, values in genre_to_movies.items() :
        if keys == genre :
            for value in values :
                filtered_dict.update({value : movie_to_average_rating[value]})

    for key in sorted(filtered_dict, key=filtered_dict.get, reverse=True)[:n]:
        return_dict.update({key : filtered_dict[key]})
        
    return return_dict

# 3.4
def get_genre_rating(genre, genre_to_movies, movie_to_average_rating):
    filtered_dict = {}
    total = float(0)
    iterations = 0
    for keys, values in genre_to_movies.items() :
        if keys == genre :
            for value in values :
                filtered_dict.update({value : movie_to_average_rating[value]})
                total = total + float(movie_to_average_rating[value])
                iterations = iterations + 1
        
    return total/iterations

# 3.5
def genre_popularity(genre_to_movies, movie_to_average_rating, n=5):
    ratings_dict = {}
    final_dict = {}
    rating = float(0)

    for key, values in genre_to_movies.items() :
        rating = get_genre_rating(key, genre_to_movies, movie_to_average_rating)
        ratings_dict.update({key : float(rating)})
     
    for key in sorted(ratings_dict, key=ratings_dict.get, reverse=True)[:n]:
        final_dict.update({key : ratings_dict[key]})
    
    return final_dict

# --- TASK 4: USER FOCUSED ---

# 4.1
def read_user_ratings(f):
    userRatingsDictionary ={}
    file = open(f)
    for line in file:
        i = line.strip().split('|')
        if int(i[2]) in userRatingsDictionary:
            userRatingsDictionary[int(i[2])].append((i[0],float(i[1])))
        else: 
            userRatingsDictionary[int(i[2])] = [(i[0],float(i[1]))]
    return userRatingsDictionary

# 4.2
def get_user_genre(user_id, user_to_movies, movie_to_genre):
    genreDictionary = {}
    movieRatings = user_to_movies[user_id]
    for movie in movieRatings:
        if movie_to_genre[movie[0]] in genreDictionary:
            currentRating = genreDictionary[movie_to_genre[movie[0]]][0];
            currentMovieAmount = genreDictionary[movie_to_genre[movie[0]]][1];
            newRating = ((currentRating * currentMovieAmount)+movie[1])/(currentMovieAmount + 1)
            newMovieAmount = currentMovieAmount + 1
            genreDictionary[movie_to_genre[movie[0]]] = [newRating, newMovieAmount]
        else:
            genreDictionary[movie_to_genre[movie[0]]] = [movie[1], 1]
    maxRating = -1.0;
    userGenre = "No Genre"
    for key in genreDictionary:
        if genreDictionary[key][0]>maxRating:
            maxRating = genreDictionary[key][0]
            userGenre = key
    return userGenre

# 4.3
def recommend_movies(user_id, user_to_movies, movie_to_genre, movie_to_average_rating):
    favoriteGenre = get_user_genre(user_id, user_to_movies, movie_to_genre)
    watchedMovies = []
    for arry in user_to_movies[user_id]:
        watchedMovies.append(arry[0])
    favoriteGenreMovies = []
    for movieName in movie_to_average_rating:
        if ((movie_to_genre[movieName] == favoriteGenre) and ((movieName not in watchedMovies))):
            favoriteGenreMovies.append((movieName, movie_to_average_rating[movieName]));
    favoriteGenreMovies.sort(key = lambda x: x[1])
    favoriteGenreMovies.reverse()
    if len(favoriteGenreMovies) <= 3:
        top3 = []
        for movieName in favoriteGenreMovies:
            top3.append(movieName[0])
        return top3
    else:
        top3  = []
        for x in range(3):
            top3.append(favoriteGenreMovies[x][0])
        return top3

# --- main function for your testing ---
def main():
    s = '---------------------------------------------------------------------------------------------------------------------'
    
    print('1.1')
    ratingsDict = read_ratings_data('movieRatingSample.txt')
    print(ratingsDict)
    print(s)
    
    print('1.2')
    genreDict = read_movie_genre('genreMovieSample.txt')
    print(genreDict)
    print(s)
    
    print('2.1')
    genreDict2 = create_genre_dict(genreDict)
    print(genreDict2)
    print(s)
    
    print('2.2')
    avgRatingDict = calculate_average_rating(ratingsDict)
    print(avgRatingDict)
    print(s)
    
    print('3.1')
    popularMovies = get_popular_movies(avgRatingDict, 15)
    print(popularMovies)
    print(s)
    
    print('3.2')
    filteredMovies = filter_movies(avgRatingDict, 4)
    print(filteredMovies)
    print(s)
    
    print('3.3')
    poplGenreMovies = get_popular_in_genre('Action', genreDict2, avgRatingDict, 5)
    print(poplGenreMovies)
    print(s)
    
    print('3.4')
    genreRating = get_genre_rating('Action', genreDict2, avgRatingDict)
    print(genreRating)
    print(s)
    
    print('3.5')
    genrePopularity = genre_popularity(genreDict2, avgRatingDict, 3)
    print(genrePopularity)
    print(s)
    
    print('4.1')
    userRatings = read_user_ratings('movieRatingSample.txt')
    print(userRatings)
    print(s)
    
    print('4.2')
    userGenre = get_user_genre(5, userRatings, genreDict)
    print(userGenre)
    print(s)
    
    print('4.3')
    recommendations = recommend_movies(5, userRatings, genreDict, avgRatingDict)
    print(recommendations)
    print(s)

main()
