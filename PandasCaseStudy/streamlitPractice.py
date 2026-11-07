import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sb
import time 
st.title("Hello Streamlit-er 👋")
st.markdown(
    """ 
    This is a playground for you to try Streamlit and have fun. 

    **There's :rainbow[so much] you can build!**
    
    We prepared a few examples for you to get started. Just 
    click on the buttons above and discover what you can do 
    with Streamlit. 
    """
)

if st.button("Send balloons!"):
    st.balloons()

st.markdown("""

**hello here is my first data analysis :rainbow[startup data] analysis.**

first dataframe look here:
""")

st.code("""
def odd(num):
  print('odd' if num&1 else 'even')

def generator(s,e):
  i = s
  while i < e:
    yield i 
    i +=1 
""")

st.latex('a^3 + b^2 + c = 0 ')


df = sb.load_dataset('tips')

st.dataframe(df)

st.json({
    'ids': [121,122,123],
    'name' : ['abdul rehman','hamza' , 'ali'] ,
    'city' : ['skp' , 'lhr' , 'mlt']
})

st.sidebar.title('Options to view:')
st.sidebar.button(':rainbow[Data preview]')

col1 , col2 = st.columns(2)
with col1:
    st.markdown('### Column1 analysis')
with col2:
    st.markdown('### Column 2 analysis')
  

bar = st.progress(0)

for i in range(1,101):
    #time.sleep(0.1)
    bar.progress(i)

mail = st.text_input('Enter your mail')
password = st.text_input('Enter password')
if mail == 'abc@gmail.com' and password == 'abc123' :
    st.success('Login successful!')
else:
    st.error('Login failed!')

date = st.date_input('Enter date' )

st.selectbox('Select gender' , ['male' , 'female' , 'others']) 
st.file_uploader('Upload file')

st.menu_button('Data sets' , options=['Titanic' , 'IPL' , 'Movies'])