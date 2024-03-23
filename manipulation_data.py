###### this file contain function to manipulate data  ##############
import pandas as pd
import numpy as np 
import re
import datetime




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
