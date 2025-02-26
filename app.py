import streamlit as st
import pandas as pd
import os 
from io import BytesIO

# Set up our App
st.set_page_config(page_title="💽 Data sweeper", layout='wide')
st.title("💽 Data sweeper")
st.write("Seamlessly convert between CSV and Excel with smart data cleaning and powerful visuals!")

uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=['csv', 'xlsx'], accept_multiple_files=True) 

if uploaded_files:
    for file in uploaded_files:
        file_ext =os.path.splitext(file.name)[-1].lower()

        if file_ext == '.csv':
            df = pd.read_csv(file)
        elif file_ext == '.xlsx':
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file type:{file_ext}")
            continue

        # Display info about the file
        st.write(f"**File.Name:** {file.name}")  
        st.write(f"**File Size:** {file.Size/1024}")

        # Show 5 rows of our df
        st.write("🔍preview the Head of the Dataframe:")
        st.dataframe(df.head())

        # Option for data cleaning 
        st.subheader("🛠️Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
               if st.button(f"Remove Duplicates from {file.name}"):
                  df.drop_duplicates(inplace=True)
                  st.write("Duplicates Removed!")
            
            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                   numeric_cols = df.select_dtypes(include=['numbers']).columns
                   df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                   st.write("Missing Values have been Filled!")

                   # choose Specific columns to keep or Convert
                   st.subheader("🎸select Columns to Convert")
                   columns = st.multiselect("Choose Columns for {file.name}", df.columns, default=df.columns)
                   df = df[columns]

                  # # Create Some Visualizations
                   st.subheader("📊Data Visualizations")
                   if st.checkbox(f"Show Visualizations for {file.name}"):
                      st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

                    # Convert the File -> CSV or Excel
                      st.subheader("🔄Conversion Options")
                      conversion_type = st.radio(f"Convert {file.name} to:", ['CSV', 'Excel'], key=file.name)
                      if st.button(f"Convert {file.name}"):
                           buffer = BytesIO()
                           if conversion_type == 'CSV':
                              df.to_csv(buffer, index=False)
                              file_name = file.name.replace(file_ext, '.csv')
                              mime_type = 'text/csv'

                            elif conversion_type == 'Excel':
                                df.to_excel(buffer, index=False)
                                file_name = file.name.replace(file_ext, '.xlsx')
                                mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                                buffer.seek(0)


                            # Download Button
                            st.download_button(
                                label=f" ⬇️ Download {file_name} as {conversion_type}",
                                data=buffer,
                                filename=file_name,
                                mime=mime_type
                            )
st.success("🥂 All file processed!" ) 





















                
                            