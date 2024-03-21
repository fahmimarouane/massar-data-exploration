import streamlit as st
import pandas as pd
import numpy as np 
import plotly.express as px
import os
import re
import datetime
from streamlit_option_menu import option_menu



st.set_page_config(page_title="Dashboard Massar",page_icon="📊",layout="wide")
#st.header("Exploration des données du système de gestion scolaire MASSAR")
# Add title using Markdown
#st.markdown("# Exploration des données du système de gestion scolaire MASSAR")

custom_css = """
<style>
    /* Define responsive CSS rules */
    @media screen and (max-width: 600px) {
        /* Adjust layout for small screens */
        .container {
            width: 90%; /* Adjust width for small screens */
        }
    }

    @media screen and (min-width: 601px) {
        /* Adjust layout for medium and large screens */
        .container {
            width: 70%; /* Adjust width for medium and large screens */
        }
    }
    .metric-card {
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #ccc;
        background-color: #f9f9f9;
        color: #333;
        margin: 10px;
    }

    .metric-card-title {
        font-size: 20px;
        margin-bottom: 5px;
    }

    .metric-card-value {
        font-size: 24px;
        font-weight: bold;
    }

    .metric-card-delta {
        font-size: 16px;
    }

    .black-background {
        background-color: #000;
        color: #BF1F4D; /* Soft Blue Color */
    }
</style>
"""

# Apply the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown("@FAHMI Marouane")
st.markdown("---")
# Use the custom class for elements on black background
st.markdown("<h2 class='black-background' style='text-align: center;'>Exploration des données du système de gestion scolaire MASSAR</h2>", unsafe_allow_html=True)



# Define the starting row for data extraction
start_row = 17

# Define the column names for the specific data to be extracted
column_names = ['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 5', 'النقطة', 'النقطة.1', 'النقطة.2', 'النقطة.3']



def process_files(uploaded_files):
    # Find the selected file with the specified name pattern
    selected_file = None
    for file in uploaded_files:
        if "ListEleve" in file.name and (file.name.endswith(".xls") or file.name.endswith(".xlsx")):
            selected_file = file
            break

    if selected_file is None:
        return None

    # Define the mapping from Arabic to French
    arabic_to_french = {'ذكر': 'H', 'أنثى': 'F'}

    # Open the Excel file
    xls = pd.ExcelFile(selected_file)

    # Get the list of sheet names
    sheet_names = xls.sheet_names

    # Define an empty dictionary to store dictionaries for each DataFrame
    df_dicts = {}

    # Iterate through each sheet and store its contents in a separate DataFrame
    for i, sheet_name in enumerate(sheet_names):
        # Read the sheet into a DataFrame, starting from row 13 and selecting specific columns
        df = pd.read_excel(selected_file, sheet_name=sheet_name, usecols=['Unnamed: 11', 'Unnamed: 12', 'Unnamed: 16', 'Unnamed: 23'], skiprows=13)
        
        # Rename columns for convenience
        df.columns = ['Sexe', 'nom', 'Prenom','Code Massar']
        df = df.drop(0)
        # Reset index after dropping row
        df = df.reset_index(drop=True)
        
        # Merge 'nom' and 'Prenom' columns into a single column
        df['Nom et prénom'] = df['Prenom'] + ' ' + df['nom']
        
        # Drop the original 'nom' and 'Prenom' columns
        df = df.drop(columns=['nom', 'Prenom'])
        
        # Translate 'sexe' column from Arabic to French
        df['Sexe'] = df['Sexe'].replace(arabic_to_french)
        
        # Create a dictionary for the current DataFrame
        df_dict = df.set_index('Code Massar')['Sexe'].to_dict()
        
        # Store the dictionary in df_dicts
        df_dicts[f'df{i+1}'] = df_dict

    # Merge all dictionaries in df_dicts into a single dictionary
    merged_code_massar_gender = {k: v for dct in df_dicts.values() for k, v in dct.items()}

    # Create an empty list to store all extracted data
    all_data = []
    
    # Define the pattern to extract class and subclass from the file name
    pattern = r'^export_notesCC_([A-Z0-9]+)-([A-Z0-9]+)_'
    
    # Iterate over each uploaded file
    for file in uploaded_files:
        if file != selected_file:
            # Extract the file name
            file_name = file.name
            
            # Search for matches with the pattern in the file name
            match = re.search(pattern, file_name)
            
            if match:
                # Extract class and subclass from the matches
                classe = match.group(1)
                subclass = classe + "-" + match.group(2)
                
                # Read the Excel file
                df = pd.read_excel(file, skiprows=start_row-1, engine="openpyxl")
                
                # Extract specific data for each column
                code_massar = list(df[column_names[0]])
                names = list(df[column_names[1]])
                dn = list(df[column_names[2]])
                note_ctr1 = list(df[column_names[3]])
                note_ctr2 = list(df[column_names[4]])
                note_ctr3 = list(df[column_names[5]])
                note_act = list(df[column_names[6]])
                # Create a list of Sexe based on Code Massar using the dictionary
                sexe = [ merged_code_massar_gender.get(cm, None) for cm in code_massar ]
                
                # Store the data in a dictionary
                data_dict = {
                    'Code Massar': code_massar,
                    'Nom et prénom': names,
                    'Date Naissance': dn,
                    'Classe': [classe] * len(code_massar),
                    'Sub Classe': [subclass] * len(code_massar),
                    'Sexe': sexe,
                    'Note Ctrl 1': note_ctr1,
                    'Note Ctrl 2': note_ctr2,
                    'Note Ctrl 3': note_ctr3,
                    'Note Act Int': note_act
                }
                
                # Append the data dictionary to the list
                all_data.append(data_dict)
    
    # Concatenate all data dictionaries into a single DataFrame
    df_final = pd.concat([pd.DataFrame(data) for data in all_data], ignore_index=True)
    
    return df_final


def calculer_moyenne(df_final, pourcentage_ctrl, pourcentage_act_int):
    moyenne_list = []
    
    for i in range(len(df_final["Note Ctrl 1"])):
        if "Note Ctrl 2" not in df_final and "Note Ctrl 3" not in df_final:
            moyenne = ((np.array(df_final["Note Ctrl 1"][i]) * pourcentage_ctrl) + 
                       (np.array(df_final["Note Act Int"][i]) * pourcentage_act_int)) / 100
        elif "Note Ctrl 3" not in df_final:
            moyenne = (((np.array(df_final["Note Ctrl 1"][i]) + np.array(df_final["Note Ctrl 2"][i])) / 2) * 
                       pourcentage_ctrl + np.array(df_final["Note Act Int"][i]) * pourcentage_act_int) / 100
        else:
            moyenne = (((np.array(df_final["Note Ctrl 1"][i]) + np.array(df_final["Note Ctrl 2"][i]) + 
                         np.array(df_final["Note Ctrl 3"][i])) / 3) * pourcentage_ctrl + 
                       np.array(df_final["Note Act Int"][i]) * pourcentage_act_int) / 100
        
        moyenne_list.append(round(moyenne, 2))
    
    df_final["Moyenne"] = moyenne_list
    return df_final

def calculer_age(df_final):
    ages_list = []
    
    for date_naissance in df_final["Date Naissance"]:
        annee_actuelle = datetime.datetime.now().year
        age = annee_actuelle - int(date_naissance.split("-")[-1])
        ages_list.append(age)
    
    df_final["Age"] = ages_list
    return df_final



# Define the function to evaluate notes
def evaluer_notes(df_final):
    evaluations_list = []
    for moyenne in df_final["Moyenne"]:
        if moyenne >= 18:
            evaluations_list.append("Très bien")
        elif 15 <= moyenne < 18:
            evaluations_list.append("Bien")
        elif 12 <= moyenne < 15:
            evaluations_list.append("Assez bien")
        elif 10 <= moyenne < 12:
            evaluations_list.append("Passable")
        elif 7 <= moyenne < 10:
            evaluations_list.append("Médiocre")
        else:
            evaluations_list.append("Faible")
    df_final["Mention"] = evaluations_list
    return df_final

################################## 


#Requette 1: Age
def requette_1(df):
    st.subheader("Sous menu : Age")
    # Define subqueries for request 1
    sous_menus = {
        "Age": ['Répartition par l\'age', 'Répartition de l\'age par Classe', 'Répartition de l\'age par Sous Classe']
    }

    # Use option menu to select subquery
    if "Age" in sous_menus:
        sub_query = option_menu(None, sous_menus["Age"], orientation="horizontal",
                                     styles={
                                         #"container": {"white-space": "nowrap"}  # Empêcher le retour à la ligne pour les éléments
                                        "container": {"max-width": "100%", "white-space": "nowrap"}  # Définir une largeur maximale pour le conteneur et empêcher le retour à la ligne
                                     })
    else:
        st.write("No subqueries available for Age")


    # Define the main container for the page
    main_container = st.container()

    with main_container:
        if sub_query == 'Répartition par l\'age':
            with st.expander("Répartition par l'age", expanded=False):
                st.subheader("Répartition par l'age")
                count_age_df = df['Age'].value_counts().reset_index()
                count_age_df.columns = ['Age', 'Count']
                
                # Define columns with minimum padding
                col1, col2 = st.columns([2, 3])
                with col1:
                    #st.write(count_age_df)
                    use_container_width = True
                    st.dataframe(count_age_df, use_container_width=use_container_width)
                    #st.write(count_age_df, width=100)

                with col2:
                    use_container_width = True
                    # Adjust plot size
                    fig_count_age = px.bar(count_age_df, x='Age', y='Count', title='Count of Age', 
                                        labels={'Age': 'Age', 'Count': 'Count'}, color='Age',
                                        color_discrete_map={'Age': 'darkblue'})
                    # Set layout attributes for responsiveness
                    #fig_count_age.update_layout(width=400, height=450, autosize=True)
                    #st.plotly_chart(fig_count_age)
                    st.plotly_chart(fig_count_age, use_container_width=use_container_width)
                    
                                    
                #with col2:
                 #   fig_count_age = px.bar(count_age_df, x='Age', y='Count', title='Count of Age', 
                  #                      labels={'Age': 'Age', 'Count': 'Count'}, color='Age',
                   #                     color_discrete_map={'Age': 'darkblue'})
                   # st.plotly_chart(fig_count_age)
                


       
        elif sub_query == 'Répartition de l\'age par Classe':
            st.subheader("Répartition de l'age par Classe")
            # Filter data based on selected Classe
            classes = st.multiselect("Select Classe", df['Classe'].unique(), key="select_classe_requette_1")
            filtered_data = df[df['Classe'].isin(classes)]

            if set(classes) == set(df['Classe'].unique()):
                # Generate dataframe for all data
                count_age_by_classe_df = df.groupby(['Classe', 'Age']).size().reset_index(name='Count')

                with st.expander("All Classes", expanded=False):
                    st.write("All Classes:")
                    #st.write(count_age_by_classe_df)
                    
                    col1, col2 = st.columns([2, 3])
                    with col1:
                        use_container_width = True
                        #st.write(count_age_by_classe_df)
                        st.dataframe(count_age_by_classe_df, use_container_width=use_container_width)
                    with col2:
                        use_container_width = True
                        fig = px.bar(count_age_by_classe_df, 
                            x='Age', 
                            y='Count', 
                            color='Classe',
                            barmode='group',
                            title='Count of Age by Classe', 
                            labels={'Age': 'Age', 'Count': 'Count', 'Classe': 'Classe'},
                            color_discrete_map={'Classe': 'darkred'})
                        #st.plotly_chart(fig)
                        st.plotly_chart(fig, use_container_width=use_container_width)
            else:
                for classe in classes:
                    count_age_by_classe_df = filtered_data[filtered_data['Classe'] == classe].groupby('Age').size().reset_index(name='Count')

                    with st.expander(f"Classe: {classe}", expanded=False):
                        st.write(f"Classe: {classe}")
                        #st.write(count_age_by_classe_df)

                        col1, col2 = st.columns([2, 3])

                        with col1:
                            use_container_width = True
                            #st.write(count_age_by_classe_df)
                            st.dataframe(count_age_by_classe_df, use_container_width=use_container_width)

                        with col2:
                            use_container_width = True
                            fig_age_by_classe = px.bar(count_age_by_classe_df, x='Age', y='Count', 
                                                    title=f'Count of Age for {classe}', 
                                                    labels={'Age': 'Age', 'Count': 'Count'}, color='Age',
                                                    color_discrete_map={'Age': 'darkblue'})
                            #st.plotly_chart(fig_age_by_classe)
                            st.plotly_chart(fig_age_by_classe, use_container_width=use_container_width)


                
        elif sub_query == 'Répartition de l\'age par Sous Classe':
            st.subheader("Répartition de l'age par Sous Classe")
            # Filter data based on selected Sub Classe
            sub_classes = st.multiselect("Select Sub Classe", df['Sub Classe'].unique(), key="select_sub_classe_requette_1")
            filtered_data = df[df['Sub Classe'].isin(sub_classes)]

            if set(sub_classes) == set(df['Sub Classe'].unique()):
                # Generate dataframe for all data
                count_age_by_subclasse_df = df.groupby(['Sub Classe', 'Age']).size().reset_index(name='Count')

                with st.expander("All Sub Classes", expanded=False):
                    st.write("All Sub Classes:")
                    
                    col1, col2 = st.columns([2, 3])
                    with col1:
                        use_container_width = True
                        #st.write(count_age_by_subclasse_df)
                        st.dataframe(count_age_by_subclasse_df, use_container_width=use_container_width)
                        
                    with col2:
                        use_container_width = True
                        fig = px.bar(count_age_by_subclasse_df, 
                                    x='Age', 
                                    y='Count', 
                                    color='Sub Classe',
                                    barmode='group',
                                    title='Count of Age by Sub Classe', 
                                    labels={'Age': 'Age', 'Count': 'Count', 'Sub Classe': 'Sub Classe'},
                                    color_discrete_map={'Sub Classe': 'darkgreen'})
                        #st.plotly_chart(fig)
                        st.plotly_chart(fig, use_container_width=use_container_width)
            else:
                for sub_classe in sub_classes:
                    count_age_by_sub_classe_df = filtered_data[filtered_data['Sub Classe'] == sub_classe].groupby('Age').size().reset_index(name='Count')

                    with st.expander(f"Sub Classe: {sub_classe}", expanded=False):
                        st.write(f"Sub Classe: {sub_classe}")
                        
                        col1, col2 = st.columns([2, 3])

                        with col1:
                            use_container_width = True
                            #st.write(count_age_by_sub_classe_df)
                            st.dataframe(count_age_by_sub_classe_df, use_container_width=use_container_width)

                        with col2:
                            use_container_width = True
                            fig_age_by_sub_classe = px.bar(count_age_by_sub_classe_df, x='Age', y='Count', 
                                                        title=f'Count of Age for {sub_classe}', 
                                                        labels={'Age': 'Age', 'Count': 'Count'}, color='Age',
                                                        color_discrete_map={'Age': 'darkblue'})
                            #st.plotly_chart(fig_age_by_sub_classe)
                            st.plotly_chart(fig_age_by_sub_classe, use_container_width=use_container_width)
                            



# Requette 2: Sexe
def requette_2(df):
    st.subheader("Sous menu : Sexe")
    # Define subqueries for request 1
    sous_menus = {
        "Sexe": ['Répartition par Sexe', 'Répartition du Sexe par Classe', 'Répartition du Sexe par Sous Classe']
    }

    # Use option menu to select subquery
    if "Sexe" in sous_menus:
        sub_query = option_menu(None, sous_menus["Sexe"], orientation="horizontal",
                                     styles={
                                         #"container": {"white-space": "nowrap"}  # Empêcher le retour à la ligne pour les éléments
                                        "container": {"max-width": "100%", "white-space": "nowrap"}  # Définir une largeur maximale pour le conteneur et empêcher le retour à la ligne
                                     })
    else:
        st.write("No subqueries available for Sexe")
        
        
    main_container = st.container()
    with main_container:
        if sub_query == 'Répartition par Sexe':
            st.subheader("Répartition par Sexe")
            with st.expander("Répartition par Sexe", expanded=False):
                count_sexe_df = df['Sexe'].value_counts().reset_index()
                count_sexe_df.columns = ['Sexe', 'Count']
                
                # Define columns with minimum padding
                # Define columns with adjusted width
                #col1, col2, col3 = st.columns([3, 3, 6])
                col1, col2 = st.columns([2, 3])
                col3 = st.columns([8])[0]  # Full width for the third column
                
            
                with col1:
                    use_container_width = True
                    #st.write(count_sexe_df)
                    st.dataframe(count_sexe_df, use_container_width=use_container_width)

                with col2:
                    use_container_width = True
                    fig = px.bar(count_sexe_df, x='Sexe', y='Count', title='Count of Sexe',
                                labels={'Sexe': 'Sexe', 'Count': 'Count'}, color='Sexe',
                                color_discrete_map={'Sexe': 'darkblue'})
                    fig.update_layout(showlegend=True)
                    #st.plotly_chart(fig)
                    st.plotly_chart(fig, use_container_width=use_container_width)
            
                with col3:
                    use_container_width = True
                    count_sexe_df['Percentage'] = (count_sexe_df['Count'] / count_sexe_df['Count'].sum()) * 100
                    fig_pie = px.pie(count_sexe_df, values='Percentage', names='Sexe', title='Percentage Distribution of Sexe')
                    #st.plotly_chart(fig_pie)
                    st.plotly_chart(fig_pie, use_container_width=use_container_width)


        elif sub_query == 'Répartition du Sexe par Classe':
            st.subheader("Répartition du Sexe par Classe")

            # Filter data based on selected Classe
            classes = st.multiselect("Select Classe", df['Classe'].unique())
            filtered_data = df[df['Classe'].isin(classes)]

            if set(classes) == set(df['Classe'].unique()):
                # Generate dataframe for all data
                count_sexe_by_classe_df = df.groupby(['Classe', 'Sexe']).size().reset_index(name='Count')
                count_sexe_by_classe_df['Percentage'] = (count_sexe_by_classe_df['Count'] / count_sexe_by_classe_df['Count'].sum()) * 100
                count_sexe_by_classe_df['Percentage'] = count_sexe_by_classe_df['Percentage'].round(2)

                with st.expander("All Classes", expanded=False):
                    st.write("All Classes:")
                    #col1, col2, col3 = st.columns([1, 1, 1])
                    col1, col2 = st.columns([2, 3])
                    col3 = st.columns([8])[0]  # Full width for the third column
                    with col1:
                        use_container_width = True
                        #st.write(count_sexe_by_classe_df)
                        st.dataframe(count_sexe_by_classe_df, use_container_width=use_container_width)
                    with col2:
                        use_container_width = True
                        fig_all_classes = px.bar(count_sexe_by_classe_df, x='Sexe', y='Count', color='Classe',
                                                barmode='group', title='Count of Sexe by Classe',
                                                labels={'Sexe': 'Sexe', 'Count': 'Count', 'Classe': 'Classe'},
                                                color_discrete_map={'Classe': 'darkred'})
                        #st.plotly_chart(fig_all_classes)
                        st.plotly_chart(fig_all_classes, use_container_width=use_container_width)
                        
                    with col3:
                        use_container_width = True
                        count_sexe_by_classe_df['Percentage'] = (count_sexe_by_classe_df['Count'] / count_sexe_by_classe_df['Count'].sum()) * 100
                        fig_pie = px.pie(count_sexe_by_classe_df, values='Percentage', names='Sexe', title=f'Percentage Distribution of Sexe for all classes')
                        #st.plotly_chart(fig_pie)
                        st.plotly_chart(fig_pie, use_container_width=use_container_width)
            else:
                for classe in classes:
                    count_sexe_by_classe_df = filtered_data[filtered_data['Classe'] == classe]['Sexe'].value_counts().reset_index()
                    count_sexe_by_classe_df.columns = ['Sexe', 'Count']
                    count_sexe_by_classe_df['Percentage'] = (count_sexe_by_classe_df['Count'] / count_sexe_by_classe_df['Count'].sum()) * 100
                    count_sexe_by_classe_df['Percentage'] = count_sexe_by_classe_df['Percentage'].round(2)

                    with st.expander(f"Classe: {classe}", expanded=False):
                        st.write(f"Classe: {classe}")

                        #col1, col2, col3 = st.columns([1, 1, 1])
                        col1, col2 = st.columns([2, 3])
                        col3 = st.columns([8])[0]  # Full width for the third column

                        with col1:
                            use_container_width = True
                            #st.write(count_sexe_by_classe_df)
                            st.dataframe(count_sexe_by_classe_df, use_container_width=use_container_width)

                        with col2:
                            use_container_width = True
                            fig_bar = px.bar(count_sexe_by_classe_df, x='Sexe', y='Count', color='Sexe',
                                            barmode='group', title=f'Count of Sexe for {classe}',
                                            labels={'Sexe': 'Sexe', 'Count': 'Count'},
                                            color_discrete_map={'Sexe': 'darkblue'})
                            #st.plotly_chart(fig_bar)
                            st.plotly_chart(fig_bar, use_container_width=use_container_width)

                        with col3:
                            use_container_width = True
                            count_sexe_by_classe_df['Percentage'] = (count_sexe_by_classe_df['Count'] / count_sexe_by_classe_df['Count'].sum()) * 100
                            fig_pie = px.pie(count_sexe_by_classe_df, values='Percentage', names='Sexe', title=f'Percentage Distribution of Sexe for {classe}')
                            #st.plotly_chart(fig_pie)
                            st.plotly_chart(fig_pie, use_container_width=use_container_width)
                            

        
        elif sub_query == 'Répartition du Sexe par Sous Classe':
            st.subheader("Répartition du Sexe par Sous Classe")
            # Filter data based on selected Sub Classe
            sub_classes = st.multiselect("Select Sub Classe", df['Sub Classe'].unique())
            filtered_data = df[df['Sub Classe'].isin(sub_classes)]

            if set(sub_classes) == set(df['Sub Classe'].unique()):
                # Generate dataframe for all data
                count_sexe_by_sub_classe_df = df.groupby(['Sub Classe', 'Sexe']).size().reset_index(name='Count')
                count_sexe_by_sub_classe_df['Percentage'] = (count_sexe_by_sub_classe_df['Count'] / count_sexe_by_sub_classe_df['Count'].sum()) * 100
                count_sexe_by_sub_classe_df['Percentage'] = count_sexe_by_sub_classe_df['Percentage'].round(2)

                with st.expander("All Sub Classes", expanded=False):
                    st.write("All Sub Classes:")
                    #col1, col2, col3 = st.columns([1, 1, 1])
                    col1, col2 = st.columns([2, 3])
                    col3 = st.columns([8])[0]  # Full width for the third column
                    with col1:
                        use_container_width = True
                        #st.write(count_sexe_by_sub_classe_df)
                        st.dataframe(count_sexe_by_sub_classe_df, use_container_width=use_container_width)
                    with col2:
                        use_container_width = True
                        fig_all_sub_classes = px.bar(count_sexe_by_sub_classe_df, x='Sexe', y='Count', color='Sub Classe',
                                                    barmode='group', title='Count of Sexe by Sub Classe',
                                                    labels={'Sexe': 'Sexe', 'Count': 'Count', 'Sub Classe': 'Sub Classe'},
                                                    color_discrete_map={'Sub Classe': 'darkgreen'})
                        #st.plotly_chart(fig_all_sub_classes)
                        st.plotly_chart(fig_all_sub_classes, use_container_width=use_container_width)
                    with col3:
                        
                        count_sexe_by_sub_classe_df['Percentage'] = (count_sexe_by_sub_classe_df['Count'] / count_sexe_by_sub_classe_df['Count'].sum()) * 100
                        fig_pie = px.pie(count_sexe_by_sub_classe_df, values='Percentage', names='Sexe', title='Percentage Distribution of Sexe for all sub-classes')
                        #st.plotly_chart(fig_pie)
                        
            else:
                for sub_classe in sub_classes:
                    count_sexe_by_sub_classe_df = filtered_data[filtered_data['Sub Classe'] == sub_classe]['Sexe'].value_counts().reset_index()
                    count_sexe_by_sub_classe_df.columns = ['Sexe', 'Count']
                    count_sexe_by_sub_classe_df['Percentage'] = (count_sexe_by_sub_classe_df['Count'] / count_sexe_by_sub_classe_df['Count'].sum()) * 100
                    count_sexe_by_sub_classe_df['Percentage'] = count_sexe_by_sub_classe_df['Percentage'].round(2)

                    with st.expander(f"Sub Classe: {sub_classe}", expanded=False):
                        st.write(f"Sub Classe: {sub_classe}")

                        #col1, col2, col3 = st.columns([1, 1, 1])
                        col1, col2 = st.columns([1, 2])
                        col3 = st.columns([8])[0]  # Full width for the third column

                        with col1:
                            st.write(count_sexe_by_sub_classe_df)

                        with col2:
                            fig_bar = px.bar(count_sexe_by_sub_classe_df, x='Sexe', y='Count', color='Sexe',
                                            barmode='group', title=f'Count of Sexe for {sub_classe}',
                                            labels={'Sexe': 'Sexe', 'Count': 'Count'},
                                            color_discrete_map={'Sexe': 'darkblue'})
                            st.plotly_chart(fig_bar)

                        with col3:
                            count_sexe_by_sub_classe_df['Percentage'] = (count_sexe_by_sub_classe_df['Count'] / count_sexe_by_sub_classe_df['Count'].sum()) * 100
                            fig_pie = px.pie(count_sexe_by_sub_classe_df, values='Percentage', names='Sexe', title=f'Percentage Distribution of Sexe for {sub_classe}')
                            st.plotly_chart(fig_pie)




# Requette 3: Nombre d'élèves
def requette_3(df):
    st.subheader("Sous menu : Nombre d'élèves")
    # Define subqueries for request 1
    sous_menus = {
        "Nombre d'élèves": ['Nombre d\'élèves par Classe', 'Nombre d\'élèves par Sous Classe']
    }

    # Use option menu to select subquery
    if "Nombre d'élèves" in sous_menus:
        sub_query = option_menu(None, sous_menus["Nombre d'élèves"], orientation="horizontal",
                                     styles={
                                         #"container": {"white-space": "nowrap"}  # Empêcher le retour à la ligne pour les éléments
                                        "container": {"max-width": "100%", "white-space": "nowrap"}  # Définir une largeur maximale pour le conteneur et empêcher le retour à la ligne
                                     })
    else:
        st.write("No subqueries available for Nombre d'élèves")
    
    
    
    main_container = st.container()
    with main_container:
        if sub_query == 'Nombre d\'élèves par Classe':
            st.subheader("Nombre d'élèves par Classe")

            # Filter data based on selected Classe
            classes = st.multiselect("Select Classe", df['Classe'].unique())
            filtered_data = df[df['Classe'].isin(classes)]

            if filtered_data.empty:
                st.warning("No data available for the selected class(es).")
            else:
                all_classes = set(df['Classe'].unique())
                if set(classes) == all_classes:
                    # Generate dataframe for all classes
                    count_by_classe_df = df['Classe'].value_counts().reset_index()
                    count_by_classe_df.columns = ['Classe', 'Count']

                    with st.expander("Count by Classe", expanded=False):
                        st.write("All Classes:")

                        col1, col2 = st.columns([2, 3])
                        with col1:
                            use_container_width = True
                            st.dataframe(count_by_classe_df, use_container_width=use_container_width)
                        with col2:
                            use_container_width = True
                            fig_bar = px.bar(count_by_classe_df, x='Classe', y='Count', 
                                            title='Count of Students by Classe',
                                            color='Classe', 
                                            color_discrete_sequence=px.colors.qualitative.Set1)
                            fig_bar.update_layout(showlegend=True)
                            st.plotly_chart(fig_bar, use_container_width=use_container_width)
                else:
                    for classe in classes:
                        count_by_classe_df = filtered_data[filtered_data['Classe'] == classe]['Classe'].value_counts().reset_index()
                        count_by_classe_df.columns = ['Classe', 'Count']

                        with st.expander(f"Count by Classe: {classe}", expanded=False):
                            st.write(f"Classe: {classe}")

                            col1, col2 = st.columns([2, 3])

                            with col1:
                                use_container_width = True
                                st.dataframe(count_by_classe_df, use_container_width=use_container_width)

                            with col2:
                                use_container_width = True
                                fig_bar = px.bar(count_by_classe_df, x='Classe', y='Count', 
                                                title=f'Count of Students for {classe}',
                                                color='Classe', 
                                                color_discrete_sequence=px.colors.qualitative.Set1)
                                fig_bar.update_layout(showlegend=True)
                                st.plotly_chart(fig_bar, use_container_width=use_container_width)

        elif sub_query == 'Nombre d\'élèves par Sous Classe':
            st.subheader("Nombre d'élèves par Sous Classe")

            # Filter data based on selected Sub Classe
            sub_classes = st.multiselect("Select Sub Classe", df['Sub Classe'].unique())
            filtered_data = df[df['Sub Classe'].isin(sub_classes)]

            if filtered_data.empty:
                st.warning("No data available for the selected sub class(es).")
            else:
                all_sub_classes = set(df['Sub Classe'].unique())
                if set(sub_classes) == all_sub_classes:
                    # Generate dataframe for all sub classes
                    count_by_subclasse_df = df['Sub Classe'].value_counts().reset_index()
                    count_by_subclasse_df.columns = ['Sub Classe', 'Count']

                    with st.expander("Count by Sub Classe", expanded=False):
                        st.write("All Sub Classes:")

                        col1, col2 = st.columns([2, 3])
                        with col1:
                            use_container_width = True
                            st.dataframe(count_by_subclasse_df, use_container_width=use_container_width)
                        with col2:
                            use_container_width = True
                            fig_bar_subclasse = px.bar(count_by_subclasse_df, x='Sub Classe', y='Count', 
                                                    title='Count of Students by Sub Classe',
                                                    color='Sub Classe', 
                                                    color_discrete_sequence=px.colors.qualitative.Set2)
                            fig_bar_subclasse.update_layout(showlegend=True)
                            st.plotly_chart(fig_bar_subclasse, use_container_width=use_container_width)
                else:
                    for sub_classe in sub_classes:
                        count_by_subclasse_df = filtered_data[filtered_data['Sub Classe'] == sub_classe]['Sub Classe'].value_counts().reset_index()
                        count_by_subclasse_df.columns = ['Sub Classe', 'Count']

                        with st.expander(f"Count by Sub Classe: {sub_classe}", expanded=False):
                            st.write(f"Sub Classe: {sub_classe}")

                            col1, col2 = st.columns([2, 3])

                            with col1:
                                use_container_width = True
                                st.dataframe(count_by_subclasse_df, use_container_width=use_container_width)

                            with col2:
                                use_container_width = True
                                fig_bar_subclasse = px.bar(count_by_subclasse_df, x='Sub Classe', y='Count', 
                                                        title=f'Count of Students for {sub_classe}',
                                                        color='Sub Classe', 
                                                        color_discrete_sequence=px.colors.qualitative.Set2)
                                fig_bar_subclasse.update_layout(showlegend=True)
                                st.plotly_chart(fig_bar_subclasse, use_container_width=use_container_width)






# Requette 4: Notes Controle 1
def requette_4(df):
    st.subheader("Sous menu : Controle 1")
    # Define subqueries for request 1
    sous_menus = {
        "Controle 1": ['Valeur Maximale, valeur minimale et la moyenne dans chaque sous classe', 'Eleves ayant note au dessus et au dessous la moyenne par Classe', 'Eleves ayant note au dessus et au dessous la moyenne par Sous Classe']
    }

    # Use option menu to select subquery
    if "Controle 1" in sous_menus:
        sub_query = option_menu(None, sous_menus["Controle 1"], orientation="horizontal",
                                     styles={
                                         #"container": {"white-space": "nowrap"}  # Empêcher le retour à la ligne pour les éléments
                                        "container": {"max-width": "100%", "white-space": "nowrap"}  # Définir une largeur maximale pour le conteneur et empêcher le retour à la ligne
                                     })
    else:
        st.write("No subqueries available for Controle 1")
    
    
    
    main_container = st.container()
    with main_container:
        if sub_query == 'Valeur Maximale, valeur minimale et la moyenne dans chaque sous classe':
            st.subheader("Valeur Maximale, valeur minimale et la moyenne dans chaque sous classe")

            # Select subclasses
            selected_subclasses = st.multiselect("Select Sub Classe", df['Sub Classe'].unique())

            # Filter data based on selected subclasses
            filtered_data = df[df['Sub Classe'].isin(selected_subclasses)]

            # If all subclasses are selected
            if set(selected_subclasses) == set(df['Sub Classe'].unique()):
                subclasse_stats_df = df.groupby('Sub Classe')['Note Ctrl 1'].agg([('Max Note', 'max'), ('Min Note', 'min'), ('Moyenne', 'mean')]).reset_index()
                subclasse_stats_df['Moyenne'] = subclasse_stats_df['Moyenne'].round(2)

                # Displaying dataframe and plot for all subclasses
                with st.expander("Max Note, Min Note, and Moyenne of Note Ctrl 1 for All Sub Classes", expanded=False):
                    col1, col2 = st.columns([2, 3])
                    with col1:
                        use_container_width = True
                        #st.write(subclasse_stats_df)
                        st.dataframe(subclasse_stats_df, use_container_width=use_container_width)
                    with col2:
                        use_container_width = True
                        fig = px.bar(subclasse_stats_df, x='Sub Classe', y=['Max Note', 'Min Note', 'Moyenne'],
                                    title='Max Note, Min Note, and Moyenne of Note Ctrl 1 for Each Sub Classe',
                                    labels={'value': 'Note', 'variable': 'Statistic'},
                                    barmode='group')
                        fig.update_layout(xaxis_title='Sub Classe', yaxis_title='Note')
                        #st.plotly_chart(fig)
                        st.plotly_chart(fig, use_container_width=use_container_width)

            else:
                # Display dataframe and plot for each selected subclass
                for subclass in selected_subclasses:
                    subclass_data = filtered_data[filtered_data['Sub Classe'] == subclass]
                    subclass_stats_df = subclass_data.agg({'Note Ctrl 1': ['max', 'min', 'mean']}).reset_index()
                    subclass_stats_df.columns = ['Statistique', 'Valeur']
                    subclass_stats_df['Valeur'] = subclass_stats_df['Valeur'].round(2)

                    with st.expander(f"Max Note, Min Note, and Moyenne of Note Ctrl 1 for Sub Classe: {subclass}", expanded=False):
                        col1, col2 = st.columns([2, 3])
                        with col1:
                            use_container_width = True
                            #st.write(subclass_stats_df)
                            st.dataframe(subclass_stats_df, use_container_width=use_container_width)
                            
                        with col2:
                            use_container_width = True
                            fig = px.bar(subclass_stats_df, x='Statistique', y='Valeur',
                                        title=f'Max Note, Min Note, and Moyenne of Note Ctrl 1 for Sub Classe: {subclass}',
                                        labels={'Valeur': 'Note', 'Statistique': 'Statistic'},
                                        color_discrete_sequence=px.colors.qualitative.Set1)
                            fig.update_layout(xaxis_title='Statistic', yaxis_title='Note')
                            #st.plotly_chart(fig)
                            st.plotly_chart(fig, use_container_width=use_container_width)

        elif sub_query == 'Eleves ayant note au dessus et au dessous la moyenne par Classe':
            st.subheader("Eleves ayant note au dessus et au dessous la moyenne par Classe")

            # Select classes
            selected_classes = st.multiselect("Select Classe", df['Classe'].unique())

            # Filter data based on selected classes
            filtered_data = df[df['Classe'].isin(selected_classes)]

            if set(selected_classes) == set(df['Classe'].unique()):
                # Calculate total counts of Note Ctrl 1 >= 10 and < 10 for each class
                total_counts_classe_df = df.groupby('Classe')['Note Ctrl 1'].agg([('Total >= 10', lambda x: (x >= 10).sum()), ('Total < 10', lambda x: (x < 10).sum())]).reset_index()

                # Calculate total counts for each class
                total_counts_classe_df['Total'] = total_counts_classe_df['Total >= 10'] + total_counts_classe_df['Total < 10']

                # Calculate percentage for each category
                total_counts_classe_df['Percentage >= 10'] = (total_counts_classe_df['Total >= 10'] / total_counts_classe_df['Total']) * 100
                total_counts_classe_df['Percentage < 10'] = (total_counts_classe_df['Total < 10'] / total_counts_classe_df['Total']) * 100

                # Round the percentage values to two decimal places
                total_counts_classe_df['Percentage >= 10'] = total_counts_classe_df['Percentage >= 10'].round(2)
                total_counts_classe_df['Percentage < 10'] = total_counts_classe_df['Percentage < 10'].round(2)

                # Display the DataFrame
                with st.expander("Eleves ayant note au dessus et au dessous la moyenne par Classe", expanded=False):
                    col1, col2 = st.columns([2, 3])
                    with col1:
                        use_container_width = True
                        #st.write(total_counts_classe_df)
                        st.dataframe(total_counts_classe_df, use_container_width=use_container_width)

                    with col2:
                        use_container_width = True
                        fig_bar = px.bar(total_counts_classe_df, x='Classe', y=['Total >= 10', 'Total < 10'],
                                        title='Total Counts of Note Ctrl 1 >= 10 and <= 10 for Each Class',
                                        labels={'value': 'Count', 'variable': 'Note Ctrl 1'},
                                        color_discrete_map={'Total >= 10': 'green', 'Total < 10': 'red'},
                                        barmode='group')
                        fig_bar.update_layout(xaxis_title='Classe', yaxis_title='Count')
                        #st.plotly_chart(fig_bar)
                        st.plotly_chart(fig_bar, use_container_width=use_container_width)

                        colors = ['green', 'red']
                        
                        # Prepare DataFrame with required columns
                        total_percentage_classe_moyenne_df =  total_counts_classe_df[['Classe','Percentage >= 10','Percentage < 10']]

                        # Plotting Sunburst chart with legend
                        fig = px.sunburst(total_percentage_classe_moyenne_df, path=['Classe', 'Percentage >= 10', 'Percentage < 10'], 
                                title='Percentage Moyenne >= 10 and Moyenne < 10 in each Classe',
                                labels={'Percentage >= 10': 'Percentage >= 10', 'Percentage < 10': 'Percentage < 10'})
                        #st.plotly_chart(fig)
                        st.plotly_chart(fig, use_container_width=use_container_width)
                        
                        

            else:
                for classe in selected_classes:
                    total_counts_classe_df = filtered_data[filtered_data['Classe'] == classe].groupby('Classe')['Note Ctrl 1'].agg([('Total >= 10', lambda x: (x >= 10).sum()), ('Total < 10', lambda x: (x < 10).sum())]).reset_index()

                    with st.expander(f"Eleves ayant note au dessus et au dessous la moyenne pour la classe: {classe}", expanded=False):
                        col1, col2 = st.columns([2, 3])
                        with col1:
                            use_container_width = True
                            #st.write(total_counts_classe_df)
                            st.dataframe(total_counts_classe_df, use_container_width=use_container_width)

                        with col2:
                            use_container_width = True
                            fig_bar = px.bar(total_counts_classe_df, x='Classe', y=['Total >= 10', 'Total < 10'],
                                            title=f'Total Counts of Note Ctrl 1 >= 10 and <= 10 for Classe: {classe}',
                                            labels={'value': 'Count', 'variable': 'Note Ctrl 1'},
                                            color_discrete_map={'Total >= 10': 'green', 'Total < 10': 'red'},
                                            barmode='group')
                            fig_bar.update_layout(xaxis_title='Classe', yaxis_title='Count')
                            #st.plotly_chart(fig_bar)
                            st.plotly_chart(fig_bar, use_container_width=use_container_width)

                            colors = ['green', 'red']

                            # Data for current class
                            labels = ["Percentage >= 10", "Percentage < 10"]
                            values = [(total_counts_classe_df['Total >= 10'].iloc[0] / (total_counts_classe_df['Total >= 10'].iloc[0] + total_counts_classe_df['Total < 10'].iloc[0])) * 100, (total_counts_classe_df['Total < 10'].iloc[0] / (total_counts_classe_df['Total >= 10'].iloc[0] + total_counts_classe_df['Total < 10'].iloc[0])) * 100]

                            # Create pie chart for current class with custom colors
                            fig_pie = px.pie(names=labels, values=values, title=f"Class: {classe}",
                                            color_discrete_sequence=colors)
                            #st.plotly_chart(fig_pie)
                            st.plotly_chart(fig_pie, use_container_width=use_container_width)
                            

        elif sub_query == 'Eleves ayant note au dessus et au dessous la moyenne par Sous Classe':
            st.subheader("Eleves ayant note au dessus et au dessous la moyenne par Sous Classe")

            # Select subclasses
            selected_subclasses = st.multiselect("Select Sub Classe", df['Sub Classe'].unique())

            # Filter data based on selected subclasses
            filtered_data = df[df['Sub Classe'].isin(selected_subclasses)]

            if set(selected_subclasses) == set(df['Sub Classe'].unique()):
                # Calculate total counts of Note Ctrl 1 >= 10 and < 10 for each sub class
                total_counts_subclasse_df = df.groupby('Sub Classe')['Note Ctrl 1'].agg([('Total >= 10', lambda x: (x >= 10).sum()), ('Total < 10', lambda x: (x < 10).sum())]).reset_index()

                # Calculate the total number of students for each sub class
                total_counts_subclasse_df['Total'] = total_counts_subclasse_df['Total >= 10'] + total_counts_subclasse_df['Total < 10']

                # Calculate the percentage for each category
                total_counts_subclasse_df['Percentage >= 10'] = (total_counts_subclasse_df['Total >= 10'] / total_counts_subclasse_df['Total']) * 100
                total_counts_subclasse_df['Percentage < 10'] = (total_counts_subclasse_df['Total < 10'] / total_counts_subclasse_df['Total']) * 100

                # Round the percentage values
                total_counts_subclasse_df['Percentage >= 10'] = total_counts_subclasse_df['Percentage >= 10'].round()
                total_counts_subclasse_df['Percentage < 10'] = total_counts_subclasse_df['Percentage < 10'].round()

                # Display the DataFrame
                with st.expander("Eleves ayant note au dessus et au dessous la moyenne par Sous Classe", expanded=False):
                    col1, col2 = st.columns([2, 3])
                    with col1:
                        use_container_width = True
                        st.dataframe(total_counts_subclasse_df, use_container_width=use_container_width)
                        #st.write(total_counts_subclasse_df)

                    with col2:
                        use_container_width = True
                        fig_bar = px.bar(total_counts_subclasse_df, x='Sub Classe', y=['Total >= 10', 'Total < 10'],
                                        title='Total Counts of Note Ctrl 1 >= 10 and <= 10 for Each Sub Classe',
                                        labels={'value': 'Count', 'variable': 'Note Ctrl 1'},
                                        color_discrete_map={'Total >= 10': 'green', 'Total < 10': 'red'},
                                        barmode='group')
                        fig_bar.update_layout(xaxis_title='Sub Classe', yaxis_title='Count')
                        #st.plotly_chart(fig_bar)
                        st.plotly_chart(fig_bar, use_container_width=use_container_width)
                        

                        colors = ['green', 'red']
                        
                        # Prepare DataFrame with required columns
                        total_percentage_sub_classe_moyenne_df = total_counts_subclasse_df[['Sub Classe','Percentage >= 10','Percentage < 10']]

                        # Plotting Sunburst chart with legend
                        fig = px.sunburst(total_percentage_sub_classe_moyenne_df, path=['Sub Classe', 'Percentage >= 10', 'Percentage < 10'], 
                                title='Percentage Moyenne >= 10 and Moyenne < 10 in each Classe',
                                labels={'Percentage >= 10': 'Percentage >= 10', 'Percentage < 10': 'Percentage < 10'})
                        #st.plotly_chart(fig)
                        st.plotly_chart(fig, use_container_width=use_container_width)
                        


            else:
                for subclass in selected_subclasses:
                    total_counts_subclasse_df = filtered_data[filtered_data['Sub Classe'] == subclass].groupby('Sub Classe')['Note Ctrl 1'].agg([('Total >= 10', lambda x: (x >= 10).sum()), ('Total < 10', lambda x: (x < 10).sum())]).reset_index()

                    with st.expander(f"Eleves ayant note au dessus et au dessous la moyenne par Sous Classe: {subclass}", expanded=False):
                        col1, col2 = st.columns([2, 3])
                        with col1:
                            use_container_width = True
                            st.dataframe(total_counts_subclasse_df, use_container_width=use_container_width)
                            #st.write(total_counts_subclasse_df)

                        with col2:
                            use_container_width = True
                            fig_bar = px.bar(total_counts_subclasse_df, x='Sub Classe', y=['Total >= 10', 'Total < 10'],
                                            title=f'Total Counts of Note Ctrl 1 >= 10 and <= 10 for Sous Classe: {subclass}',
                                            labels={'value': 'Count', 'variable': 'Note Ctrl 1'},
                                            color_discrete_map={'Total >= 10': 'green', 'Total < 10': 'red'},
                                            barmode='group')
                            fig_bar.update_layout(xaxis_title='Sub Classe', yaxis_title='Count')
                            #st.plotly_chart(fig_bar)
                            st.plotly_chart(fig_bar, use_container_width=use_container_width)

                            colors = ['green', 'red']

                            # Data for current sub class
                            labels = ["Percentage >= 10", "Percentage < 10"]
                            values = [(total_counts_subclasse_df['Total >= 10'].iloc[0] / (total_counts_subclasse_df['Total >= 10'].iloc[0] + total_counts_subclasse_df['Total < 10'].iloc[0])) * 100, (total_counts_subclasse_df['Total < 10'].iloc[0] / (total_counts_subclasse_df['Total >= 10'].iloc[0] + total_counts_subclasse_df['Total < 10'].iloc[0])) * 100]

                            # Create pie chart for current sub class with custom colors
                            fig_pie = px.pie(names=labels, values=values, title=f"Sub Classe: {subclass}",
                                            color_discrete_sequence=colors)
                            #st.plotly_chart(fig_pie)
                            st.plotly_chart(fig_pie, use_container_width=use_container_width)



# Requette 5: Notes Moyenne
def requette_5(df):
    st.subheader("Sous menu : Moyenne")
    # Define subqueries for request 1
    sous_menus = {
        "Moyenne": ['Valeur Maximale, valeur minimale et la moyenne dans chaque sous classe', 'Eleves ayant note au dessus et au dessous la moyenne par Classe', 'Eleves ayant note au dessus et au dessous la moyenne par Sous Classe']
    }

    # Use option menu to select subquery
    if "Moyenne" in sous_menus:
        sub_query = option_menu(None, sous_menus["Moyenne"], orientation="horizontal",
                                     styles={
                                         #"container": {"white-space": "nowrap"}  # Empêcher le retour à la ligne pour les éléments
                                        "container": {"max-width": "100%", "white-space": "nowrap"}  # Définir une largeur maximale pour le conteneur et empêcher le retour à la ligne
                                     })
    else:
        st.write("No subqueries available for Moyenne")
    
    
    
    
    main_container = st.container()
    with main_container:
        if sub_query == 'Valeur Maximale, valeur minimale et la moyenne dans chaque sous classe':
            st.subheader("Valeur Maximale, valeur minimale et la moyenne dans chaque sous classe")

            # Select subclasses
            selected_subclasses = st.multiselect("Select Sub Classe", df['Sub Classe'].unique())

            # Filter data based on selected subclasses
            filtered_data = df[df['Sub Classe'].isin(selected_subclasses)]

            # If all subclasses are selected
            if set(selected_subclasses) == set(df['Sub Classe'].unique()):
                subclasse_stats_df = df.groupby('Sub Classe')['Moyenne'].agg([('Max Note', 'max'), ('Min Note', 'min'), ('Moyenne', 'mean')]).reset_index()
                subclasse_stats_df['Moyenne'] = subclasse_stats_df['Moyenne'].round(2)

                # Displaying dataframe and plot for all subclasses
                with st.expander("Max Note, Min Note, and Moyenne of Note Ctrl 1 for All Sub Classes", expanded=False):
                    col1, col2 = st.columns([2, 3])
                    with col1:
                        use_container_width = True
                        st.dataframe(subclasse_stats_df, use_container_width=use_container_width)
                        #st.write(subclasse_stats_df)
                    with col2:
                        use_container_width = True
                        fig = px.bar(subclasse_stats_df, x='Sub Classe', y=['Max Note', 'Min Note', 'Moyenne'],
                                    title='Max Note, Min Note, and Moyenne of Note Ctrl 1 for Each Sub Classe',
                                    labels={'value': 'Note', 'variable': 'Statistic'},
                                    barmode='group')
                        fig.update_layout(xaxis_title='Sub Classe', yaxis_title='Note')
                        #st.plotly_chart(fig)
                        st.plotly_chart(fig, use_container_width=use_container_width)
                        
            else:
                # Display dataframe and plot for each selected subclass
                for subclass in selected_subclasses:
                    subclass_data = filtered_data[filtered_data['Sub Classe'] == subclass]
                    subclass_stats_df = subclass_data.agg({'Moyenne': ['max', 'min', 'mean']}).reset_index()
                    subclass_stats_df.columns = ['Statistique', 'Valeur']
                    subclass_stats_df['Valeur'] = subclass_stats_df['Valeur'].round(2)

                    with st.expander(f"Max Note, Min Note, and Moyenne of Note Ctrl 1 for Sub Classe: {subclass}", expanded=False):
                        col1, col2 = st.columns([2, 3])
                        with col1:
                            use_container_width = True
                            st.dataframe(subclass_stats_df, use_container_width=use_container_width)
                            #st.write(subclass_stats_df)
                        with col2:
                            use_container_width = True
                            fig = px.bar(subclass_stats_df, x='Statistique', y='Valeur',
                                        title=f'Max Note, Min Note, and Moyenne of Note Ctrl 1 for Sub Classe: {subclass}',
                                        labels={'Valeur': 'Note', 'Statistique': 'Statistic'},
                                        color_discrete_sequence=px.colors.qualitative.Set1)
                            fig.update_layout(xaxis_title='Statistic', yaxis_title='Note')
                            #st.plotly_chart(fig)
                            st.plotly_chart(fig, use_container_width=use_container_width)
                            
        elif sub_query == 'Eleves ayant note au dessus et au dessous la moyenne par Classe':
            st.subheader("Eleves ayant note au dessus et au dessous la moyenne par Classe")

            # Select classes
            selected_classes = st.multiselect("Select Classe", df['Classe'].unique())

            # Filter data based on selected classes
            filtered_data = df[df['Classe'].isin(selected_classes)]

            if set(selected_classes) == set(df['Classe'].unique()):
                # Calculate total counts of Note Ctrl 1 >= 10 and < 10 for each class
                total_counts_classe_df = df.groupby('Classe')['Moyenne'].agg([('Total >= 10', lambda x: (x >= 10).sum()), ('Total < 10', lambda x: (x < 10).sum())]).reset_index()

                # Calculate total counts for each class
                total_counts_classe_df['Total'] = total_counts_classe_df['Total >= 10'] + total_counts_classe_df['Total < 10']

                # Calculate percentage for each category
                total_counts_classe_df['Percentage >= 10'] = (total_counts_classe_df['Total >= 10'] / total_counts_classe_df['Total']) * 100
                total_counts_classe_df['Percentage < 10'] = (total_counts_classe_df['Total < 10'] / total_counts_classe_df['Total']) * 100

                # Round the percentage values to two decimal places
                total_counts_classe_df['Percentage >= 10'] = total_counts_classe_df['Percentage >= 10'].round(2)
                total_counts_classe_df['Percentage < 10'] = total_counts_classe_df['Percentage < 10'].round(2)

                # Display the DataFrame
                with st.expander("Eleves ayant note au dessus et au dessous la moyenne par Classe", expanded=False):
                    col1, col2 = st.columns([2, 3])
                    with col1:
                        use_container_width = True
                        st.dataframe(total_counts_classe_df, use_container_width=use_container_width)
                        #st.write(total_counts_classe_df)
                        
                    with col2:
                        use_container_width = True
                        fig_bar = px.bar(total_counts_classe_df, x='Classe', y=['Total >= 10', 'Total < 10'],
                                        title='Total Counts of Moyenne >= 10 and <= 10 for Each Class',
                                        labels={'value': 'Count', 'variable': 'Moyenne'},
                                        color_discrete_map={'Total >= 10': 'green', 'Total < 10': 'red'},
                                        barmode='group')
                        fig_bar.update_layout(xaxis_title='Classe', yaxis_title='Count')
                        #st.plotly_chart(fig_bar)
                        st.plotly_chart(fig_bar, use_container_width=use_container_width)

                        colors = ['green', 'red']
                        
                        # Prepare DataFrame with required columns
                        total_percentage_classe_moyenne_df =  total_counts_classe_df[['Classe','Percentage >= 10','Percentage < 10']]

                        # Plotting Sunburst chart with legend
                        fig = px.sunburst(total_percentage_classe_moyenne_df, path=['Classe', 'Percentage >= 10', 'Percentage < 10'], 
                                title='Percentage Moyenne >= 10 and Moyenne < 10 in each Classe',
                                labels={'Percentage >= 10': 'Percentage >= 10', 'Percentage < 10': 'Percentage < 10'})
                        #st.plotly_chart(fig)
                        st.plotly_chart(fig, use_container_width=use_container_width)
                        
            else:
                for classe in selected_classes:
                    total_counts_classe_df = filtered_data[filtered_data['Classe'] == classe].groupby('Classe')['Moyenne'].agg([('Total >= 10', lambda x: (x >= 10).sum()), ('Total < 10', lambda x: (x < 10).sum())]).reset_index()

                    with st.expander(f"Eleves ayant note au dessus et au dessous la moyenne pour la classe: {classe}", expanded=False):
                        col1, col2 = st.columns([2, 3])
                        with col1:
                            use_container_width = True
                            st.dataframe(total_counts_classe_df, use_container_width=use_container_width)
                            #st.write(total_counts_classe_df)

                        with col2:
                            use_container_width = True
                            fig_bar = px.bar(total_counts_classe_df, x='Classe', y=['Total >= 10', 'Total < 10'],
                                            title=f'Total Counts of Moyenne >= 10 and <= 10 for Classe: {classe}',
                                            labels={'value': 'Count', 'variable': 'Moyenne'},
                                            color_discrete_map={'Total >= 10': 'green', 'Total < 10': 'red'},
                                            barmode='group')
                            fig_bar.update_layout(xaxis_title='Classe', yaxis_title='Count')
                            #st.plotly_chart(fig_bar)
                            st.plotly_chart(fig_bar, use_container_width=use_container_width)

                            colors = ['green', 'red']

                            # Data for current class
                            labels = ["Percentage >= 10", "Percentage < 10"]
                            values = [(total_counts_classe_df['Total >= 10'].iloc[0] / (total_counts_classe_df['Total >= 10'].iloc[0] + total_counts_classe_df['Total < 10'].iloc[0])) * 100, (total_counts_classe_df['Total < 10'].iloc[0] / (total_counts_classe_df['Total >= 10'].iloc[0] + total_counts_classe_df['Total < 10'].iloc[0])) * 100]

                            # Create pie chart for current class with custom colors
                            fig_pie = px.pie(names=labels, values=values, title=f"Class: {classe}",
                                            color_discrete_sequence=colors)
                            #st.plotly_chart(fig_pie)
                            st.plotly_chart(fig_pie, use_container_width=use_container_width)
                            
        elif sub_query == 'Eleves ayant note au dessus et au dessous la moyenne par Sous Classe':
            st.subheader("Eleves ayant note au dessus et au dessous la moyenne par Sous Classe")

            # Select subclasses
            selected_subclasses = st.multiselect("Select Sub Classe", df['Sub Classe'].unique())

            # Filter data based on selected subclasses
            filtered_data = df[df['Sub Classe'].isin(selected_subclasses)]

            if set(selected_subclasses) == set(df['Sub Classe'].unique()):
                # Calculate total counts of Note Ctrl 1 >= 10 and < 10 for each sub class
                total_counts_subclasse_df = df.groupby('Sub Classe')['Moyenne'].agg([('Total >= 10', lambda x: (x >= 10).sum()), ('Total < 10', lambda x: (x < 10).sum())]).reset_index()

                # Calculate the total number of students for each sub class
                total_counts_subclasse_df['Total'] = total_counts_subclasse_df['Total >= 10'] + total_counts_subclasse_df['Total < 10']

                # Calculate the percentage for each category
                total_counts_subclasse_df['Percentage >= 10'] = (total_counts_subclasse_df['Total >= 10'] / total_counts_subclasse_df['Total']) * 100
                total_counts_subclasse_df['Percentage < 10'] = (total_counts_subclasse_df['Total < 10'] / total_counts_subclasse_df['Total']) * 100

                # Round the percentage values
                total_counts_subclasse_df['Percentage >= 10'] = total_counts_subclasse_df['Percentage >= 10'].round()
                total_counts_subclasse_df['Percentage < 10'] = total_counts_subclasse_df['Percentage < 10'].round()

                # Display the DataFrame
                with st.expander("Eleves ayant note au dessus et au dessous la moyenne par Sous Classe", expanded=False):
                    col1, col2 = st.columns([2, 3])
                    with col1:
                        use_container_width = True
                        st.dataframe(total_counts_subclasse_df, use_container_width=use_container_width)
                        #st.write(total_counts_subclasse_df)

                    with col2:
                        use_container_width = True
                        fig_bar = px.bar(total_counts_subclasse_df, x='Sub Classe', y=['Total >= 10', 'Total < 10'],
                                        title='Total Counts of Moyenne >= 10 and <= 10 for Each Sub Classe',
                                        labels={'value': 'Count', 'variable': 'Note Ctrl 1'},
                                        color_discrete_map={'Total >= 10': 'green', 'Total < 10': 'red'},
                                        barmode='group')
                        fig_bar.update_layout(xaxis_title='Sub Classe', yaxis_title='Count')
                        #st.plotly_chart(fig_bar)
                        st.plotly_chart(fig_bar, use_container_width=use_container_width)

                        colors = ['green', 'red']
                        
                        # Prepare DataFrame with required columns
                        total_percentage_sub_classe_moyenne_df = total_counts_subclasse_df[['Sub Classe','Percentage >= 10','Percentage < 10']]

                        # Plotting Sunburst chart with legend
                        fig = px.sunburst(total_percentage_sub_classe_moyenne_df, path=['Sub Classe', 'Percentage >= 10', 'Percentage < 10'], 
                                title='Percentage Moyenne >= 10 and Moyenne < 10 in each Classe',
                                labels={'Percentage >= 10': 'Percentage >= 10', 'Percentage < 10': 'Percentage < 10'})
                        st.plotly_chart(fig)


            else:
                for subclass in selected_subclasses:
                    total_counts_subclasse_df = filtered_data[filtered_data['Sub Classe'] == subclass].groupby('Sub Classe')['Moyenne'].agg([('Total >= 10', lambda x: (x >= 10).sum()), ('Total < 10', lambda x: (x < 10).sum())]).reset_index()

                    with st.expander(f"Eleves ayant note au dessus et au dessous la moyenne par Sous Classe: {subclass}", expanded=False):
                        col1, col2 = st.columns([2, 3])
                        with col1:
                            use_container_width = True
                            st.dataframe(total_counts_subclasse_df, use_container_width=use_container_width)
                            #st.write(total_counts_subclasse_df)

                        with col2:
                            use_container_width = True
                            fig_bar = px.bar(total_counts_subclasse_df, x='Sub Classe', y=['Total >= 10', 'Total < 10'],
                                            title=f'Total Counts of Moyenne >= 10 and <= 10 for Sous Classe: {subclass}',
                                            labels={'value': 'Count', 'variable': 'Moyenne'},
                                            color_discrete_map={'Total >= 10': 'green', 'Total < 10': 'red'},
                                            barmode='group')
                            fig_bar.update_layout(xaxis_title='Sub Classe', yaxis_title='Count')
                            #st.plotly_chart(fig_bar)
                            st.plotly_chart(fig_bar, use_container_width=use_container_width)

                            colors = ['green', 'red']

                            # Data for current sub class
                            labels = ["Percentage >= 10", "Percentage < 10"]
                            values = [(total_counts_subclasse_df['Total >= 10'].iloc[0] / (total_counts_subclasse_df['Total >= 10'].iloc[0] + total_counts_subclasse_df['Total < 10'].iloc[0])) * 100, (total_counts_subclasse_df['Total < 10'].iloc[0] / (total_counts_subclasse_df['Total >= 10'].iloc[0] + total_counts_subclasse_df['Total < 10'].iloc[0])) * 100]

                            # Create pie chart for current sub class with custom colors
                            fig_pie = px.pie(names=labels, values=values, title=f"Sub Classe: {subclass}",
                                            color_discrete_sequence=colors)
                            #st.plotly_chart(fig_pie)
                            st.plotly_chart(fig_pie, use_container_width=use_container_width)






# Requette 6: Notes Mentions
def requette_6(df):
    st.subheader("Mentions")

    st.subheader("Sous menu : Mentions")
    # Define subqueries for request 1
    sous_menus = {
        "Mentions": ['Répartition par Mention', 'Répartition de la Mention par Classe', 'Répartition de la Mention par Sous Classe']
    }

    # Use option menu to select subquery
    if "Mentions" in sous_menus:
        sub_query = option_menu(None, sous_menus["Mentions"], orientation="horizontal",
                                     styles={
                                         #"container": {"white-space": "nowrap"}  # Empêcher le retour à la ligne pour les éléments
                                        "container": {"max-width": "100%", "white-space": "nowrap"}  # Définir une largeur maximale pour le conteneur et empêcher le retour à la ligne
                                     })
    else:
        st.write("No subqueries available for Mentions")
    
    
    main_container = st.container()
    with main_container:
        if sub_query == 'Répartition par Mention':
            st.subheader("Répartition par Mention")
            with st.expander("Répartition par Mention", expanded=False):
                count_mentions_df = df['Mention'].value_counts().reset_index()
                count_mentions_df.columns = ['Mention', 'Count']    
                col1, col2 = st.columns([2, 3])
                col3 = st.columns([8])[0]  # Full width for the third column
                
            
                with col1:
                    use_container_width = True
                    st.dataframe(count_mentions_df, use_container_width=use_container_width)
                    #st.write(count_mentions_df)

                with col2:
                    use_container_width = True
                    fig_bar_mentions = px.bar(count_mentions_df, x='Mention', y='Count', title='Count of Mentions', 
                                        labels={'Mention': 'Mention', 'Count': 'Count'}, color='Mention',
                                        color_discrete_map={'Mention': 'darkblue'})
                    #st.plotly_chart(fig_bar_mentions)
                    st.plotly_chart(fig_bar_mentions, use_container_width=use_container_width)

            
                with col3:
                    use_container_width = True
                    count_mentions_df['Percentage'] = (count_mentions_df['Count'] / count_mentions_df['Count'].sum()) * 100
                    fig_pie_mentions = px.pie(count_mentions_df, values='Percentage', names='Mention', title='Percentage Distribution of Mentions')
                    #st.plotly_chart(fig_pie_mentions)
                    st.plotly_chart(fig_pie_mentions, use_container_width=use_container_width)
                    
                        
    
        elif sub_query == 'Répartition de la Mention par Classe':
            st.subheader("Répartition de la Mention par Classe")

            # Filter data based on selected Classe
            classes = st.multiselect("Select Classe", df['Classe'].unique())
            filtered_data = df[df['Classe'].isin(classes)]
            
            # Check if all available classes are selected
            if set(classes) == set(df['Classe'].unique()):
                # Generate dataframe for all data
                count_mention_by_classe_df = df['Mention'].value_counts().reset_index()
                count_mention_by_classe_df.columns = ['Mention', 'Count']

                with st.expander("All Classes", expanded=False):
                    st.write("All Classes:")
                    #col1, col2, col3 = st.columns([1, 1, 1])
                    col1, col2 = st.columns([2, 3])
                    col3 = st.columns([8])[0]  # Full width for the third column
                    with col1:
                        use_container_width = True
                        st.dataframe(count_mention_by_classe_df, use_container_width=use_container_width)            
                        #st.write(count_mention_by_classe_df)
                    with col2:
                        use_container_width = True
                        fig = px.bar(count_mention_by_classe_df, 
                            x='Mention', 
                            y='Count', 
                            color='Mention',
                            title='Count of Mentions by Classe',
                            barmode='group')
                        #st.plotly_chart(fig)
                        st.plotly_chart(fig, use_container_width=use_container_width)
                        
                    with col3:
                        use_container_width = True
                        count_mention_by_classe_df['Percentage'] = (count_mention_by_classe_df['Count'] / count_mention_by_classe_df['Count'].sum()) * 100
                        count_mention_by_classe_df['Percentage'] = count_mention_by_classe_df['Percentage'].round(2)
                        fig_pie = px.pie(count_mention_by_classe_df, values='Percentage', names='Mention', title=f'Percentage Distribution of Mention for all classes')
                        #st.plotly_chart(fig_pie)
                        st.plotly_chart(fig_pie, use_container_width=use_container_width)
                        


                
                
            else:
                for classe in classes:
                    count_mention_by_classe_df = filtered_data[filtered_data['Classe'] == classe]['Mention'].value_counts().reset_index()
                    count_mention_by_classe_df.columns = ['Mention', 'Count']
                    count_mention_by_classe_df['Percentage'] = (count_mention_by_classe_df['Count'] / count_mention_by_classe_df['Count'].sum()) * 100
                    count_mention_by_classe_df['Percentage'] = count_mention_by_classe_df['Percentage'].round(2)

                    with st.expander(f"Classe: {classe}", expanded=False):
                        st.write(f"Classe: {classe}")

                        #col1, col2, col3 = st.columns([1, 1, 1])
                        col1, col2 = st.columns([2, 3])
                        col3 = st.columns([8])[0]  # Full width for the third column

                        with col1:
                            use_container_width = True
                            st.dataframe(count_mention_by_classe_df, use_container_width=use_container_width)
                            #st.write(count_mention_by_classe_df)

                        with col2:
                            use_container_width = True
                            fig_mention_by_classe = px.bar(count_mention_by_classe_df, x='Mention', y='Count', 
                                                title=f'Count of Mentions for {classe}', 
                                                labels={'Mention': 'Mention', 'Count': 'Count'}, color='Mention',
                                                color_discrete_map={'Mention': 'darkblue'})
                            #st.plotly_chart(fig_mention_by_classe)
                            st.plotly_chart(fig_mention_by_classe, use_container_width=use_container_width)

                        with col3:
                            use_container_width = True
                            fig_pie_mention_by_classe = px.pie(count_mention_by_classe_df, values='Percentage', names='Mention', title=f'Percentage Distribution of Mentions for {classe}')
                            #st.plotly_chart(fig_pie_mention_by_classe)
                            st.plotly_chart(fig_pie_mention_by_classe, use_container_width=use_container_width)
                            

        elif sub_query == 'Répartition de la Mention par Sous Classe':
            st.subheader("Répartition de la Mention par Sous Classe")

            # Filter data based on selected Classe
            sub_classes = st.multiselect("Select Sub Classe", df['Sub Classe'].unique())
            filtered_data = df[df['Sub Classe'].isin(sub_classes)]
            
            # Check if all available classes are selected
            if set(sub_classes) == set(df['Sub Classe'].unique()):
                # Generate dataframe for all data
                count_mention_by_sub_classe_df = df['Mention'].value_counts().reset_index()
                count_mention_by_sub_classe_df.columns = ['Mention', 'Count']

                with st.expander("All Classes", expanded=False):
                    st.write("All Classes:")
                    #col1, col2, col3 = st.columns([1, 1, 1])
                    col1, col2 = st.columns([2, 3])
                    col3 = st.columns([8])[0]  # Full width for the third column
                    with col1:
                        use_container_width = True
                        st.dataframe(count_mention_by_sub_classe_df, use_container_width=use_container_width)
                        #st.write(count_mention_by_sub_classe_df)
                    with col2:
                        use_container_width = True
                        fig = px.bar(count_mention_by_sub_classe_df, 
                            x='Mention', 
                            y='Count', 
                            color='Mention',
                            title='Count of Mentions by Sub Classe',
                            barmode='group')
                        #st.plotly_chart(fig)
                        st.plotly_chart(fig, use_container_width=use_container_width)
                    with col3:
                        use_container_width = True
                        count_mention_by_sub_classe_df['Percentage'] = (count_mention_by_sub_classe_df['Count'] / count_mention_by_sub_classe_df['Count'].sum()) * 100
                        count_mention_by_sub_classe_df['Percentage'] = count_mention_by_sub_classe_df['Percentage'].round(2)
                        fig_pie = px.pie(count_mention_by_sub_classe_df, values='Percentage', names='Mention', title=f'Percentage Distribution of Mention for all sub classes')
                        #st.plotly_chart(fig_pie)
                        st.plotly_chart(fig_pie, use_container_width=use_container_width)


                
                
            else:
                for sub_classe in sub_classes:
                    count_mention_by_sub_classe_df = filtered_data[filtered_data['Sub Classe'] == sub_classe]['Mention'].value_counts().reset_index()
                    count_mention_by_sub_classe_df.columns = ['Mention', 'Count']
                    count_mention_by_sub_classe_df['Percentage'] = (count_mention_by_sub_classe_df['Count'] / count_mention_by_sub_classe_df['Count'].sum()) * 100
                    count_mention_by_sub_classe_df['Percentage'] = count_mention_by_sub_classe_df['Percentage'].round(2)

                    with st.expander(f"Sub Classe: {sub_classe}", expanded=False):
                        st.write(f"Sub Classe: {sub_classe}")

                        #col1, col2, col3 = st.columns([1, 1, 1])
                        col1, col2 = st.columns([2, 3])
                        col3 = st.columns([8])[0]  # Full width for the third column

                        with col1:
                            use_container_width = True
                            st.dataframe(count_mention_by_sub_classe_df, use_container_width=use_container_width)
                            #st.write(count_mention_by_sub_classe_df)

                        with col2:
                            use_container_width = True
                            fig_mention_by_sub_classe = px.bar(count_mention_by_sub_classe_df, x='Mention', y='Count', 
                                                title=f'Count of Mentions for {sub_classe}', 
                                                labels={'Mention': 'Mention', 'Count': 'Count'}, color='Mention',
                                                color_discrete_map={'Mention': 'darkblue'})
                            #st.plotly_chart(fig_mention_by_sub_classe)
                            st.plotly_chart(fig_mention_by_sub_classe, use_container_width=use_container_width)

                        with col3:
                            use_container_width = True
                            fig_pie_mention_by_sub_classe = px.pie(count_mention_by_sub_classe_df, values='Percentage', names='Mention', title=f'Percentage Distribution of Mentions for {sub_classe}')
                            #st.plotly_chart(fig_pie_mention_by_sub_classe)
                            st.plotly_chart(fig_pie_mention_by_sub_classe, use_container_width=use_container_width)


def top_students_by_subclass(df, subclass):
    # Filter the DataFrame for the specified subclass
    subclass_df = df[df['Sub Classe'] == subclass]

    # Sort the students by their average score (Moyenne) in descending order
    sorted_df = subclass_df.sort_values(by='Moyenne', ascending=False)

    # Extract the top 3 students for this subclass
    top_students_df = sorted_df.head(3)[['Code Massar','Nom et prénom', 'Moyenne', 'Sub Classe']]

    return top_students_df


def top_students_by_subclass(df, subclass, num_students):
    # Filter the DataFrame for the specified subclass
    subclass_df = df[df['Sub Classe'] == subclass]

    # Sort the students by their average score (Moyenne) in descending order
    sorted_df = subclass_df.sort_values(by='Moyenne', ascending=False)

    # Extract the top students for this subclass based on the specified number
    top_students_df = sorted_df.head(num_students)[['Code Massar','Nom et prénom', 'Moyenne', 'Sub Classe']]

    return top_students_df



def requette_7(df):
    st.subheader("N premiers éleves")
    # Get unique subclasses
    sub_classes = st.multiselect("Select Sub Classe", df['Sub Classe'].unique())

    # If no subclass is selected, return
    if not sub_classes:
        st.warning("Please select at least one Sub Classe.")
        return

    # Define custom colors
    custom_colors = px.colors.qualitative.Set2
    num_students = st.slider("Sélectionner le nombre de meilleurs étudiants à afficher", min_value=3, max_value=10, value=3)

    # If all subclasses are selected
    if set(sub_classes) == set(df['Sub Classe'].unique()):
        # Concatenate top students data for all subclasses
        # Sélectionner le nombre de meilleurs étudiants à afficher avec un slider
        #num_students = st.slider("Sélectionner le nombre de meilleurs étudiants à afficher", min_value=3, max_value=10, value=3)
        top_students_all_df = pd.concat([top_students_by_subclass(df, subclass,num_students ) for subclass in sub_classes])

        # Plotting the bar chart for all subclasses
        fig_all = px.bar(top_students_all_df, x='Nom et prénom', y='Moyenne', 
                         title=f'Top 3 Students for All Sub Classes',
                         labels={'Moyenne': 'Moyenne', 'Nom et prénom': 'Nom et prénom'},
                         color='Nom et prénom',  # Assign colors based on student names
                         color_discrete_sequence=custom_colors)
        
        # Display the DataFrame and plot within separate columns
        with st.expander(f"All Sub Classes", expanded=False):
            # Divide the space into two columns
            col1, col2 = st.columns([2, 3])

            # Col 1: DataFrame
            with col1:
                use_container_width = True
                st.dataframe(top_students_all_df, use_container_width=use_container_width)
                #st.write(top_students_all_df)

            # Col 2: Bar Plot
            with col2:
                use_container_width = True
                st.plotly_chart(fig_all, use_container_width=use_container_width)
                #st.plotly_chart(fig_all)
                
    else:
        # Iterate over each subclass and create plots
        for subclass in sub_classes:
            # Get the top students for the current subclass
            # Sélectionner le nombre de meilleurs étudiants à afficher avec un slider
            #num_students = st.slider("Sélectionner le nombre de meilleurs étudiants à afficher", min_value=3, max_value=10, value=3)
            top_students = top_students_by_subclass(df, subclass,num_students )
            
            # Plotting the bar chart for the current subclass
            fig = px.bar(top_students, x='Nom et prénom', y='Moyenne', 
                         title=f'Top 3 Students for Sub Classe: {subclass}',
                         labels={'Moyenne': 'Moyenne', 'Nom et prénom': 'Nom et prénom'},
                         color='Nom et prénom',  # Assign colors based on student names
                         color_discrete_sequence=custom_colors)
            
            # Display the DataFrame and plot within separate columns
            with st.expander(f"Sub Classe: {subclass}", expanded=False):
                # Divide the space into two columns
                col1, col2 = st.columns([2, 3])

                # Col 1: DataFrame
                with col1:
                    use_container_width = True
                    st.dataframe(top_students, use_container_width=use_container_width)
                    #st.write(top_students)

                # Col 2: Bar Plot
                with col2:
                    use_container_width = True
                    #st.plotly_chart(fig)
                    st.plotly_chart(fig, use_container_width=use_container_width)



# Function to display metrics
def display_metrics(data):
    # Line 1: Total students, Total Males, Total Females
    total_students = len(data)
    total_male = data[data['Sexe'] == 'H']['Sexe'].count()
    total_female = data[data['Sexe'] == 'F']['Sexe'].count()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Students", total_students)
    c2.metric("Total Males", total_male)
    c3.metric("Total Females", total_female)

    # Line 2: Total students in each classe
    total_students_per_classe = data.groupby('Classe').size().reset_index(name='Total Students')

    st.subheader("Total Students in Each Classe")
    with st.expander("Show Total Students in Each Classe"):
        for index, row in total_students_per_classe.iterrows():
            col1, col2 = st.columns([1, 1])
            with col1:
                st.write(row['Classe'])
            with col2:
                st.metric("Total Students", row['Total Students'])


    # Line 3: Total students in each sub classe
    total_students_per_sub_classe = data.groupby('Sub Classe').size().reset_index(name='Total Students')

    st.subheader("Total Students in Each Sub Classe")
    with st.expander("Show Total Students in Each Sub Classe"):
        for index, row in total_students_per_sub_classe.iterrows():
            col1, col2 = st.columns([1, 1])
            with col1:
                st.write(row['Sub Classe'])
            with col2:
                st.metric("Total Students", row['Total Students'])

    # Line 4: Mean in each sub classe (use column: Moyenne)
    mean_per_sub_classe = data.groupby('Sub Classe')['Moyenne'].mean().reset_index(name='Mean')
    mean_per_sub_classe['Mean'] = mean_per_sub_classe['Mean'].round(2)

    st.subheader("Mean in Each Sub Classe")
    with st.expander("Show Mean in Each Sub Classe"):
        for index, row in mean_per_sub_classe.iterrows():
            col1, col2 = st.columns([1, 1])
            with col1:
                st.write(row['Sub Classe'])
            with col2:
                st.metric("Mean", row['Mean'])


def display_student_info(data):
    # Titre de l'application
    st.title("Information apprenants")

    # Champ de saisie pour le code Massar
    code_massar_input = st.text_input("Saisir le Code Massar")

    # Liste déroulante pour choisir parmi les codes Massar disponibles
    codes_massar_list = data['Code Massar'].unique()
    selected_codes_massar = st.multiselect("Choisir un ou plusieurs Code Massar", codes_massar_list)

    # Affichage des informations de l'élève sélectionné
    if code_massar_input:
        student_info = data[data['Code Massar'] == code_massar_input]
        if not student_info.empty:
            st.subheader("Informations de l'élève")
            st.write(student_info)
        else:
            st.write("Aucune information trouvée pour ce Code Massar.")
    elif selected_codes_massar:
        selected_student_info = data[data['Code Massar'].isin(selected_codes_massar)]
        st.subheader("Informations des élèves sélectionnés")
        use_container_width = True
        st.dataframe(selected_student_info, use_container_width=use_container_width)
        #st.write(selected_student_info)
 
 
 
                  
# Define the main function
def main():
    #st.title("Streamlit App")
    st.sidebar.title("Upload your massar exported files")

    # File uploader in the sidebar
    #uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=["xlsx"])
    uploaded_files = st.sidebar.file_uploader("Upload your Excel files", type=["xls","xlsx"], accept_multiple_files=True)
        # Check if files are uploaded
    if uploaded_files:
        
        # Select the first uploaded file
        file1 = uploaded_files[3]

        # Read the selected Excel file
        df_annee = pd.read_excel(file1, skiprows=12, engine="openpyxl")
        df_semestre = pd.read_excel(file1, skiprows=10, engine="openpyxl")
        df_matiere = pd.read_excel(file1, skiprows=10, engine="openpyxl")
        df_academie = pd.read_excel(file1, skiprows=6, engine="openpyxl")
        df_province = pd.read_excel(file1, skiprows=6, engine="openpyxl")
        df_ecole = pd.read_excel(file1, skiprows=6, engine="openpyxl")


        # Extract information based on skiprows values
        annee_scolaire = df_annee.columns[3]
        semestre = df_semestre.columns[3]
        matiere = df_matiere.columns[14]
        academie = df_academie.columns[3]
        province = df_province.columns[8]
        ecole = df_ecole.columns[14]
        

        
        # Display extracted information using st.columns for a nice layout with CSS styling
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        col1.write(f"<div style='text-align: center; font-size: 30px;'><b>Année Scolaire:</b> <span style='color:#BF1F4D'>{annee_scolaire}</span></div>", unsafe_allow_html=True)
        col2.write(f"<div style='text-align: center; font-size: 30px;'><b>Semestre:</b> <span style='color:#BF1F4D'>{semestre}</span></div>", unsafe_allow_html=True)
        col3.write(f"<div style='text-align: center; font-size: 30px;'><b>Matiere:</b> <span style='color:#BF1F4D'>{matiere}</span></div>", unsafe_allow_html=True)

        col4, col5, col6 = st.columns(3)
        col4.write(f"<div style='text-align: center; font-size: 30px;'><b>Academie:</b> <span style='color:#BF1F4D'>{academie}</span></div>", unsafe_allow_html=True)
        col5.write(f"<div style='text-align: center; font-size: 30px;'><b>Province:</b> <span style='color:#BF1F4D'>{province}</span></div>", unsafe_allow_html=True)
        col6.write(f"<div style='text-align: center; font-size: 30px;'><b>Ecole:</b> <span style='color:#BF1F4D'>{ecole}</span></div>", unsafe_allow_html=True)
        #st.markdown("---")
        
        
        
        
        df_final = process_files(uploaded_files)
        
        # Display the processed DataFrame
        #st.write(df_final)
        
        # Calculate Moyenne column
        #pourcentage_ctrl = 57.182
        #pourcentage_act_int = 42.818
        
        # Ask the user to enter the percentage for pourcentage_ctrl
        # Ask the user to enter the percentage for pourcentage_ctrl
        st.markdown("---")
        # Sidebar
        
        

        st.sidebar.title("Input Parameters")
        # Add message info
        st.sidebar.info("These are the actual percentages of massar to calculate Moyenne. You can adjust the percentages...")
        # Ask the user to enter the percentage for pourcentage_ctrl
        pourcentage_ctrl = st.sidebar.number_input("Enter the percentage for ctrls:", 
                                    min_value=0.01, max_value=99.99, step=0.01, value=57.19,format="%.2f")
                
        pourcentage_act_int = st.sidebar.number_input("Enter the percentage for Activité intégté :", 
                                    min_value=0.01, max_value=99.99, step=0.01, value=42.81, format="%.2f")
        
        # Check if the total percentage is equal to 100
        total_percentage = pourcentage_ctrl + pourcentage_act_int
        if total_percentage != 100:
            st.sidebar.error("Error: The total percentage must equal 100. Please adjust your input.")
        


        
    # Check if data is uploaded
    #if not data.empty:
        #st.sidebar.title("Queries")
        #selected_query = st.sidebar.selectbox('Select Query', ['Statistic info','Age', 'Sexe', 'Nombre d\'élèves', 'Controle 1', 'Moyennes', 'Mentions', 'Trois premiers éleves','Information sur apprenant'])

        st.title("Menu")

        # Define the main query options
        query_options = ["Statistic info", "Age", "Sexe", "Nombre d'élèves", "Controle 1", "Moyennes", "Mentions", "N premiers éleves", "Information sur apprenant"]
        
        # Use the option menu to select the main query
        selected_query = option_menu(None, 
                            ["Statistic info", "Age", "Sexe", "Nombre d'élèves", "Controle 1", "Moyennes", "Mentions", "N premiers éleves", "Information sur apprenant"],
                            #icons=list(query_options.values()),
                            #icons=["gender-ambiguous", "person-circle" ,"info-circle", "person-lines-fill", "person-vcard", "journal-text", "journal-check","123", "person-badge"],
                            icons= ["info-circle", "person-circle"  ,"gender-ambiguous",  "person-lines-fill", "person-vcard", "journal-text", "journal-check","123", "person-badge" ],
                            menu_icon="cast",
                            default_index=0,
                            orientation="horizontal",
                            styles={
                                #"container": {"white-space": "nowrap"}  # Empêcher le retour à la ligne pour les éléments
                                "container": {"max-width": "100%", "white-space": "nowrap"}  # Définir une largeur maximale pour le conteneur et empêcher le retour à la ligne
                            }
                )



        #st.markdown("---")
        
        if "Note Ctrl 2" in df_final.columns:
            df_final.drop(columns=["Note Ctrl 2"], inplace=True)
        if "Note Ctrl 3" in df_final.columns:
            df_final.drop(columns=["Note Ctrl 3"], inplace=True)
        df_final = calculer_moyenne(df_final, pourcentage_ctrl, pourcentage_act_int)
        
        df_final = calculer_age(df_final)

        
        # Reorder the columns
        df_final = df_final[['Code Massar', 
                            'Nom et prénom', 
                            'Date Naissance', 
                            'Age',
                            'Sexe',
                            'Classe', 
                            'Sub Classe', 
                            'Note Ctrl 1',
                            'Note Act Int',
                            'Moyenne'
                            ]]
        
        df_final = evaluer_notes(df_final)
        




        if selected_query == 'Statistic info':
            st.write("Nombre total de lignes :", len(df_final))
            # Options d'affichage
            expander = st.expander("Nombre de lignes à afficher :", expanded=False)
            with expander:
                # Display the total number of rows
                st.write("Nombre total de lignes :", len(df_final))

                # Select the number of rows to display
                row_selection = st.select_slider("Nombre de lignes à afficher", options=list(range(1, len(df_final) + 1)))

                # Afficher le df avec le nombre de lignes sélectionné
                st.write("DataFrame avec le nombre de lignes sélectionné:")
                st.write(df_final.head(row_selection))

            # Select a class
            classe_expander = st.expander("Sélectionner une classe", expanded=False)
            with classe_expander:
                classe_selection = st.selectbox("Sélectionner une classe", list(df_final["Classe"].unique()))
                st.write(f"Données pour la classe {classe_selection} :")
                filtered_df_Classe = df_final[df_final["Classe"] == classe_selection].reset_index(drop=True)
                st.write(filtered_df_Classe)
                #st.write(df_final[df_final["Classe"] == classe_selection])

            # Select a subclass
            sub_classe_expander = st.expander("Sélectionner une sous-classe", expanded=False)
            with sub_classe_expander:
                sub_classe_selection = st.selectbox("Sélectionner une sous-classe", list(df_final["Sub Classe"].unique()))
                st.write(f"Données pour la sous-classe {sub_classe_selection} :")
                filtered_df_Sub_Classe = df_final[df_final["Sub Classe"] == sub_classe_selection].reset_index(drop=True)
                st.write(filtered_df_Sub_Classe)
                #st.write(df_final[df_final["Sub Classe"] == sub_classe_selection])
            
            #############
            st.markdown("---")
            display_metrics(df_final)
        elif selected_query == 'Age':
            requette_1(df_final)
        elif selected_query == 'Sexe':
            requette_2(df_final)
        elif selected_query == 'Nombre d\'élèves':
            requette_3(df_final)
        elif selected_query == 'Controle 1':
            requette_4(df_final)
        elif selected_query == 'Moyennes':
            requette_5(df_final)
        elif selected_query == 'Mentions':
            requette_6(df_final)
        elif selected_query == 'N premiers éleves':
            requette_7(df_final)
        elif selected_query == 'Information sur apprenant':
            display_student_info(df_final)
          
          
          
    
 


if __name__ == '__main__':
    main()
