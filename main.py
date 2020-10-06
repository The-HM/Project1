#Henry Murillo
#10/5/2020
from nltk.corpus import stopwords
import streamlit as st
import pandas as pd
import main_functions
from nltk.probability import FreqDist
from nltk import sent_tokenize
from nltk import word_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import json
import nltk
import requests

nltk.download("stopwords")
#nltk.download("punkt")
st.title("COP 4813 - Web Application Programming")
st.title("Project 1")
st.header("Part A - The Stories API")
st.write("This app uses the Top Stories API to display the most common words used in the top"
         " current articles based on a specified topic selected by the user. The data is displayed"
         " as line chart and as a wordcloud image.")
st.subheader("I - Topic Selection")

nameBox = st.text_input("Please enter your name")
selectBox = st.selectbox("Select a topic of your interest",["arts","automobiles","books","business",
                                                            "fashion","food","health","home","insider",
                                                            "magazine","movies","nyregion","obituaries",
                                                             "opinion","politics","realestate","science",
                                                             "sports","sundayreview","technology","theater",
                                                             "t-magazine","travel","upshot","us","world"])
if nameBox and selectBox:
    st.write(nameBox, " selected ",selectBox)
    api_key_dict = main_functions.read_from_file("JSON_Files/api_key.json")
    api_key = api_key_dict["my_key"]
    url = "https://api.nytimes.com/svc/topstories/v2/" + selectBox + ".json?api-key=" + api_key
    response = requests.get(url).json()
    main_functions.save_to_file(response,"JSON_Files/response.json")

    articles = main_functions.read_from_file("JSON_Files/response.json")

    str1 = ""
    for i in articles["results"]:
        str1 = str1 + i["abstract"]

    words = word_tokenize(str1)
    words_no_punc = []

    for w in words:
        if w.isalpha():
            words_no_punc.append(w.lower())

    stopwords = stopwords.words("english")

    cleanWords = []

    for w in words_no_punc:
        if w not in stopwords:
            cleanWords.append(w)

    fdist = FreqDist(cleanWords)

    st.subheader("II - Frequency Distribution")
    if st.checkbox("Click here to generate frequency distribution"):
        mostCommon = pd.DataFrame(fdist.most_common(10))
        dataFrame = pd.DataFrame({"words": mostCommon[0],"count": mostCommon[1]})
        f = px.line(dataFrame, x="words", y="count", title="")
        st.plotly_chart(f)

    st.subheader("III - Wordcloud")
    if st.checkbox("Click here to generate a wordcloud"):
        wordCloud = WordCloud().generate(str1)
        plt.figure(figsize=(12,12))
        plt.imshow(wordCloud)
        plt.axis('off')
        st.set_option('deprecation.showPyplotGlobalUse',False)
        st.pyplot()


st.header("Part B - Most Popular Articles")
st.write("Select if you want to see the most shared, emailed, or viewed articles.")
selectBox2 = st.selectbox("Select your preferred set of articles",["shared","emailed","viewed"])
selectBox3 = st.selectbox("Select the period of time (last days),",["1","7","30"])

if selectBox2 and selectBox3:
    api_key_dict = main_functions.read_from_file("JSON_Files/api_key.json")
    api_key = api_key_dict["my_key"]
    url2 = "https://api.nytimes.com/svc/mostpopular/v2/" + selectBox2 +"/" + selectBox3 + ".json?api-key=" + api_key
    response2 = requests.get(url2).json()
    main_functions.save_to_file(response2, "JSON_Files/response2.json")

    articles2 = main_functions.read_from_file("JSON_Files/response2.json")

    str2 = ""
    for i in articles2["results"]:
        str2 = str2 + i["abstract"]


    wordCloud2 = WordCloud().generate(str2)
    plt.figure(figsize=(12, 12))
    plt.imshow(wordCloud2)
    plt.axis('off')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()


