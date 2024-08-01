import requests
import random

# Tmdb Api
movie_api_key = "774e9132f23e81e442ceadbc47e213f7"
# Google books
book_api_key = "AIzaSyAaRg-7XpJ1FiHgQKSo0eYfNuu9YNsdZ40"

# Movie Search
def movie_search(item_name):
    movie_api_url = f'https://api.themoviedb.org/3/search/movie?api_key={movie_api_key}&query={item_name}'
    movie_search_response = requests.get(movie_api_url).json()

    if 'results' in movie_search_response and movie_search_response['results']:
        movie_id = movie_search_response['results'][0]['id']
        movie_details_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={movie_api_key}&append_to_response=reviews'
        movie_details = requests.get(movie_details_url).json()

        # Getting and Grouping only the genre names
        movie_details['genre_names'] = [genre['name'] for genre in movie_details['genres']]

        # Getting Similar Movies
        similar_movies_url = f'https://api.themoviedb.org/3/movie/{movie_id}/similar?api_key={movie_api_key}'
        similar_movies = requests.get(similar_movies_url).json()

        return movie_details, similar_movies
    else:
        return None, None

# Book Search
def book_search(item_name):
    book_api_url = f'https://www.googleapis.com/books/v1/volumes?q={item_name}&key={book_api_key}'
    book_search_response = requests.get(book_api_url).json()

    if 'items' in book_search_response:
        book_id = book_search_response['items'][0]['id']
        book_details_url = f'https://www.googleapis.com/books/v1/volumes/{book_id}'
        book_details = requests.get(book_details_url).json()

        # Assigning categories directly to genre_names
        book_details['genre_names'] = book_details.get('volumeInfo', {}).get('categories', [])

        # Getting Similar Books
        similar_books_url = f'https://www.googleapis.com/books/v1/volumes?q={item_name}&key={book_api_key}'
        similar_books = requests.get(similar_books_url).json()

        return book_details, similar_books
    else:
        return None, None

# Display results
def display_result(movie_details, similar_movies, book_details, similar_books, collated_result):
    if not movie_details:
        print("Movie not found.")
    else:
        print(f"Title: {movie_details['title']}")
        print(f"Overview: {movie_details['overview']}")
        print(f"Rating: {movie_details['vote_average']}")
        print(f"Genres: {', '.join(movie_details['genre_names'])}")

        # Printing the results in similar Movies
        print("")
        print("Similar Results")
        print("")


        for movie in similar_movies.get('results', []):
            mv_similar_result = f"{movie['title']} (movie)"

            print(f"Title: {movie['title']} (movie)")

            collated_result.append(mv_similar_result)

    if not book_details:
        print("Book not found.")
    else:
        # Printing the result in Books
        print("")
        print("")

        print(f"Title: {book_details.get('volumeInfo', {}).get('title', 'N/A')}")
        print(f"Rating: {book_details.get('volumeInfo', {}).get('averageRating', 'N/A')}")
        print(f"Genres: {', '.join(book_details['genre_names'])}")

        # Printing the results in similar Books
        print("")
        print("Similar Results")
        print("")

        for book in similar_books.get('items', []):
            bk_similar_result = f"{book['volumeInfo']['title']} (book)"
            print(f"Title: {book['volumeInfo']['title']} (book)")
            collated_result.append(bk_similar_result)

collated_result = []
item_name = input("Please enter Title: ")
movie_details, similar_movies = movie_search(item_name)
book_details, similar_books = book_search(item_name)
display_result(movie_details, similar_movies, book_details, similar_books, collated_result)


print("")
print("Recommended")
print("")


def recommmend(collated_result):
  recommendation = []
  i = 1
  while i < 4 :
    if len(recommendation) <= len(collated_result):
      ans = random.randint(1, len(collated_result))

      recommendation.append(collated_result[ans])
    i += 1



  if recommendation[0] == recommendation[1] or recommendation[0] == recommendation[2]:
    recommendation.remove(recommendation[0])
  elif recommendation[1] == recommendation[2] or recommendation[1] == recommendation[0]:
    recommendation.remove(recommendation[1])
  elif recommendation[2] == recommendation[0] or recommendation[2] == recommendation[1]:
    recommendation.remove(recommendation[2])
  elif len(recommendation) > 3:
    recommendation.remove(recommendation[3])
  print(recommendation)

recommmend(collated_result)
print("")
refresh_input = input("Do you want to refresh Recommendation (Y/N): ")

if refresh_input.lower() == 'y':
  print("")
  print("New Recommended")
  print("")
  recommmend(collated_result)
else:
   print('Thank you')