import streamlit as st
import pandas as pd
import numpy as np 
import plotly.express as px
import os
import re
import datetime
from streamlit_option_menu import option_menu
import base64 
import io

import manipulation_data
import request_on_data


st.set_page_config(page_title="Dashboard Massar",page_icon="📊",layout="wide")


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

        
               
# Define the main function
def main():
    #st.title("Streamlit App")
    st.sidebar.title("Chargez vos fichiers exportés depuis Massar")

    # File uploader in the sidebar
    #uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=["xlsx"])
    uploaded_files = st.sidebar.file_uploader("Charger vos fichiers Excel", type=["xls","xlsx"], accept_multiple_files=True)
    
    # Check if files are uploaded
    if not uploaded_files:
        st.write("")
        st.write("")
        st.warning("Veuillez charger vos fichiers !")
        st.write("")
        # Display warning message
        st.info("Fichiers requis:\n1) Listes exportées de Massar avec l'option (*) (plusieurs fichiers xlsx)\n2) Liste des informations des élèves de l'année en cours, fournie par le directeur de l'école (un fichier xls ou xlsx)")
        
        st.stop()
    # Check if files are uploaded
    else:
        
        # Select the first uploaded file
        file1 = uploaded_files[1]

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
        col6.write(f"<div style='text-align: center; font-size: 30px;'><b>Collége/Lycée:</b> <span style='color:#BF1F4D'>{ecole}</span></div>", unsafe_allow_html=True)
        #st.markdown("---")
        
        
        
        
        df_final = manipulation_data.process_files(uploaded_files)
        
        # Display the processed DataFrame
        #st.write(df_final)
        
        # Calculate Moyenne column
        #pourcentage_ctrl = 57.182
        #pourcentage_act_int = 42.818
        
        # Ask the user to enter the percentage for pourcentage_ctrl
        # Ask the user to enter the percentage for pourcentage_ctrl
        st.markdown("---")
        # Sidebar
        
        

        st.sidebar.title("Paramètres")
        # Add message info
        st.sidebar.info("Il s'agit des pourcentages réels de massar pour calculer la Moyenne. Vous pouvez ajuster les pourcentages...")
        # Ask the user to enter the percentage for pourcentage_ctrl
        pourcentage_ctrl = st.sidebar.number_input("Indiquer le pourcentage pour les contrôles:", 
                                    min_value=0.01, max_value=99.99, step=0.01, value=57.19,format="%.2f")
                
        pourcentage_act_int = st.sidebar.number_input("Indiquer le pourcentage pour les activitées intégrées :", 
                                    min_value=0.01, max_value=99.99, step=0.01, value=42.81, format="%.2f")
        
        # Check if the total percentage is equal to 100
        total_percentage = pourcentage_ctrl + pourcentage_act_int
        if total_percentage != 100:
            st.sidebar.error("Erreur : Le pourcentage total doit être égal à 100. Veuillez ajuster votre saisie.")
        


   

        st.title("Menu")

        # Define the main query options
        query_options = ["Informations statistiques", "Âge", "Sexe", "Nombre d'élèves", "Controle 1", "Moyennes", "Mentions", "N premiers éleves", "Information sur apprenant"]
        
        
        # Dropping columns if all values are not NaN
        # Vérifier si la colonne 'Note Ctrl 2' est entièrement NaN
        if 'Note Ctrl 2' in df_final.columns and df_final['Note Ctrl 2'].isnull().all():
            df_final.drop(columns=['Note Ctrl 2'], inplace=True)

        # Vérifier si la colonne 'Note Ctrl 3' est entièrement NaN
        if 'Note Ctrl 3' in df_final.columns and df_final['Note Ctrl 3'].isnull().all():
            df_final.drop(columns=['Note Ctrl 3'], inplace=True)
                
       # Check which control columns exist
        control_columns = [col for col in ['Note Ctrl 1', 'Note Ctrl 2', 'Note Ctrl 3'] if col in df_final.columns]

        # Generate the options for the option menu
        options = ["Informations statistiques", "Âge","Sexe", "Nombre d'élèves", "Moyennes", "Mentions", "N premiers éleves", "Information sur apprenant"]
        if control_columns:
            options.insert(4, "Controle 1")
        if len(control_columns) > 1:
            options.insert(5, "Controle 2")
        if len(control_columns) > 2:
            options.insert(6, "Controle 3")
            
        
        # Define the icons list
        icons = ["info-circle", "person-circle", "gender-ambiguous", "person-lines-fill", "person-vcard", "journal-check", "123", "person-badge"]
                        
        # Add "person-vcard" to the icons list based on the number of control columns
        if 'Note Ctrl 1' in control_columns:
            icons.insert(options.index("Controle 1"), "journal-text")
        if 'Note Ctrl 2' in control_columns:
            icons.insert(options.index("Controle 2"), "journal-text")
        if 'Note Ctrl 3' in control_columns:
            icons.insert(options.index("Controle 3"), "journal-text")
                
        # Use the option menu to select the main query
        selected_query = option_menu(None, 
                            options=options,
                            icons=icons,
                            menu_icon="cast",
                            default_index=0,
                            orientation="horizontal",
                            styles={
                                "container": {"max-width": "100%", "white-space": "nowrap"}  
                            }
                )


 
            
        df_final = manipulation_data.calculer_moyenne(df_final, pourcentage_ctrl, pourcentage_act_int)
        
        df_final = manipulation_data.calculer_age(df_final)

                  
        # Case 1: Only 'Note Ctrl 1' exists
        if 'Note Ctrl 1' in df_final.columns and 'Note Ctrl 2' not in df_final.columns and 'Note Ctrl 3' not in df_final.columns:
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

        # Case 2: 'Note Ctrl 1' and 'Note Ctrl 2' exist
        elif 'Note Ctrl 1' in df_final.columns and 'Note Ctrl 2' in df_final.columns and 'Note Ctrl 3' not in df_final.columns:
            df_final = df_final[['Code Massar', 
                                'Nom et prénom', 
                                'Date Naissance', 
                                'Age',
                                'Sexe',
                                'Classe', 
                                'Sub Classe', 
                                'Note Ctrl 1',
                                'Note Ctrl 2', 
                                'Note Act Int',
                                'Moyenne'
                                ]]

        # Case 3: 'Note Ctrl 1', 'Note Ctrl 2', and 'Note Ctrl 3' exist
        elif 'Note Ctrl 1' in df_final.columns and 'Note Ctrl 2' in df_final.columns and 'Note Ctrl 3' in df_final.columns:
            df_final = df_final[['Code Massar', 
                                'Nom et prénom', 
                                'Date Naissance', 
                                'Age',
                                'Sexe',
                                'Classe', 
                                'Sub Classe', 
                                'Note Ctrl 1',
                                'Note Ctrl 2', 
                                'Note Ctrl 3',
                                'Note Act Int',
                                'Moyenne'
                                ]]

        
        df_final = manipulation_data.evaluer_notes(df_final)
        




        if selected_query == 'Informations statistiques':
            st.write("Nombre total des apprenants :", len(df_final))
            # Options d'affichage
            expander = st.expander("Nombre de premier lignes à afficher :", expanded=False)
            with expander:
                use_container_width = True
                # Display the total number of rows
                st.write("Nombre total des apprenants :", len(df_final))

                # Select the number of rows to display
                row_selection = st.select_slider("Nombre de premier lignes à afficher", options=list(range(1, len(df_final) + 1)))

                # Afficher le df avec le nombre de lignes sélectionné
                st.write("Données avec le nombre de lignes sélectionnées:")
                #st.write(df_final.head(row_selection))
                st.dataframe(df_final.head(row_selection), use_container_width=use_container_width)
                
                

            # Select a class
            classe_expander = st.expander("Sélectionner une classe", expanded=False)
            with classe_expander:
                use_container_width = True
                classe_selection = st.selectbox("Sélectionner une classe", list(df_final["Classe"].unique()))
                st.write(f"Données pour la classe {classe_selection} :")
                filtered_df_Classe = df_final[df_final["Classe"] == classe_selection].reset_index(drop=True)
                #st.write(filtered_df_Classe)
                st.dataframe(filtered_df_Classe, use_container_width=use_container_width)
                #st.write(df_final[df_final["Classe"] == classe_selection])

            # Select a subclass
            sub_classe_expander = st.expander("Sélectionner une sous-classe", expanded=False)
            with sub_classe_expander:
                use_container_width = True
                sub_classe_selection = st.selectbox("Sélectionner une sous-classe", list(df_final["Sub Classe"].unique()))
                st.write(f"Données pour la sous-classe {sub_classe_selection} :")
                filtered_df_Sub_Classe = df_final[df_final["Sub Classe"] == sub_classe_selection].reset_index(drop=True)
                #st.write(filtered_df_Sub_Classe)
                st.dataframe(filtered_df_Sub_Classe, use_container_width=use_container_width)
                #st.write(df_final[df_final["Sub Classe"] == sub_classe_selection])
            
            #############
            st.markdown("---")
            request_on_data.display_metrics(df_final)
        elif selected_query == 'Âge':
            request_on_data.requette_1(df_final)
        elif selected_query == 'Sexe':
            request_on_data.requette_2(df_final)
        elif selected_query == 'Nombre d\'élèves':
            request_on_data.requette_3(df_final)
        elif selected_query == 'Nombre d\'élèves':
            request_on_data.requette_3(df_final)
        elif selected_query == 'Controle 1':
            request_on_data.requette_4(df_final)
        elif 'Controle 2' in options and selected_query == 'Controle 2':
                request_on_data.requette_4c2(df_final)
        elif 'Controle 3' in options and selected_query == 'Controle 3':
                request_on_data.requette_4c3(df_final)
        elif selected_query == 'Moyennes':
            request_on_data.requette_5(df_final)
        elif selected_query == 'Mentions':
            request_on_data.requette_6(df_final)
        elif selected_query == 'N premiers éleves':
            request_on_data.requette_7(df_final)
        elif selected_query == 'Information sur apprenant':
            request_on_data.display_student_info(df_final)
          
          
          
    
 


if __name__ == '__main__':
    main()
