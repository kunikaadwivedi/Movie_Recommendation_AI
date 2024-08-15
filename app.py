import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get(('https://api.themoviedb.org/3/movie/{'
                            '}?api_key=0476cb4524d10a8d12fb32bbf89ff414').format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
#       fetch poster from API
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movies.iloc[i[0]].movie_id))
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    .custom-title {
        font-family: 'Comic Sans MS', cursive;
        font-size: 46px;
        color:  #990000;
        text-align: center;
        
    }
</style>
    """,
    unsafe_allow_html=True
)
st.markdown('<h1 class="custom-title">MOVIE RECOMMENDATION GENERATOR</h1>', unsafe_allow_html=True)
st.markdown(
    """
    <style>
    .custom-font {
        font-family: Georgia, sans-serif;
        font-size: 20px;
        color: #808080;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("""
 <p class="custom-font">
Welcome to the Movie Recommendation Generator! Enjoy a selection of amazing movies from around the world.
""",
    unsafe_allow_html=True)
Selected_movie_name = st.selectbox('Look for your movie in the Drop Box', movies['title'].values)

if st.button('Recommend'):
    names,poster = recommend(Selected_movie_name)
    st.markdown('If you liked this movie then you will also love these')
    col1, col2, col3,col4,col5 = st.columns(5)
    with col1:
        st.image(poster[0],caption=names[0],width=130)
    with col2:
        st.image(poster[1],caption=names[1],width=130)
    with col3:
        st.image(poster[2],caption=names[2],width=130)
    with col4:
        st.image(poster[3],caption=names[3],width=130)
    with col5:
        st.image(poster[4],caption=names[4],width=130)

prompt = st.chat_input("Tell us your Experience")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")
st.markdown("""
---
*Created by Kunikaa Dwivedi with ❤️ using [Streamlit](https://streamlit.io/)*
""")