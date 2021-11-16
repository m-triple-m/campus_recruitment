# from datetime import datetime
from re import U
import streamlit as st
# import pandas as pd
# import numpy as np

# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
# from streamlit.hashing import UnhashableTypeError
# from database import Report
from visualization import *
from AnalyseData import Analyse
# import matplotlib as mpl
# import matplotlib.pyplot as plt
# from database import Report

# __________________________________________________PageLayoutSetup_______________________________________

st.set_page_config(page_title="Analysis of campus recruitment",
                   layout='wide')

# _______________________________________________Call Analyse Function From AnalyseData.py_________________

analysis = Analyse()

# ____________________________________________________HEADER____________________________________________

with st.spinner("Loading Data..."):
    st.markdown("""
        <style>
            .mainhead{
                font-family: Courgette ,Book Antiqua ;
                #letter-spacing:.1px;
                word-spacing:1px;
                color :#73e663; 
                text-shadow: 1px -1px 1px white, 1px -1px 2px white;
                font-size:40px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
            .detail{
                font-size:18px;
                letter-spacing:.1px;
                word-spacing:1px;
                font-family:Calibri;
                color:#cb7435;
                display:inline-block;
                }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="mainhead" style="text-align: center;"> Campus Recruitment Analysis </h1> <img src="" />',
                unsafe_allow_html=True)

    st.image('images/hero.jpg', use_column_width=True)


st.markdown("___")

# ________________________________________________Data Details______________________________________________


st.markdown(""" 
        <style>
            .head{
                font-family: Calibri, Book Antiqua; 
                font-size:4vh;
                padding-top:2%;
                padding-bottom:2%;
                font-weight:light;
                color:#ffc68a;
                #text-align:center;
            }
        </style>
        """, unsafe_allow_html=True)


# @st.cache(suppress_st_warning=True)
def viewDataset():

    with st.spinner("Loading Data..."):
        df = analysis.getDataframe()
        st.markdown(
            '<p class="head"> Dataset Used In This Project</p>', unsafe_allow_html=True)

        st.markdown("")
        st.dataframe(df)

        st.markdown(""" 
        <style>
            .block{
                font-family: Book Antiqua; 
                font-size:24px;
                 padding-top:11%;
                font-weight:light;
                color:lightblue;
            }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('---')
        cols = st.columns(4)
        cols[0].markdown(
            '<p class="block"> Number of Rows : <br> </p>', unsafe_allow_html=True)
        cols[1].markdown(f"# {df.shape[0]}")
        cols[2].markdown(
            '<p class= "block"> Number of Columns : <br></p>', unsafe_allow_html=True)
        cols[3].markdown(f"# {df.shape[1]}")
        st.markdown('---')

        st.markdown('<p class= "head"> Summary </p>', unsafe_allow_html=True)
        st.markdown("")
        st.dataframe(df.describe())
        st.markdown('---')

        types = {'object': 'Categorical',
                 'int64': 'Numerical', 'float64': 'Numerical'}
        types = list(map(lambda t: types[str(t)], df.dtypes))
        st.markdown('<p class="head">Dataset Columns</p>',
                    unsafe_allow_html=True)
        for col, t in zip(df.columns, types):
            st.markdown(f"## {col}")
            cols = st.columns(4)
            cols[0].markdown('#### Unique Values :')
            cols[1].markdown(f"## {df[col].unique().size}")
            cols[2].markdown('#### Type :')
            cols[3].markdown(f"## {t}")
            st.markdown("___")


def analyseCategory():
    st.header('Analysis of Different Categories')
    st.markdown('# ')

    categories = [
        {'name': 'Specialization', 'column': 'specialisation'},
        {'name': 'Work Experience', 'column': 'workex'},
        {'name': 'Graduation Degree Field', 'column': 'degree_t'},
        {'name': 'High School Field', 'column': 'hsc_s'},
        {'name': 'Placement Status', 'column': 'status'}
    ]

    for category in categories:
        data = analysis.getCategoryCount(category.get('column'))
        st.plotly_chart(plotBar(x=data.index, y=data.values, xlabel='Category',
                                ylabel='Count of Applicants', title=category.get('name')), use_container_width=True)


def analyseEducation():
    st.header('Education Analysis')

    st.plotly_chart(plotHistogram(analysis.getDataframe()[
                    'ssc_p'], title="High School percentage", xlabel='Distribution of percentage', ylabel='No. of Applicants'), use_container_width=True)

    st.plotly_chart(plotHistogram(analysis.getDataframe()[
                    'hsc_p'], title="Higher Secondary percentage", xlabel='Distribution of percentage', ylabel='No. of Applicants'), use_container_width=True)

    st.plotly_chart(plotHistogram(analysis.getDataframe()[
                    'degree_p'], title="Degree percentage", xlabel='Distribution of percentage', ylabel='No. of Applicants'), use_container_width=True)

    st.plotly_chart(plotHistogram(analysis.getPlacedDataframe()[
                    'salary'], title="Salaries Offered", xlabel='Distribution of salaries', ylabel='No. of placed Applicants'), use_container_width=True)


def analysePlacement():
    st.header('Placement Analysis')

    st.plotly_chart(plotGroupedBar(analysis.getPlacementByField(), [
                    'Placed', 'Not Placed'], title='Secondary Education Field', xlabel='Fields', ylabel='No. of Applicants'), use_container_width=True)

    st.plotly_chart(plotGroupedBar(analysis.getPlacementBySpec(), [
                    'Placed', 'Not Placed'], title='MBA stream', xlabel='Fields', ylabel='No. of Applicants'), use_container_width=True)

    col1, col2 = st.columns(2)
    data = analysis.getExpPlaced('Yes')
    col1.plotly_chart(plotpie(values=data.values,
                              labels=data.index, title='Percentage of Placed Students with Work Experience'), use_container_width=True)

    data = analysis.getExpPlaced('No')
    col2.plotly_chart(plotpie(values=data.values,
                              labels=data.index, title='Percentage of Placed Students without Work Experience'), use_container_width=True)

    st.plotly_chart(plotScatter(data=analysis.getPlacedDataframe(),
                                x='degree_p', y="salary", color='degree_t', title='Comparison of passing percentage with Salary placed'), use_container_width=True)

    st.plotly_chart(plotScatter(data=analysis.getPlacedDataframe(),
                                x='etest_p', y="salary", color='degree_t', title='Comparison of college placement text percentage with Salary placed'), use_container_width=True)


sidebar = st.sidebar

sidebar.title(
    'Campus Recruitment Analysis')
sidebar.markdown("### Select Your Choice :point_down:")
options = ['View Dataset',
           'Analyze Categories',
           #    'Education Analysis',
           'Analyze Placement',
           ]

choice = sidebar.selectbox(options=options, label="")
if choice == options[0]:
    viewDataset()
elif choice == options[1]:
    analyseCategory()
# elif choice == options[2]:
#     analyseEducation()
elif choice == options[2]:
    analysePlacement()
