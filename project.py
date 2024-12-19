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

        # Dynamic column selection
        st.subheader("🔧 Select Columns")
        st.write("Choose the columns for input and emission factor.")

        selected_input_column = st.selectbox("Select the Category/Item Column:", data.columns, help="This column contains product or category names.")
        selected_emission_column = st.selectbox("Select the Emission Factor Column:", data.columns, help="This column contains CO₂ emission factors.")

        # User input for comparison
        st.subheader("📈 Compare Emissions for Multiple Items")
        selected_rows = st.multiselect(
            "Select Rows (Categories/Items) to Compare:",
            data[selected_input_column].unique(),
            help="You can select multiple rows to compare emissions."
        )

        amount = st.number_input("Enter the Amount (e.g., distance, usage, or units):", min_value=0.0, step=0.1, value=1.0, help="Amount applies equally to all selected rows.")

        # Comparison and visualization
        if st.button("Compare Emissions"):
            if selected_rows:
                try:
                    # Filter data for selected rows and calculate emissions
                    filtered_data = data[data[selected_input_column].isin(selected_rows)]
                    filtered_data["Total Emissions"] = pd.to_numeric(filtered_data[selected_emission_column], errors="coerce") * amount

                    # Check for invalid data
                    if filtered_data["Total Emissions"].isnull().any():
                        st.error("Some rows have invalid emission factors. Please check your dataset.")
                    else:
                        # Display results in a table
                        st.subheader("🔍 Emission Results:")
                        st.table(filtered_data[[selected_input_column, selected_emission_column, "Total Emissions"]])

                        # Plot comparison graph
                        st.subheader("📊 Emission Comparison Chart")
                        fig = px.bar(
                            filtered_data,
                            x=selected_input_column,
                            y="Total Emissions",
                            labels={"Total Emissions": "Emissions (kg CO₂)", selected_input_column: "Category/Item"},
                            title="Comparison of Carbon Emissions",
                            color=selected_input_column
                        )
                        st.plotly_chart(fig)
                except Exception as e:
                    st.error(f"Error during calculation: {e}")
            else:
                st.warning("Please select at least one row to compare emissions.")
    else:
        st.warning("Unable to load dataset. Please ensure the file is valid and formatted correctly.")





if __name__ == "__main__":
    main()