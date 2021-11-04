import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit_analytics


# We use streamlit_analytics to track the site like in Google Analytics
streamlit_analytics.start_tracking()
# your streamlit code here


# configuring the page and the logo
st.set_page_config(page_title='Mohamed Gabr - House Price Prediction', page_icon ='logo.png', layout = 'wide', initial_sidebar_state = 'auto')


import os
import base64

# the functions to prepare the image to be a hyperlink
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache(allow_output_mutation=True)
def get_img_with_href(local_img_path, target_url):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}">
            <img src="data:image/{img_format};base64,{bin_str}" />
        </a>'''
    return html_code


# preparing the layout for the top section of the app
# dividing the layout vertically (dividing the first row)
row1_1, row1_2, row1_3 = st.columns((1, 5, 4))

# first row first column
with row1_1:
    gif_html = get_img_with_href('logo.png', 'https://golytics.github.io/')
    st.markdown(gif_html, unsafe_allow_html=True)

with row1_2:
    # st.image('logo.png')
    st.title("Exploratory Data Analysis for The American Football")
    st.markdown("<h2>Webscraping and Analyzing The statistics of Rushing Data</h2>", unsafe_allow_html=True)

# first row second column
with row1_3:
    st.info(
        """
        ##
        This data product has been prepared to be used as a POC for sports analytics. First, the data has been scrapped from the web. 
        Then grouped by year, team , and position of the player to analyze the player's performance in rushing. The same process 
        can be used to analyze other topics like Receiving, Scrimmage Stats, Defense, Kicking & Punting, Kick & Punt Returns, Scoring, and others.
        """)



#st.title('NFL Football Stats (Rushing) Explorer')

#st.set_option('deprecation.showPyplotGlobalUse', False)

st.markdown("""
This app performs simple webscraping of NFL Football player stats data (focusing on Rushing)!
""")

st.subheader('How to use the model?')
''' 
You can use this data product by modifying the User Input Parameters (year, team, position) on the left. The app will filter the data based on your parameters. 

1- You will see the statistics of each player in the table
based on the criteria you selected in the User Input Parameters

2- you can browse the correlation between the player's features by clicking the Intercorrelation Heatmap button.

3- Also, you can download the data in the table as a CSV file.
'''

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1990,2020))))

# Web scraping of NFL player stats
# https://www.pro-football-reference.com/years/2019/rushing.htm
@st.cache
def load_data(year):
    url = "https://www.pro-football-reference.com/years/" + str(year) + "/rushing.htm"
    html = pd.read_html(url, header = 1)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats
playerstats = load_data(selected_year)

# Sidebar - Team selection
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
unique_pos = ['RB','QB','WR','FB','TE']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering data
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# Heatmap
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_team.to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        fig, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(fig)



st.info("Note: [The data source is: pro-football-reference.com](https://www.pro-football-reference.com/years/2019/rushing.htm).")
with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Published By: <a href="https://golytics.github.io/" target="_blank">Dr. Mohamed Gabr</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)



streamlit_analytics.stop_tracking(unsafe_password="forward1")
