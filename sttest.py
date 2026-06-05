from sqlalchemy import label
import streamlit as st


st.title("Streamlit Test")
st.write("This is a test of Streamlit.")

"""
# My first app
Here's our first attempt at using data to create a table:
"""


import pandas as pd
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

df



st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))


import numpy as np

dataframe = np.random.randn(10, 20)
st.dataframe(dataframe)


import streamlit as st
import numpy as np
import pandas as pd

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_min(axis=0))

import streamlit as st
import numpy as np
import pandas as pd

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))
st.table(dataframe)


import streamlit as st
import numpy as np
import pandas as pd

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.bar_chart(chart_data)
st.line_chart(chart_data)


import streamlit as st
import numpy as np
import pandas as pd

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)


import streamlit as st
x = st.slider('x', 1, 100, 50)
st.write(x)  # 👈 this is a widget
st.write(x, 'squared is', x * x)


x = st.button('button') 




box = st.selectbox('Select Box', [1, 2,3])  
st.write('You selected:', box)



st.text_input("Your name", key="name")

# You can access the value at any point with:
st.session_state.name

st.checkbox('I agree')

st.toggle('Toggle me')

st.time_input('Set an alarm for', value=None, key="alarm_time", help="This is a time input widget")

st.text_input("Your name", key="name1")

st.select_slider('Select a range of values', options=[1, 2, 3, 4, 5], key="range")

st.slider('Select a range of values', 0, 100, (25, 75), key="range_slider")

st.radio('Radio', ['Radio 1', 'Radio 2'], key="radio")

st.multiselect('Multiselect', ['Multiselect 1', 'Multiselect 2'], key="multiselect")

st.number_input('Number input', key="number_input")

st.file_uploader('File uploader', key="file_uploader", help="This is a file uploader widget", accept_multiple_files=False, type=['png', 'jpg', 'jpeg'], disabled=False, label_visibility="visible")

st.data_editor(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}), key="data_editor")

st.date_input('Date input', key="date_input", help="input Date")

st.color_picker('Color picker', key="color_picker", help="This is a color picker widget", value="#000000", disabled=False, label_visibility="visible")


import streamlit as st

enable = st.checkbox("Enable camera")
picture = st.camera_input("Take a picture", disabled=not enable)

if picture:
    st.image(picture)



