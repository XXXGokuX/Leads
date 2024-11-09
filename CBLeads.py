import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import timedelta
import numpy as np

# Set Streamlit page configuration
st.set_page_config(page_title="Lead Analysis Dashboard", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        .header {
            color: #2F4F4F;
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            margin-top: 20px;
        }
        .subheader {
            color: #696969;
            font-size: 1.5rem;
            text-align: center;
            margin-bottom: 20px;
        }
        .sidebar .sidebar-content {
            background-color: #f4f4f9;
            font-size: 1.2rem;
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            font-size: 1.2rem;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
nav_option = st.sidebar.radio("Go to", (
    "Introduction", "Lead Source Distribution", "Lead Response Time Analysis",
    "Lead Status by Source", "Leads Over Time", "Lead Conversion Rate by Representative",
    "Course Interest Analysis", "Course Trends with Forecast"
))

# Introduction section
if nav_option == "Introduction":
    st.markdown("<h1 class='header'>Lead Analysis Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subheader'>Upload an Excel file with columns similar to 'Coding Bytes.xlsx' to generate insights.</p>", unsafe_allow_html=True)

    # File upload section
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

    # Data loading and validation
    if uploaded_file is not None:
        st.session_state['data'] = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully! Use the navigation to explore different analyses.")
    else:
        st.info("Please upload an Excel file to get started.")

# Check if data is loaded in session state
if 'data' in st.session_state:
    data = st.session_state['data']
    
    # Preprocess data
    data = data.dropna(subset=['Lead Date & Time'])
    data['Lead Date & Time'] = pd.to_datetime(data['Lead Date & Time'], errors='coerce')
    data['Lead Source'] = data['Lead Source'].fillna('Unknown')
    data['Lead Status'] = data['Lead Status'].fillna('No Status')
    data['Lead Representative'] = data['Lead Representative'].fillna('Unassigned')

    # Lead Source Distribution section
    if nav_option == "Lead Source Distribution":
        st.markdown("<h2 class='header'>Lead Source Distribution</h2>", unsafe_allow_html=True)
        
        #col1, col2 = st.columns(2)
        st.subheader("Count Plot")
        fig, ax = plt.subplots(figsize=(16, 10))
        sns.countplot(data=data, x='Lead Source', ax=ax)
        ax.set_title('Lead Source Distribution')
        st.pyplot(fig)

        
        st.subheader("Pie Chart")
        fig, ax = plt.subplots(figsize=(8, 8))
        data['Lead Source'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, ax=ax)
        ax.set_ylabel('')
        st.pyplot(fig)

    # Lead Response Time Analysis section
    if nav_option == "Lead Response Time Analysis":
        st.markdown("<h2 class='header'>Lead Response Time Analysis</h2>", unsafe_allow_html=True)
        if 'Last Call' in data.columns:
            data['Response Time (Hours)'] = (data['Last Call'] - data['Lead Date & Time']).dt.total_seconds() / 3600
            fig, ax = plt.subplots(figsize=(14, 8))  # Increase figure size to fit more labels

            sns.boxplot(data=data, x='Course', y='Response Time (Hours)', ax=ax)

            # Rotate the x-axis labels for better visibility
            plt.xticks(rotation=90)

            # Adjust title and labels for readability
            ax.set_title("Response Time by Course", fontsize=16)
            ax.set_xlabel("Course", fontsize=12)
            ax.set_ylabel("Response Time (Hours)", fontsize=12)

            # Optionally, reduce the number of x-axis ticks if there are too many courses
            ax.set_xticks(ax.get_xticks()[::max(1, len(data['Course'].unique()) // 20)])  # Limit to 20 ticks for better visibility

            st.pyplot(fig)

        else:
            st.warning("Column 'Last Call' not found in the uploaded data.")

    # Lead Status by Source section
    if nav_option == "Lead Status by Source":
        st.markdown("<h2 class='header'>Lead Status by Source</h2>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(15, 8))
        sns.countplot(data=data, x='Lead Source', hue='Lead Status', ax=ax)
        ax.set_title('Lead Status by Source')
        st.pyplot(fig)

    # Leads Over Time section
    if nav_option == "Leads Over Time":
        st.markdown("<h2 class='header'>Leads Over Time</h2>", unsafe_allow_html=True)
        leads_over_time = data.groupby(data['Lead Date & Time'].dt.date).size()
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(x=leads_over_time.index, y=leads_over_time.values, ax=ax)
        ax.set_title('Leads Over Time')
        st.pyplot(fig)

    # Lead Conversion Rate by Representative section
    if nav_option == "Lead Conversion Rate by Representative":
        st.markdown("<h2 class='header'>Lead Conversion Rate by Representative</h2>", unsafe_allow_html=True)
        conversion_rate = data[data['Lead Status'] == 'Converted'].groupby('Lead Representative').size() / data.groupby('Lead Representative').size()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=conversion_rate.index, y=conversion_rate.values, ax=ax)
        ax.set_title("Lead Conversion Rate by Representative")
        st.pyplot(fig)

        # Plot the data
        plt.figure(figsize=(12, 6))
        sns.countplot(data=data, x='Lead Representative', hue='Lead Status')
        plt.title('Lead Conversion by Representative')
        plt.xlabel('Lead Representative')
        plt.ylabel('Count')
        plt.legend(title='Lead Status')
        
        # Render the plot in Streamlit
        st.pyplot(plt)

    # Course Interest Analysis section
    if nav_option == "Course Interest Analysis":
        st.markdown("<h2 class='header'>Course Interest Analysis</h2>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.countplot(data=data, y='Course', order=data['Course'].value_counts().index, ax=ax)
        ax.set_title('Course Interest Analysis')
        st.pyplot(fig)
        
        
        data['Lead Date & Time'] = pd.to_datetime(data['Lead Date & Time'], errors='coerce')
        data = data.dropna(subset=['Lead Date & Time', 'Course'])

        # Create a new column 'Lead Date' from 'Lead Date & Time'
        data['Lead Date'] = data['Lead Date & Time'].dt.date
        # Grouping data by 'Lead Date' and 'Course' to count the number of leads
        course_trends = data.groupby(['Lead Date', 'Course']).size().reset_index(name='Lead Count')
        plt.figure(figsize=(12, 8))
        sns.lineplot(data=course_trends, x='Lead Date', y='Lead Count', hue='Course', marker="o")
        plt.title("Course Trends Over Time")
        plt.xlabel("Date")
        plt.ylabel("Number of Leads")
        plt.xticks(rotation=45)
        plt.legend(title="Course", bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Render the plot in Streamlit
        st.pyplot(plt)

    # Course Trends with Forecast section
    if nav_option == "Course Trends with Forecast":
        st.markdown("<h2 class='header'>Course Trends Over Time with Forecast</h2>", unsafe_allow_html=True)
        forecast_days = 30
        future_dates = pd.date_range(start=data['Lead Date & Time'].max() + timedelta(days=1), periods=forecast_days)
        
        
        for course in data['Course'].unique():
            course_data = data[data['Course'] == course].set_index('Lead Date & Time').resample('D').size()
            course_data = course_data.reindex(pd.date_range(course_data.index.min(), course_data.index.max()), fill_value=0)
            X = (course_data.index - course_data.index.min()).days.values.reshape(-1, 1)
            y = course_data.values
            model = LinearRegression().fit(X, y)
            future_X = (future_dates - course_data.index.min()).days.values.reshape(-1, 1)
            future_pred = model.predict(future_X)

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(course_data.index, course_data, label="Historical")
            ax.plot(future_dates, future_pred, '--', label="Forecast")
            ax.set_title(f"Course Trends for {course}")
            ax.legend()
            st.pyplot(fig)
