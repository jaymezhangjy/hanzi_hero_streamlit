import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
from gtts import gTTS
from io import BytesIO
from streamlit_drawable_canvas import st_canvas
import tensorflow as tf
from tensorflow import keras
import json


# Function for image pre-processing of child's answers [COMPLETED]
def preprocess_image(image):
        image = Image.fromarray(image) # Since canvas.image_data is an array, use Image.fromarray() to read
        image1 = image.resize((64,64)) # Resize image from original canvas size of (300, 300) to (64, 64) to fit into model
        image2 = image1.convert('L') # Convert image to from RGB to greyscale
        image3 = np.array(image2) / 255.0  # Rescale by dividing by 255 and save image2 as a separate array image3
        image4 = image3.reshape((64, 64, 1)) # Reshape from (300, 300, 4) to (64, 64, 1)
        image5= np.expand_dims(image4, axis=0) # To add 4th dummy dimension for batch on top of height, width, channel
        return image5

# Function to load Chinese character prediction model [COMPLETED]
@st.cache_resource
def load_model():
     model = keras.models.load_model('self_trained_model_multiclass_st.keras', compile=False) # Loading pre-trained model for prediction, no need to compile
     return model


header = st.container()
question = st.container()
question1 = st.container()
question2 = st.container()
question3 = st.container()

with header:
    st.title(':rainbow[Welcome to Hanzi Hero] 🥷🏼')
    st.header("Training in Progress 🥋", divider='rainbow')
    st.markdown('''Click the Play button :arrow_forward: to listen to the word, and write it :writing_hand: in the space provided. When you are done, click 'Check my answer'.''')

    # st.write(st.session_state.selected_char)


with question:
    for i in range(len(st.session_state.selected_char)):
        st.subheader(f'Question {i+1}:')
        # Creating audio file
        audio_file = BytesIO() # To work with in-memory file-like objects without actually writing to or reading from physical file
        tts = gTTS(st.session_state.selected_char[i], lang='zh-TW')
        tts.write_to_fp(audio_file)
        st.audio(audio_file)
                
        # Creating drawing canvas
        canvas = BytesIO()
        canvas = st_canvas(
                        stroke_width=10,
                        height=300,
                        width=300,
                        background_color='#eee',
                        key=st.session_state.selected_char[i]
                    )
            
        preprocessed_image = preprocess_image(canvas.image_data.astype('uint8'))
            
        model = load_model()
        with open('class_labels.json', 'r') as f:
            class_labels = json.load(f) # loads class_labels saved from model training
        prediction = model.predict(preprocessed_image)
        predicted_class = np.argmax(prediction, axis=1)
        predicted_char = class_labels[predicted_class[0]]

        st.write(prediction)
        st.write(predicted_class)
        st.write(predicted_char)

        if predicted_char == st.session_state.selected_char[i]:
            result = '✅ Correct, great attempt 🙌🏽'
        else:
            result = '❎ Incorrect, please practise more 💪🏽'
        

        if st.button('Check my answer', key=i):
            st.markdown(result)


# with question1:
#     st.subheader(f'Question 1:')
#     # Creating audio file
#     audio_file = BytesIO() # To work with in-memory file-like objects without actually writing to or reading from physical file
#     tts = gTTS('手', lang='zh-TW')
#     tts.write_to_fp(audio_file)
#     st.audio(audio_file)
            
#     # Creating drawing canvas
#     canvas = BytesIO()
#     canvas = st_canvas(
#                     stroke_width=10,
#                     height=300,
#                     width=300,
#                     background_color='#eee',
#                     key='手'
#                 )
        
#     preprocessed_image = preprocess_image(canvas.image_data.astype('uint8'))
        
#     model = load_model()
#     with open('class_labels.json', 'r') as f:
#         class_labels = json.load(f) # loads class_labels saved from model training
#     prediction = model.predict(preprocessed_image)
#     predicted_class = np.argmax(prediction, axis=1)
#     predicted_char = class_labels[predicted_class[0]]

#     # st.write(prediction)
#     # st.write(predicted_class)
#     # st.write(predicted_char)

#     if predicted_char == '手':
#         result = '✅ Correct, great attempt 🙌🏽'
#     else:
#         result = '❎ Incorrect, please practise more 💪🏽'
    

#     if st.button('Check my answer', key='0'):
#         st.markdown(result)
        

# with question2:
#     st.subheader(f'Question 2:')
#     # Creating audio file
#     audio_file = BytesIO() # To work with in-memory file-like objects without actually writing to or reading from physical file
#     tts = gTTS('我', lang='zh-TW')
#     tts.write_to_fp(audio_file)
#     st.audio(audio_file)
            
#     # Creating drawing canvas
#     canvas = BytesIO()
#     canvas = st_canvas(
#                     stroke_width=10,
#                     height=300,
#                     width=300,
#                     background_color='#eee',
#                     key='我'
#                 )
        
#     preprocessed_image = preprocess_image(canvas.image_data.astype('uint8'))
        
#     model = load_model()
#     with open('class_labels.json', 'r') as f:
#         class_labels = json.load(f) # loads class_labels saved from model training
#     prediction = model.predict(preprocessed_image)
#     predicted_class = np.argmax(prediction, axis=1)
#     predicted_char = class_labels[predicted_class[0]]

#     # st.write(prediction)
#     # st.write(predicted_class)
#     # st.write(predicted_char)

#     if predicted_char == '我':
#         result = '✅ Correct, great attempt 🙌🏽'
#     else:
#         result = '❎ Incorrect, please practise more 💪🏽'
    
#     # st.button('Check my answer Q2', on_click=click_button, key='2')
#     # if st.session_state.clicked:
#     #     st.write(result)
#     if st.button('Check my answer', key='1'):
#         st.markdown(result)

# with question3:
#     st.subheader(f'Question 3:')
#     # Creating audio file
#     audio_file = BytesIO() # To work with in-memory file-like objects without actually writing to or reading from physical file
#     tts = gTTS('有', lang='zh-TW')
#     tts.write_to_fp(audio_file)
#     st.audio(audio_file)
            
#     # Creating drawing canvas
#     canvas = BytesIO()
#     canvas = st_canvas(
#                     stroke_width=10,
#                     height=300,
#                     width=300,
#                     background_color='#eee',
#                     key='目'
#                 )
        
#     preprocessed_image = preprocess_image(canvas.image_data.astype('uint8'))
        
#     model = load_model()
#     with open('class_labels.json', 'r') as f:
#         class_labels = json.load(f) # loads class_labels saved from model training
#     prediction = model.predict(preprocessed_image)
#     predicted_class = np.argmax(prediction, axis=1)
#     predicted_char = class_labels[predicted_class[0]]

#     # st.write(prediction)
#     # st.write(predicted_class)
#     # st.write(predicted_char)

#     if predicted_char == '有':
#         result = '✅ Correct, great attempt 🙌🏽'
#     else:
#         result = '❎ Incorrect, please practise more 💪🏽'
    
#     # st.button('Check my answer Q3', on_click=click_button, key='3')
#     # if st.session_state.clicked:
#     #     st.write(result)

#     if st.button('Check my answer', key='2'):
#         st.markdown(result)
            





