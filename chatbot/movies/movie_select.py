import streamlit as st
import random

# Movie data
movies = [
    {'title': 'The Shawshank Redemption', 'genre': 'Drama'},
    {'title': 'The Godfather', 'genre': 'Crime'},
    {'title': 'Pulp Fiction', 'genre': 'Crime'},
    {'title': 'The Dark Knight', 'genre': 'Action'},
    {'title': 'Fight Club', 'genre': 'Drama'},
]

def movie_recommendation_app():
    st.title('Movie Recommendation App')
    
    # Genre selection
    genre = st.selectbox(
        'Select a genre:',
        ['-- Select --', 'Drama', 'Crime', 'Action']
    )
    
    # Recommendation button
    if st.button('Get Recommendation'):
        if genre != '-- Select --':
            movies_by_genre = [movie for movie in movies if movie['genre'] == genre]
            
            if movies_by_genre:
                recommended_movie = random.choice(movies_by_genre)
                st.write(f'Recommended Movie: {recommended_movie["title"]}')
            else:
                st.write('No movies found for the selected genre')
        else:
            st.warning('Please select a genre first')

if __name__ == '__main__':
    movie_recommendation_app()

