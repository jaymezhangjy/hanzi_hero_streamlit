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


header = st.container()
upload_spelling_list = st.container()


with header:
    st.title(':rainbow[Welcome to Hanzi Hero] 🥷🏼')
    st.markdown('''With the help of this tool, all you need to do is to upload the spelling list :memo:, select the words to test for this session :white_check_mark:, and click 'Let the training begin 🥋'.''')

    
with upload_spelling_list:
    # To upload image of spelling list
    st.header('Upload spelling list :memo:', divider='rainbow')
    uploaded_file = st.file_uploader("Choose a file to upload", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        st.image(uploaded_file) # Displays image after it's uploaded
        list_of_chinese_char = ['手', '我', '目', '头', '口', '走', '自己', '足', '舌', '公公', '东西', '要', '看', '有', '狗', '它']

        # To select which words to test for this session
        st.subheader('Please select the words to test for this session :white_check_mark:', divider='rainbow')
    
        list_of_checkbox = [] # To create same number of items in list_of_checkbox as list_of_chinese_char
        for i in range(len(list_of_chinese_char)):
            list_of_checkbox.append(False)

        df = pd.DataFrame(
            {'Words': list_of_chinese_char,
            'Yes/No': list_of_checkbox,}
        )

        edited_df = st.data_editor(
            data=df,
            use_container_width=True,
            height=500,
            column_config={
                'list_of_checkbox': st.column_config.CheckboxColumn(
                    label='Yes/No',
                    default=False,
                )
            },
            disabled=['list_of_chinese_char'],
            hide_index=True,
        )

        # List of Chinese characters selected by user
        selected_char = edited_df.loc[edited_df['Yes/No'] == True]['Words'].tolist()

        if selected_char not in st.session_state:
            st.session_state.selected_char = selected_char

        # st.write(st.session_state.selected_char)    

        if st.button(':rainbow[Let the training begin] 🥋', use_container_width=True):
            st.switch_page('pages/Training in Progress.py')





