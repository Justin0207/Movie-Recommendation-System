# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 18:16:58 2024

@author: HP
"""

import streamlit as st
import pickle
import base64

st.set_page_config(layout="wide")


def set_background(main_bg):
    '''
    A function to unpack an image from root folder and set as bg.
 
    Returns
    -------
    The background.
    '''
    # set bg name
    main_bg_ext = "png"
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover;
         }}
         .st-emotion-cache-sxs2aw{{
             background: None}}
         </style>
         """,
         unsafe_allow_html=True
     )

set_background(r'C:\Users\HP\Downloads\movie.jpg') 





st.header('Movie Recommendation System')


net_movies = pickle.load(open(r'C:\Users\HP\Desktop\DS\Amazon Recommender\random_movies.pkl', 'rb'))

similarity = pickle.load(open(r'C:\Users\HP\Desktop\DS\Amazon Recommender\similarity.pkl', 'rb'))





selected_movie = st.selectbox(
    'Select a Movie', options = net_movies['Title_and_year'].values
    )




numbers = st.number_input('Numbers of Movies to recommend : ', value = 5, step = 1, max_value = 10)


    
def fetch_poster(suggestion):
        
        poster_url = [ ]
        
        for movie_id in suggestion:
            poster_url.append(net_movies.iloc[movie_id]['Poster_Url'])
            
        return poster_url

def recommend_movie(movie, number_to_recommend = numbers):
    recommended_movies = []
    
    suggestion = []
    
    movie_index = net_movies[net_movies['Title_and_year'] == movie].index[0]
    
    distances = similarity[movie_index]
    
    movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:numbers+1]
    
    for i in movies_list:
        
        recommended_movies.append(net_movies.iloc[i[0]]['Title_and_year'])
    
    for i in movies_list:
        
        suggestion.append(i[0])
    
    
    
    poster_url = fetch_poster(suggestion)
    
    
    
    for i in range(len(suggestion)):
        
        movies = net_movies.iloc[suggestion[i]]['Title_and_year']
        
        for j in movies:
            movies_list.append(j)
    return recommended_movies, poster_url







if st.button('Show Recommendation'):
    
    movies_recommended, poster_url = recommend_movie(selected_movie)

    #col1, col2, col3, col4, col5 = st.columns(5)
    #with col1:
       # st.text(movies_recommended[1])
        #st.image(poster_url[1])
    #with col2:
        #st.text(movies_recommended[2])
        #st.image(poster_url[2])
    #with col3:
        #st.text(movies_recommended[3])
        #st.image(poster_url[3])
    #with col4:
        #st.text(movies_recommended[4])
        #st.image(poster_url[4])
    #with col5:
        #st.text(movies_recommended[5])
        #st.image(poster_url[5])
        
    cols = st.columns(numbers)
    for i in range(numbers):
            cols[i].text(movies_recommended[i])
            cols[i].image(poster_url[i])
        
    