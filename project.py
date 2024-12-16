import pandas as pd
import streamlit as st
import plotly.express as px


# Load the dataset
def load_dataset(filepath):
 
    try:
        data = pd.read_excel(filepath, engine="openpyxl")
        return data
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None
def main():
    st.title("🌍 Carbon Footprint Monitoring Tool")
    st.write("Calculate and visualize carbon emissions interactively.")

    # Filepath to the dataset
    filepath = "carbon_catalogue_dataset.xlsx"

    # Load the dataset
    data = load_dataset(filepath)
    if data is not None:
        # Display dataset preview
        st.subheader("📊 Dataset Preview:")
        st.dataframe(data.head())





if __name__ == "__main__":
    main()