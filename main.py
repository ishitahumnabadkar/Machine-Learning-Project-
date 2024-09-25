import pickle
import pandas as pd
import streamlit as st
import requests
from bs4 import BeautifulSoup


def get_poster_url(movie_title):
    # Create a search URL for IMDb
    search_url = f"https://www.imdb.com/find?q={movie_title.replace(' ', '+')}&s=tt&ttype=ft"

    print(f"Searching for: {movie_title}")
    print(f"Search URL: {search_url}")

    # Make a request to fetch the search results page
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first result in the search results
    first_result = soup.find('td', class_='result_text')
    if first_result:
        # Get the link to the movie page
        movie_link = first_result.a['href']
        movie_page_url = f"https://www.imdb.com{movie_link}"

        print(f"Movie Page URL: {movie_page_url}")

        # Fetch the movie page
        movie_response = requests.get(movie_page_url)
        movie_soup = BeautifulSoup(movie_response.text, 'html.parser')

        # Find the poster image
        poster_tag = movie_soup.find('div', class_='poster').a.img
        if poster_tag:
            print(f"Found poster URL: {poster_tag['src']}")
            return poster_tag['src']  # Return the URL of the poster image

    print("Poster not found.")
    return None  # Return None if no poster is found


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies


# Loading the movies.pkl and setting 'title' as the column
movies_list = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_list, columns=['title'])  # Assign 'title' as column

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Movies like?', movies['title'].values)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    st.write(f"Recommendations for '{selected_movie_name}':")

    for movie in recommendations:
        st.write(movie)
        poster_url = get_poster_url(movie)  # Get the poster URL from the web
        if poster_url:
            st.image(poster_url, width=200)  # Display the poster image
        else:
            st.write("Poster not available.")
