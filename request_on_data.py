###################### this file contain requests on data ############################
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import base64 
import io



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
        st.write("Aucune sous-requête n'est disponible pour l'âge")


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
                    
                    # Allow the user to download 'Code Massar' and 'Nom et prénom' of individuals of a specific age
                    selected_age = st.selectbox("Sélectionner l'âge pour télécharger les noms", count_age_df['Age'])
                    filtered_df = df[df['Age'] == selected_age][['Code Massar', 'Nom et prénom','Sub Classe']]

                    
                    # Download Excel file
                    #if st.button("Download Excel File"):
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                        filtered_df.to_excel(writer, index=False, sheet_name='Data')

                    excel_buffer.seek(0)
                    b64 = base64.b64encode(excel_buffer.read()).decode()
                    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="names_of_{selected_age}_yo.xlsx">Download Excel File</a>'
                    st.markdown(href, unsafe_allow_html=True)
            

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
                    
                        

       
        elif sub_query == 'Répartition de l\'age par Classe':
            st.subheader("Répartition de l'age par Classe")
            # Filter data based on selected Classe
            classes = st.multiselect("Select Classe", df['Classe'].unique(), key="select_classe_requette_1")
            filtered_data = df[df['Classe'].isin(classes)]
           
            #filtered_data_classe_age = df[(df['Classe'].isin(classes)) & (df['Age'] == selected_age)]
           
           

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
                            
                            selected_age = st.selectbox("Select Age", count_age_by_classe_df['Age'])
                            filtered_data_classe_age = df[(df['Classe']==classe) & (df['Age'] == selected_age)]
                            excel_buffer = io.BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                                filtered_data_classe_age[['Code Massar', 'Nom et prénom', 'Sub Classe']].to_excel(writer, index=False, sheet_name='Data')

                            excel_buffer.seek(0)
                            b64 = base64.b64encode(excel_buffer.read()).decode()
                            filename = f"filtered_data_{selected_age}_for_{classe}.xlsx"
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel File</a>'
                            st.markdown(href, unsafe_allow_html=True)
    

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
                            
                            selected_age = st.selectbox("Select Age", count_age_by_sub_classe_df['Age'])
                            filtered_data_classe_age = df[(df['Sub Classe']==sub_classe) & (df['Age'] == selected_age)]
                            excel_buffer = io.BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                                filtered_data_classe_age[['Code Massar', 'Nom et prénom', 'Sub Classe']].to_excel(writer, index=False, sheet_name='Data')

                            excel_buffer.seek(0)
                            b64 = base64.b64encode(excel_buffer.read()).decode()
                            filename = f"filtered_data_{selected_age}_for_{sub_classe}.xlsx"
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel File</a>'
                            st.markdown(href, unsafe_allow_html=True)
    

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
                    selected_gendre = st.selectbox("Sélectionner le gendre pour télécharger les noms", count_sexe_df['Sexe'])
                    filtered_df = df[df['Sexe'] == selected_gendre ][['Code Massar', 'Nom et prénom','Sub Classe']]
                    
                    # Download Excel file
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                        filtered_df.to_excel(writer, index=False, sheet_name='Data')

                    excel_buffer.seek(0)
                    b64 = base64.b64encode(excel_buffer.read()).decode()
                    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="names_of_{selected_gendre}.xlsx">Download Excel File</a>'
                    st.markdown(href, unsafe_allow_html=True)

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
            #classes = st.multiselect("Select Classe", df['Classe'].unique())
            classes = st.multiselect("Select Classe", df['Classe'].unique(), key="select_classe_requette_1")
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
                            
                            #selected_gendre = st.selectbox("Select Gendre", count_sexe_by_classe_df['Sexe'])
                            selected_gendre = st.selectbox(f"Sélectionner le Gendre pour {classe}", count_sexe_by_classe_df['Sexe'])
                            filtered_data_classe_gendre = df[(df['Classe']==classe) & (df['Sexe'] == selected_gendre)]
                            excel_buffer = io.BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                                filtered_data_classe_gendre[['Code Massar', 'Nom et prénom', 'Sub Classe']].to_excel(writer, index=False, sheet_name='Data')

                            excel_buffer.seek(0)
                            b64 = base64.b64encode(excel_buffer.read()).decode()
                            filename = f"filtered_data_{selected_gendre}_for_{classe}.xlsx"
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}" > 	                      Download Excel File</a>'
                            st.markdown(href, unsafe_allow_html=True)

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
            #sub_classes = st.multiselect("Select Sub Classe", df['Sub Classe'].unique())
            sub_classes = st.multiselect("Select Sub Classe", df['Sub Classe'].unique(), key="select_sub_classe_requette_1")
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
                            use_container_width = True
                            #st.write(count_sexe_by_sub_classe_df)
                            st.dataframe(count_sexe_by_sub_classe_df, use_container_width=use_container_width)
                            
                            selected_gendre = st.selectbox(f"Sélectionner le Gendre pour {sub_classe}", count_sexe_by_sub_classe_df['Sexe'])
                            filtered_data_sub_classe_gendre = df[(df['Sub Classe']==sub_classe) & (df['Sexe'] == selected_gendre)]
                            excel_buffer = io.BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                                filtered_data_sub_classe_gendre[['Code Massar', 'Nom et prénom', 'Sub Classe']].to_excel(writer, index=False, sheet_name='Data')

                            excel_buffer.seek(0)
                            b64 = base64.b64encode(excel_buffer.read()).decode()
                            filename = f"filtered_data_{selected_gendre}_for_{sub_classe}.xlsx"
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}"> 	                      Download Excel File</a>'
                            st.markdown(href, unsafe_allow_html=True)
                            
                            
                            

                        with col2:
                            use_container_width = True
                            fig_bar = px.bar(count_sexe_by_sub_classe_df, x='Sexe', y='Count', color='Sexe',
                                            barmode='group', title=f'Count of Sexe for {sub_classe}',
                                            labels={'Sexe': 'Sexe', 'Count': 'Count'},
                                            color_discrete_map={'Sexe': 'darkblue'})
                            #st.plotly_chart(fig_bar)
                            st.plotly_chart(fig_bar, use_container_width=use_container_width)

                        with col3:
                            use_container_width = True
                            count_sexe_by_sub_classe_df['Percentage'] = (count_sexe_by_sub_classe_df['Count'] / count_sexe_by_sub_classe_df['Count'].sum()) * 100
                            fig_pie = px.pie(count_sexe_by_sub_classe_df, values='Percentage', names='Sexe', title=f'Percentage Distribution of Sexe for {sub_classe}')
                            #st.plotly_chart(fig_pie)
                            st.plotly_chart(fig_pie, use_container_width=use_container_width)




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
        st.write("Aucune sous-requête n'est disponible pour Nombre d'étudiants")
    
    
    
    main_container = st.container()
    with main_container:
        if sub_query == 'Nombre d\'élèves par Classe':
            st.subheader("Nombre d'élèves par Classe")

            # Filter data based on selected Classe
            classes = st.multiselect("Select Classe", df['Classe'].unique())
            filtered_data = df[df['Classe'].isin(classes)]

            if filtered_data.empty:
                st.warning("Aucune donnée disponible pour la (les) classe(s) sélectionnée(s).")
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
            sub_classes = st.multiselect("Choisir Sous Classe", df['Sub Classe'].unique())
            filtered_data = df[df['Sub Classe'].isin(sub_classes)]

            if filtered_data.empty:
                st.warning("Aucune donnée disponible pour la (les) sous classe(s) sélectionnée(s).")
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
        st.write("Aucune sous-requête n'est disponible pour le contrôle 1")
    
    
    
    main_container = st.container()
    with main_container:
        if sub_query == 'Valeur Maximale, valeur minimale et la moyenne dans chaque sous classe':
            st.subheader("Valeur Maximale, valeur minimale et la moyenne dans chaque sous classe")

            # Select subclasses
            #selected_subclasses = st.multiselect("Select Sub Classe", df['Sub Classe'].unique())
            selected_subclasses = st.multiselect("Choisir Sous Classe", df['Sub Classe'].unique(), key="select_sub_classe_requette_1")

            # Filter data based on selected subclasses
            filtered_data = df[df['Sub Classe'].isin(selected_subclasses)]

            # If all subclasses are selected
            if set(selected_subclasses) == set(df['Sub Classe'].unique()):
                subclasse_stats_df = df.groupby('Sub Classe')['Note Ctrl 1'].agg([('Max Note', 'max'), ('Min Note', 'min'), ('Moyenne', 'mean')]).reset_index()
                subclasse_stats_df['Moyenne'] = subclasse_stats_df['Moyenne'].round(2)

                # Displaying dataframe and plot for all subclasses
                with st.expander("Note maximale, note minimale et moyenne de la note Ctrl 1 pour toutes les sous-classes", expanded=False):
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

                    with st.expander(f"Note maximale, note minimale et moyenne de la note Ctrl 1 pour la Sous Classe: {subclass}", expanded=False):
                        col1, col2 = st.columns([2, 3])
                        with col1:
                            use_container_width = True
                            #st.write(subclass_stats_df)
                            st.dataframe(subclass_stats_df, use_container_width=use_container_width)
                            
                            # Find Code Massar, Nom et prénom, and note for max and min values
                            max_value_row = subclass_data[subclass_data['Note Ctrl 1'] == subclass_stats_df.loc[0, 'Valeur']]
                            min_value_row = subclass_data[subclass_data['Note Ctrl 1'] == subclass_stats_df.loc[1, 'Valeur']]

                            # Extract Code Massar, Nom et prénom, and note for max and min values
                            max_values = max_value_row[['Code Massar', 'Nom et prénom', 'Note Ctrl 1']]
                            min_values = min_value_row[['Code Massar', 'Nom et prénom', 'Note Ctrl 1']]

                            # Concatenate max and min values
                            max_min_values = pd.concat([max_values, min_values], axis=0)

                            # Prepare Excel file
                            excel_buffer = io.BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                                max_min_values.to_excel(writer, index=False, sheet_name=f"{subclass}")

                            # Save Excel file to buffer
                            excel_buffer.seek(0)
                            b64 = base64.b64encode(excel_buffer.read()).decode()
                            filename = f"name__for_{subclass}_of_max_min_note.xlsx"
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel File</a>'
                            st.markdown(href, unsafe_allow_html=True)
                            
                  
                      
                            
                            
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
            #selected_classes = st.multiselect("Select Classe", df['Classe'].unique())
            selected_classes = st.multiselect("Choisir Classe", df['Classe'].unique(), key="select_classe_requette_1")


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
                            # User selects whether to download students with scores >= 10 or < 10
                            #score_range = st.selectbox("Select score range:", ["superieur à 10", "inferieur à 10"], key="select_score_range")
                            score_range = st.selectbox("Sélectionner la plage de score:", ["superieur à 10", "inferieur à 10"], key=f"select_score_range_{classe}")
                             # Filter data for the current class
                            class_data = filtered_data[filtered_data['Classe'] == classe]

                            # Filter data based on selected score range
                            if score_range == "superieur à 10":
                                students = class_data[class_data['Note Ctrl 1'] >= 10]
                            else:
                                students = class_data[class_data['Note Ctrl 1'] < 10]
                                
                            excel_buffer = io.BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                                students[['Code Massar', 'Nom et prénom', 'Note Ctrl 1', 'Sub Classe']].to_excel(writer, index=False, sheet_name=f"{classe}_{score_range}")

                            # Save Excel file to buffer
                            excel_buffer.seek(0)
                            b64 = base64.b64encode(excel_buffer.read()).decode()
                            filename = f"students_{classe}_{score_range}.xlsx"
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel File</a>'
                            st.markdown(href, unsafe_allow_html=True)

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
            #selected_subclasses = st.multiselect("Select Sub Classe", df['Sub Classe'].unique())
            selected_subclasses = st.multiselect("Choisir Sous Classe", df['Sub Classe'].unique(), key="select_sub_classe_requette_1")

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
                            score_range = st.selectbox("Sélectionner la plage de score:", ["superieur à 10", "inferieur à 10"], key=f"select_score_range_{subclass}")
                            # Filter data for the current class
                            subclass_data = filtered_data[filtered_data['Sub Classe'] == subclass]

                            # Filter data based on selected score range
                            if score_range == "superieur à 10":
                                students = subclass_data[subclass_data['Note Ctrl 1'] >= 10]
                            else:
                                students = subclass_data[subclass_data['Note Ctrl 1'] < 10]
                                
                            excel_buffer = io.BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                                students[['Code Massar', 'Nom et prénom', 'Note Ctrl 1', 'Sub Classe']].to_excel(writer, index=False, sheet_name=f"{subclass}_{score_range}")

                            # Save Excel file to buffer
                            excel_buffer.seek(0)
                            b64 = base64.b64encode(excel_buffer.read()).decode()
                            filename = f"students_{subclass}_{score_range}.xlsx"
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel File</a>'
                            st.markdown(href, unsafe_allow_html=True)

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





#Requette Controle 2 : 

def requette_4c2(df):
    st.subheader("Sous menu : Controle 2")
    # Define subqueries for request 1
    sous_menus = {
        "Controle 2": ['Valeur Maximale, valeur minimale et la moyenne dans chaque sous classe', 'Eleves ayant note au dessus et au dessous la moyenne par Classe', 'Eleves ayant note au dessus et au dessous la moyenne par Sous Classe']
    }

    # Use option menu to select subquery
    if "Controle 2" in sous_menus:
        sub_query = option_menu(None, sous_menus["Controle 2"], orientation="horizontal",
                                     styles={
                                         #"container": {"white-space": "nowrap"}  # Empêcher le retour à la ligne pour les éléments
                                        "container": {"max-width": "100%", "white-space": "nowrap"}  # Définir une largeur maximale pour le conteneur et empêcher le retour à la ligne
                                     })
    else:
        st.write("Aucune sous-requête n'est disponible pour Controle 2")
    
    
    
    main_container = st.container()
    with main_container:
        if sub_query == 'Valeur Maximale, valeur minimale et la moyenne dans chaque sous classe':
            st.subheader("Valeur Maximale, valeur minimale et la moyenne dans chaque sous classe")

            # Select subclasses
            #selected_subclasses = st.multiselect("Select Sub Classe", df['Sub Classe'].unique())
            selected_subclasses = st.multiselect("Choisir Sous Classe", df['Sub Classe'].unique(), key="select_sub_classe_requette_1")

            # Filter data based on selected subclasses
            filtered_data = df[df['Sub Classe'].isin(selected_subclasses)]

            # If all subclasses are selected
            if set(selected_subclasses) == set(df['Sub Classe'].unique()):
                subclasse_stats_df = df.groupby('Sub Classe')['Note Ctrl 2'].agg([('Max Note', 'max'), ('Min Note', 'min'), ('Moyenne', 'mean')]).reset_index()
                subclasse_stats_df['Moyenne'] = subclasse_stats_df['Moyenne'].round(2)

                # Displaying dataframe and plot for all subclasses
                with st.expander("Note maximale, note minimale et moyenne de la note Ctrl 2 pour toutes les sous-classes", expanded=False):
                    col1, col2 = st.columns([2, 3])
                    with col1:
                        use_container_width = True
                        #st.write(subclasse_stats_df)
                        st.dataframe(subclasse_stats_df, use_container_width=use_container_width)
                    with col2:
                        use_container_width = True
                        fig = px.bar(subclasse_stats_df, x='Sub Classe', y=['Max Note', 'Min Note', 'Moyenne'],
                                    title='Max Note, Min Note, and Moyenne of Note Ctrl 2 for Each Sub Classe',
                                    labels={'value': 'Note', 'variable': 'Statistic'},
                                    barmode='group')
                        fig.update_layout(xaxis_title='Sub Classe', yaxis_title='Note')
                        #st.plotly_chart(fig)
                        st.plotly_chart(fig, use_container_width=use_container_width)

            else:
                # Display dataframe and plot for each selected subclass
                for subclass in selected_subclasses:
                    subclass_data = filtered_data[filtered_data['Sub Classe'] == subclass]
                    subclass_stats_df = subclass_data.agg({'Note Ctrl 2': ['max', 'min', 'mean']}).reset_index()
                    subclass_stats_df.columns = ['Statistique', 'Valeur']
                    subclass_stats_df['Valeur'] = subclass_stats_df['Valeur'].round(2)

                    with st.expander(f"Note maximale, note minimale et moyenne de la note Ctrl 2 pour la Sous Classe: {subclass}", expanded=False):
                        col1, col2 = st.columns([2, 3])
                        with col1:
                            use_container_width = True
                            #st.write(subclass_stats_df)
                            st.dataframe(subclass_stats_df, use_container_width=use_container_width)
                            
                            # Find Code Massar, Nom et prénom, and note for max and min values
                            max_value_row = subclass_data[subclass_data['Note Ctrl 2'] == subclass_stats_df.loc[0, 'Valeur']]
                            min_value_row = subclass_data[subclass_data['Note Ctrl 2'] == subclass_stats_df.loc[1, 'Valeur']]

                            # Extract Code Massar, Nom et prénom, and note for max and min values
                            max_values = max_value_row[['Code Massar', 'Nom et prénom', 'Note Ctrl 2']]
                            min_values = min_value_row[['Code Massar', 'Nom et prénom', 'Note Ctrl 2']]

                            # Concatenate max and min values
                            max_min_values = pd.concat([max_values, min_values], axis=0)

                            # Prepare Excel file
                            excel_buffer = io.BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                                max_min_values.to_excel(writer, index=False, sheet_name=f"{subclass}")

                            # Save Excel file to buffer
                            excel_buffer.seek(0)
                            b64 = base64.b64encode(excel_buffer.read()).decode()
                            filename = f"name__for_{subclass}_of_max_min_note.xlsx"
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel File</a>'
                            st.markdown(href, unsafe_allow_html=True)
                            
                  
                      
                            
                            
                        with col2:
                            use_container_width = True
                            fig = px.bar(subclass_stats_df, x='Statistique', y='Valeur',
                                        title=f'Max Note, Min Note, and Moyenne of Note Ctrl 2 for Sub Classe: {subclass}',
                                        labels={'Valeur': 'Note', 'Statistique': 'Statistic'},
                                        color_discrete_sequence=px.colors.qualitative.Set1)
                            fig.update_layout(xaxis_title='Statistic', yaxis_title='Note')
                            #st.plotly_chart(fig)
                            st.plotly_chart(fig, use_container_width=use_container_width)

        elif sub_query == 'Eleves ayant note au dessus et au dessous la moyenne par Classe':
            st.subheader("Eleves ayant note au dessus et au dessous la moyenne par Classe")

            # Select classes
            #selected_classes = st.multiselect("Select Classe", df['Classe'].unique())
            selected_classes = st.multiselect("Choisir Classe", df['Classe'].unique(), key="select_classe_requette_1")


            # Filter data based on selected classes
            filtered_data = df[df['Classe'].isin(selected_classes)]

            if set(selected_classes) == set(df['Classe'].unique()):
                # Calculate total counts of Note Ctrl 1 >= 10 and < 10 for each class
                total_counts_classe_df = df.groupby('Classe')['Note Ctrl 2'].agg([('Total >= 10', lambda x: (x >= 10).sum()), ('Total < 10', lambda x: (x < 10).sum())]).reset_index()

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
                                        title='Total Counts of Note Ctrl 2 >= 10 and <= 10 for Each Class',
                                        labels={'value': 'Count', 'variable': 'Note Ctrl 2'},
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
                    total_counts_classe_df = filtered_data[filtered_data['Classe'] == classe].groupby('Classe')['Note Ctrl 2'].agg([('Total >= 10', lambda x: (x >= 10).sum()), ('Total < 10', lambda x: (x < 10).sum())]).reset_index()

                    with st.expander(f"Eleves ayant note au dessus et au dessous la moyenne pour la classe: {classe}", expanded=False):
                        col1, col2 = st.columns([2, 3])
                        with col1:
                            use_container_width = True
                            #st.write(total_counts_classe_df)
                            st.dataframe(total_counts_classe_df, use_container_width=use_container_width)
                            # User selects whether to download students with scores >= 10 or < 10
                            #score_range = st.selectbox("Select score range:", ["superieur à 10", "inferieur à 10"], key="select_score_range")
                            score_range = st.selectbox("Select score range:", ["superieur à 10", "inferieur à 10"], key=f"select_score_range_{classe}")
                             # Filter data for the current class
                            class_data = filtered_data[filtered_data['Classe'] == classe]

                            # Filter data based on selected score range
                            if score_range == "superieur à 10":
                                students = class_data[class_data['Note Ctrl 2'] >= 10]
                            else:
                                students = class_data[class_data['Note Ctrl 2'] < 10]
                                
                            excel_buffer = io.BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                                students[['Code Massar', 'Nom et prénom', 'Note Ctrl 2', 'Sub Classe']].to_excel(writer, index=False, sheet_name=f"{classe}_{score_range}")

                            # Save Excel file to buffer
                            excel_buffer.seek(0)
                            b64 = base64.b64encode(excel_buffer.read()).decode()
                            filename = f"students_{classe}_{score_range}.xlsx"
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel File</a>'
                            st.markdown(href, unsafe_allow_html=True)

                        with col2:
                            use_container_width = True
                            fig_bar = px.bar(total_counts_classe_df, x='Classe', y=['Total >= 10', 'Total < 10'],
                                            title=f'Total Counts of Note Ctrl 2 >= 10 and <= 10 for Classe: {classe}',
                                            labels={'value': 'Count', 'variable': 'Note Ctrl 2'},
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
            #selected_subclasses = st.multiselect("Select Sub Classe", df['Sub Classe'].unique())
            selected_subclasses = st.multiselect("Select Sub Classe", df['Sub Classe'].unique(), key="select_sub_classe_requette_1")

            # Filter data based on selected subclasses
            filtered_data = df[df['Sub Classe'].isin(selected_subclasses)]

            if set(selected_subclasses) == set(df['Sub Classe'].unique()):
                # Calculate total counts of Note Ctrl 1 >= 10 and < 10 for each sub class
                total_counts_subclasse_df = df.groupby('Sub Classe')['Note Ctrl 2'].agg([('Total >= 10', lambda x: (x >= 10).sum()), ('Total < 10', lambda x: (x < 10).sum())]).reset_index()

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
                                        title='Total Counts of Note Ctrl 2 >= 10 and <= 10 for Each Sub Classe',
                                        labels={'value': 'Count', 'variable': 'Note Ctrl 2'},
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
                    total_counts_subclasse_df = filtered_data[filtered_data['Sub Classe'] == subclass].groupby('Sub Classe')['Note Ctrl 2'].agg([('Total >= 10', lambda x: (x >= 10).sum()), ('Total < 10', lambda x: (x < 10).sum())]).reset_index()

                    with st.expander(f"Eleves ayant note au dessus et au dessous la moyenne par Sous Classe: {subclass}", expanded=False):
                        col1, col2 = st.columns([2, 3])
                        with col1:
                            use_container_width = True
                            st.dataframe(total_counts_subclasse_df, use_container_width=use_container_width)
                            score_range = st.selectbox("Sélectionner la plage de score:", ["superieur à 10", "inferieur à 10"], key=f"select_score_range_{subclass}")
                            # Filter data for the current class
                            subclass_data = filtered_data[filtered_data['Sub Classe'] == subclass]

                            # Filter data based on selected score range
                            if score_range == "superieur à 10":
                                students = subclass_data[subclass_data['Note Ctrl 2'] >= 10]
                            else:
                                students = subclass_data[subclass_data['Note Ctrl 2'] < 10]
                                
                            excel_buffer = io.BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                                students[['Code Massar', 'Nom et prénom', 'Note Ctrl 2', 'Sub Classe']].to_excel(writer, index=False, sheet_name=f"{subclass}_{score_range}")

                            # Save Excel file to buffer
                            excel_buffer.seek(0)
                            b64 = base64.b64encode(excel_buffer.read()).decode()
                            filename = f"students_{subclass}_{score_range}.xlsx"
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel File</a>'
                            st.markdown(href, unsafe_allow_html=True)

                        with col2:
                            use_container_width = True
                            fig_bar = px.bar(total_counts_subclasse_df, x='Sub Classe', y=['Total >= 10', 'Total < 10'],
                                            title=f'Total Counts of Note Ctrl 2 >= 10 and <= 10 for Sous Classe: {subclass}',
                                            labels={'value': 'Count', 'variable': 'Note Ctrl 2'},
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




#########################################################



# Requette Controle 3 : 

def requette_4c3(df):
    st.subheader("Sous menu : Controle 3")
    # Define subqueries for request 1
    sous_menus = {
        "Controle 3": ['Valeur Maximale, valeur minimale et la moyenne dans chaque sous classe', 'Eleves ayant note au dessus et au dessous la moyenne par Classe', 'Eleves ayant note au dessus et au dessous la moyenne par Sous Classe']
    }

    # Use option menu to select subquery
    if "Controle 3" in sous_menus:
        sub_query = option_menu(None, sous_menus["Controle 3"], orientation="horizontal",
                                     styles={
                                         #"container": {"white-space": "nowrap"}  # Empêcher le retour à la ligne pour les éléments
                                        "container": {"max-width": "100%", "white-space": "nowrap"}  # Définir une largeur maximale pour le conteneur et empêcher le retour à la ligne
                                     })
    else:
        st.write("Aucune sous-requête n'est disponible pour Controle 3")
    
    
    
    main_container = st.container()
    with main_container:
        if sub_query == 'Valeur Maximale, valeur minimale et la moyenne dans chaque sous classe':
            st.subheader("Valeur Maximale, valeur minimale et la moyenne dans chaque sous classe")

            # Select subclasses
            #selected_subclasses = st.multiselect("Select Sub Classe", df['Sub Classe'].unique())
            selected_subclasses = st.multiselect("Choisir Sous Classe", df['Sub Classe'].unique(), key="select_sub_classe_requette_1")

            # Filter data based on selected subclasses
            filtered_data = df[df['Sub Classe'].isin(selected_subclasses)]

            # If all subclasses are selected
            if set(selected_subclasses) == set(df['Sub Classe'].unique()):
                subclasse_stats_df = df.groupby('Sub Classe')['Note Ctrl 3'].agg([('Max Note', 'max'), ('Min Note', 'min'), ('Moyenne', 'mean')]).reset_index()
                subclasse_stats_df['Moyenne'] = subclasse_stats_df['Moyenne'].round(2)

                # Displaying dataframe and plot for all subclasses
                with st.expander("Note maximale, note minimale et moyenne de la note Ctrl 3 pour toutes les sous-classes", expanded=False):
                    col1, col2 = st.columns([2, 3])
                    with col1:
                        use_container_width = True
                        #st.write(subclasse_stats_df)
                        st.dataframe(subclasse_stats_df, use_container_width=use_container_width)
                    with col2:
                        use_container_width = True
                        fig = px.bar(subclasse_stats_df, x='Sub Classe', y=['Max Note', 'Min Note', 'Moyenne'],
                                    title='Max Note, Min Note, and Moyenne of Note Ctrl 3 for Each Sub Classe',
                                    labels={'value': 'Note', 'variable': 'Statistic'},
                                    barmode='group')
                        fig.update_layout(xaxis_title='Sub Classe', yaxis_title='Note')
                        #st.plotly_chart(fig)
                        st.plotly_chart(fig, use_container_width=use_container_width)

            else:
                # Display dataframe and plot for each selected subclass
                for subclass in selected_subclasses:
                    subclass_data = filtered_data[filtered_data['Sub Classe'] == subclass]
                    subclass_stats_df = subclass_data.agg({'Note Ctrl 3': ['max', 'min', 'mean']}).reset_index()
                    subclass_stats_df.columns = ['Statistique', 'Valeur']
                    subclass_stats_df['Valeur'] = subclass_stats_df['Valeur'].round(2)

                    with st.expander(f"Note maximale, note minimale et moyenne de la note Ctrl 3 pour la Sous Classe: {subclass}", expanded=False):
                        col1, col2 = st.columns([2, 3])
                        with col1:
                            use_container_width = True
                            #st.write(subclass_stats_df)
                            st.dataframe(subclass_stats_df, use_container_width=use_container_width)
                            
                            # Find Code Massar, Nom et prénom, and note for max and min values
                            max_value_row = subclass_data[subclass_data['Note Ctrl 3'] == subclass_stats_df.loc[0, 'Valeur']]
                            min_value_row = subclass_data[subclass_data['Note Ctrl 3'] == subclass_stats_df.loc[1, 'Valeur']]

                            # Extract Code Massar, Nom et prénom, and note for max and min values
                            max_values = max_value_row[['Code Massar', 'Nom et prénom', 'Note Ctrl 3']]
                            min_values = min_value_row[['Code Massar', 'Nom et prénom', 'Note Ctrl 3']]

                            # Concatenate max and min values
                            max_min_values = pd.concat([max_values, min_values], axis=0)

                            # Prepare Excel file
                            excel_buffer = io.BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                                max_min_values.to_excel(writer, index=False, sheet_name=f"{subclass}")

                            # Save Excel file to buffer
                            excel_buffer.seek(0)
                            b64 = base64.b64encode(excel_buffer.read()).decode()
                            filename = f"name__for_{subclass}_of_max_min_note.xlsx"
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel File</a>'
                            st.markdown(href, unsafe_allow_html=True)
                            
                  
                      
                            
                            
                        with col2:
                            use_container_width = True
                            fig = px.bar(subclass_stats_df, x='Statistique', y='Valeur',
                                        title=f'Max Note, Min Note, and Moyenne of Note Ctrl 3 for Sub Classe: {subclass}',
                                        labels={'Valeur': 'Note', 'Statistique': 'Statistic'},
                                        color_discrete_sequence=px.colors.qualitative.Set1)
                            fig.update_layout(xaxis_title='Statistic', yaxis_title='Note')
                            #st.plotly_chart(fig)
                            st.plotly_chart(fig, use_container_width=use_container_width)

        elif sub_query == 'Eleves ayant note au dessus et au dessous la moyenne par Classe':
            st.subheader("Eleves ayant note au dessus et au dessous la moyenne par Classe")

            # Select classes
            #selected_classes = st.multiselect("Select Classe", df['Classe'].unique())
            selected_classes = st.multiselect("Choisir Classe", df['Classe'].unique(), key="select_classe_requette_1")


            # Filter data based on selected classes
            filtered_data = df[df['Classe'].isin(selected_classes)]

            if set(selected_classes) == set(df['Classe'].unique()):
                # Calculate total counts of Note Ctrl 1 >= 10 and < 10 for each class
                total_counts_classe_df = df.groupby('Classe')['Note Ctrl 3'].agg([('Total >= 10', lambda x: (x >= 10).sum()), ('Total < 10', lambda x: (x < 10).sum())]).reset_index()

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
                                        title='Total Counts of Note Ctrl 3 >= 10 and <= 10 for Each Class',
                                        labels={'value': 'Count', 'variable': 'Note Ctrl 3'},
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
                    total_counts_classe_df = filtered_data[filtered_data['Classe'] == classe].groupby('Classe')['Note Ctrl 3'].agg([('Total >= 10', lambda x: (x >= 10).sum()), ('Total < 10', lambda x: (x < 10).sum())]).reset_index()

                    with st.expander(f"Eleves ayant note au dessus et au dessous la moyenne pour la classe: {classe}", expanded=False):
                        col1, col2 = st.columns([2, 3])
                        with col1:
                            use_container_width = True
                            #st.write(total_counts_classe_df)
                            st.dataframe(total_counts_classe_df, use_container_width=use_container_width)
                            # User selects whether to download students with scores >= 10 or < 10
                            #score_range = st.selectbox("Select score range:", ["superieur à 10", "inferieur à 10"], key="select_score_range")
                            score_range = st.selectbox("Sélectionner la plage de score:", ["superieur à 10", "inferieur à 10"], key=f"select_score_range_{classe}")
                             # Filter data for the current class
                            class_data = filtered_data[filtered_data['Classe'] == classe]

                            # Filter data based on selected score range
                            if score_range == "superieur à 10":
                                students = class_data[class_data['Note Ctrl 3'] >= 10]
                            else:
                                students = class_data[class_data['Note Ctrl 3'] < 10]
                                
                            excel_buffer = io.BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                                students[['Code Massar', 'Nom et prénom', 'Note Ctrl 1', 'Sub Classe']].to_excel(writer, index=False, sheet_name=f"{classe}_{score_range}")

                            # Save Excel file to buffer
                            excel_buffer.seek(0)
                            b64 = base64.b64encode(excel_buffer.read()).decode()
                            filename = f"students_{classe}_{score_range}.xlsx"
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel File</a>'
                            st.markdown(href, unsafe_allow_html=True)

                        with col2:
                            use_container_width = True
                            fig_bar = px.bar(total_counts_classe_df, x='Classe', y=['Total >= 10', 'Total < 10'],
                                            title=f'Total Counts of Note Ctrl 3 >= 10 and <= 10 for Classe: {classe}',
                                            labels={'value': 'Count', 'variable': 'Note Ctrl 3'},
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
            #selected_subclasses = st.multiselect("Select Sub Classe", df['Sub Classe'].unique())
            selected_subclasses = st.multiselect("Choisir Sous Classe", df['Sub Classe'].unique(), key="select_sub_classe_requette_1")

            # Filter data based on selected subclasses
            filtered_data = df[df['Sub Classe'].isin(selected_subclasses)]

            if set(selected_subclasses) == set(df['Sub Classe'].unique()):
                # Calculate total counts of Note Ctrl 1 >= 10 and < 10 for each sub class
                total_counts_subclasse_df = df.groupby('Sub Classe')['Note Ctrl 3'].agg([('Total >= 10', lambda x: (x >= 10).sum()), ('Total < 10', lambda x: (x < 10).sum())]).reset_index()

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
                                        title='Total Counts of Note Ctrl 3 >= 10 and <= 10 for Each Sub Classe',
                                        labels={'value': 'Count', 'variable': 'Note Ctrl 3'},
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
                    total_counts_subclasse_df = filtered_data[filtered_data['Sub Classe'] == subclass].groupby('Sub Classe')['Note Ctrl 3'].agg([('Total >= 10', lambda x: (x >= 10).sum()), ('Total < 10', lambda x: (x < 10).sum())]).reset_index()

                    with st.expander(f"Eleves ayant note au dessus et au dessous la moyenne par Sous Classe: {subclass}", expanded=False):
                        col1, col2 = st.columns([2, 3])
                        with col1:
                            use_container_width = True
                            st.dataframe(total_counts_subclasse_df, use_container_width=use_container_width)
                            score_range = st.selectbox("Sélectionner la plage de score:", ["superieur à 10", "inferieur à 10"], key=f"select_score_range_{subclass}")
                            # Filter data for the current class
                            subclass_data = filtered_data[filtered_data['Sub Classe'] == subclass]

                            # Filter data based on selected score range
                            if score_range == "superieur à 10":
                                students = subclass_data[subclass_data['Note Ctrl 3'] >= 10]
                            else:
                                students = subclass_data[subclass_data['Note Ctrl 3'] < 10]
                                
                            excel_buffer = io.BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                                students[['Code Massar', 'Nom et prénom', 'Note Ctrl 3', 'Sub Classe']].to_excel(writer, index=False, sheet_name=f"{subclass}_{score_range}")

                            # Save Excel file to buffer
                            excel_buffer.seek(0)
                            b64 = base64.b64encode(excel_buffer.read()).decode()
                            filename = f"students_{subclass}_{score_range}.xlsx"
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel File</a>'
                            st.markdown(href, unsafe_allow_html=True)

                        with col2:
                            use_container_width = True
                            fig_bar = px.bar(total_counts_subclasse_df, x='Sub Classe', y=['Total >= 10', 'Total < 10'],
                                            title=f'Total Counts of Note Ctrl 3 >= 10 and <= 10 for Sous Classe: {subclass}',
                                            labels={'value': 'Count', 'variable': 'Note Ctrl 3'},
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



#####################################################














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
        st.write("Aucune sous-requête disponible pour Moyenne")
    
    
    
    
    main_container = st.container()
    with main_container:
        if sub_query == 'Valeur Maximale, valeur minimale et la moyenne dans chaque sous classe':
            st.subheader("Valeur Maximale, valeur minimale et la moyenne dans chaque sous classe")

            # Select subclasses
            selected_subclasses = st.multiselect("Choosir Sous Classe", df['Sub Classe'].unique())

            # Filter data based on selected subclasses
            filtered_data = df[df['Sub Classe'].isin(selected_subclasses)]

            # If all subclasses are selected
            if set(selected_subclasses) == set(df['Sub Classe'].unique()):
                subclasse_stats_df = df.groupby('Sub Classe')['Moyenne'].agg([('Max Note', 'max'), ('Min Note', 'min'), ('Moyenne', 'mean')]).reset_index()
                subclasse_stats_df['Moyenne'] = subclasse_stats_df['Moyenne'].round(2)

                # Displaying dataframe and plot for all subclasses
                with st.expander("Note maximale, note minimale et moyenne pour toutes les sous-classes", expanded=False):
                    col1, col2 = st.columns([2, 3])
                    with col1:
                        use_container_width = True
                        st.dataframe(subclasse_stats_df, use_container_width=use_container_width)
                        #st.write(subclasse_stats_df)
                    with col2:
                        use_container_width = True
                        fig = px.bar(subclasse_stats_df, x='Sub Classe', y=['Max Note', 'Min Note', 'Moyenne'],
                                    title='Max Note, Min Note, and Moyenne for Each Sub Classe',
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

                    with st.expander(f"Note maximale, note minimale et moyenne pour la sous-classe: {subclass}", expanded=False):
                        col1, col2 = st.columns([2, 3])
                        with col1:
                            use_container_width = True
                            st.dataframe(subclass_stats_df, use_container_width=use_container_width)
                            #st.write(subclass_stats_df)
                            # Find Code Massar, Nom et prénom, and note for max and min values
                            max_value_row = subclass_data[subclass_data['Moyenne'] == subclass_stats_df.loc[0, 'Valeur']]
                            min_value_row = subclass_data[subclass_data['Moyenne'] == subclass_stats_df.loc[1, 'Valeur']]

                            # Extract Code Massar, Nom et prénom, and note for max and min values
                            max_values = max_value_row[['Code Massar', 'Nom et prénom', 'Moyenne']]
                            min_values = min_value_row[['Code Massar', 'Nom et prénom', 'Moyenne']]

                            # Concatenate max and min values
                            max_min_values = pd.concat([max_values, min_values], axis=0)

                            # Prepare Excel file
                            excel_buffer = io.BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                                max_min_values.to_excel(writer, index=False, sheet_name=f"{subclass}")

                            # Save Excel file to buffer
                            excel_buffer.seek(0)
                            b64 = base64.b64encode(excel_buffer.read()).decode()
                            filename = f"name__for_{subclass}_of_max_min_note.xlsx"
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel File</a>'
                            st.markdown(href, unsafe_allow_html=True)
                            
                            
                            
                        with col2:
                            use_container_width = True
                            fig = px.bar(subclass_stats_df, x='Statistique', y='Valeur',
                                        title=f'Max Note, Min Note, and Moyenne for Sub Classe: {subclass}',
                                        labels={'Valeur': 'Note', 'Statistique': 'Statistic'},
                                        color_discrete_sequence=px.colors.qualitative.Set1)
                            fig.update_layout(xaxis_title='Statistic', yaxis_title='Note')
                            #st.plotly_chart(fig)
                            st.plotly_chart(fig, use_container_width=use_container_width)
                            
        elif sub_query == 'Eleves ayant note au dessus et au dessous la moyenne par Classe':
            st.subheader("Eleves ayant note au dessus et au dessous la moyenne par Classe")

            # Select classes
            selected_classes = st.multiselect("Choisir Classe", df['Classe'].unique())

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
                            
                            score_range = st.selectbox("Sélectionner la plage de score:", ["superieur à 10", "inferieur à 10"], key=f"select_score_range_{classe}")
                            # Filter data for the current class
                            class_data = filtered_data[filtered_data['Classe'] == classe]

                            # Filter data based on selected score range
                            if score_range == "superieur à 10":
                                students = class_data[class_data['Moyenne'] >= 10]
                            else:
                                students = class_data[class_data['Moyenne'] < 10]
                                
                            excel_buffer = io.BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                                students[['Code Massar', 'Nom et prénom', 'Moyenne', 'Sub Classe']].to_excel(writer, index=False, sheet_name=f"{classe}_{score_range}")

                            # Save Excel file to buffer
                            excel_buffer.seek(0)
                            b64 = base64.b64encode(excel_buffer.read()).decode()
                            filename = f"students_{classe}_{score_range}.xlsx"
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel File</a>'
                            st.markdown(href, unsafe_allow_html=True)

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
                            
                            score_range = st.selectbox("Sélectionner la plage de score:", ["superieur à 10", "inferieur à 10"], key=f"select_score_range_{subclass}")
                            # Filter data for the current class
                            subclass_data = filtered_data[filtered_data['Sub Classe'] == subclass]

                            # Filter data based on selected score range
                            if score_range == "superieur à 10":
                                students = subclass_data[subclass_data['Moyenne'] >= 10]
                            else:
                                students = subclass_data[subclass_data['Moyenne'] < 10]
                                
                            excel_buffer = io.BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                                students[['Code Massar', 'Nom et prénom', 'Moyenne', 'Sub Classe']].to_excel(writer, index=False, sheet_name=f"{subclass}_{score_range}")

                            # Save Excel file to buffer
                            excel_buffer.seek(0)
                            b64 = base64.b64encode(excel_buffer.read()).decode()
                            filename = f"students_{subclass}_{score_range}.xlsx"
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel File</a>'
                            st.markdown(href, unsafe_allow_html=True)

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
        st.write("Aucune sous-requête n'est disponible pour Mentions")
    
    
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
                    # Allow the user to download 'Code Massar' and 'Nom et prénom' of individuals of a specific age
                    selected_mention = st.selectbox("Sélectionnez la mention à télécharger ", count_mentions_df['Mention'])
                    filtered_df = df[df['Mention'] == selected_mention][['Code Massar', 'Nom et prénom','Sub Classe']]

                    
                    # Download Excel file
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                        filtered_df.to_excel(writer, index=False, sheet_name='Data')

                    excel_buffer.seek(0)
                    b64 = base64.b64encode(excel_buffer.read()).decode()
                    filename = f"filtered_data_{selected_mention}.xlsx"
                    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel File</a>'
                    st.markdown(href, unsafe_allow_html=True)

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
                            # Allow the user to download 'Code Massar' and 'Nom et prénom' of individuals of a specific age
                            ##############################
                            selected_mention = st.selectbox(f"Choisir la Mention pour {classe}", count_mention_by_classe_df['Mention'])
                            filtered_data_classe_mention = df[(df['Classe']==classe) & (df['Mention'] == selected_mention)]
                            excel_buffer = io.BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                                filtered_data_classe_mention[['Code Massar', 'Nom et prénom', 'Sub Classe']].to_excel(writer, index=False, sheet_name='Data')

                            excel_buffer.seek(0)
                            b64 = base64.b64encode(excel_buffer.read()).decode()
                            filename = f"filtered_data_{selected_mention}_for_{classe}.xlsx"
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}" > 	                      Download Excel File</a>'
                            st.markdown(href, unsafe_allow_html=True)
                            ################################

                        
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
            sub_classes = st.multiselect("Choisir Sous Classe", df['Sub Classe'].unique())
            filtered_data = df[df['Sub Classe'].isin(sub_classes)]
            
            # Check if all available classes are selected
            if set(sub_classes) == set(df['Sub Classe'].unique()):
                # Generate dataframe for all data
                count_mention_by_sub_classe_df = df['Mention'].value_counts().reset_index()
                count_mention_by_sub_classe_df.columns = ['Mention', 'Count']

                with st.expander("Tous les Classes", expanded=False):
                    st.write("Tous les Classes:")
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
                            # Allow the user to download 'Code Massar' and 'Nom et prénom' of individuals of a specific age
                            ##############################
                            selected_mention = st.selectbox(f"Select Mention for {sub_classe}", count_mention_by_sub_classe_df['Mention'])
                            filtered_data_sub_classe_mention = df[(df['Sub Classe']==sub_classe) & (df['Mention'] == selected_mention)]
                            excel_buffer = io.BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                                filtered_data_sub_classe_mention[['Code Massar', 'Nom et prénom', 'Sub Classe']].to_excel(writer, index=False, sheet_name='Data')

                            excel_buffer.seek(0)
                            b64 = base64.b64encode(excel_buffer.read()).decode()
                            filename = f"filtered_data_{selected_mention}_for_{sub_classe}.xlsx"
                            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}" > 	                      Download Excel File</a>'
                            st.markdown(href, unsafe_allow_html=True)
                            ################################

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
    sub_classes = st.multiselect("Choisir Sous Classe", df['Sub Classe'].unique())

    # If no subclass is selected, return
    if not sub_classes:
        st.warning("Veuillez sélectionner au moins une Sous Classe.")
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
        with st.expander(f"Tous les Sous Classes", expanded=False):
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
                    ##################################
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                        top_students.to_excel(writer, index=False, sheet_name='Data')

                    excel_buffer.seek(0)
                    b64 = base64.b64encode(excel_buffer.read()).decode()
                    filename = f"{num_students}_premiers_eleves_for_{subclass}.xlsx"
                    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}" > 	                      Download Excel File</a>'
                    st.markdown(href, unsafe_allow_html=True)
                    ####################################

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
    c1.metric("Total des apprenants", total_students)
    c2.metric("Total sexe masculin", total_male)
    c3.metric("Total sexe féminin", total_female)

    # Line 2: Total students in each classe
    total_students_per_classe = data.groupby('Classe').size().reset_index(name='Total Students')

    st.subheader("Nombre total des apprenants dans chaque Classe")
    with st.expander("Afficher le nombre total des apprenants dans chaque classe"):
        for index, row in total_students_per_classe.iterrows():
            col1, col2 = st.columns([1, 1])
            with col1:
                st.write(row['Classe'])
            with col2:
                st.metric("Total apprenants", row['Total Students'])


    # Line 3: Total students in each sub classe
    total_students_per_sub_classe = data.groupby('Sub Classe').size().reset_index(name='Total Students')

    st.subheader("Nombre total des apprenants dans chaque Sous Classe")
    with st.expander("Afficher le nombre total des apprenants dans chaque Sous Classe"):
        for index, row in total_students_per_sub_classe.iterrows():
            col1, col2 = st.columns([1, 1])
            with col1:
                st.write(row['Sub Classe'])
            with col2:
                st.metric("Total apprenants", row['Total Students'])

    # Line 4: Mean in each sub classe (use column: Moyenne)
    mean_per_sub_classe = data.groupby('Sub Classe')['Moyenne'].mean().reset_index(name='Mean')
    mean_per_sub_classe['Mean'] = mean_per_sub_classe['Mean'].round(2)

    st.subheader("Moyenne dans chaque Sous Classe")
    with st.expander("Afficher Moyenne dans chaque Sous Classe"):
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
            use_container_width = True
            st.subheader("Informations de l'apprenant")
            #st.write(student_info)
            st.dataframe(student_info, use_container_width=use_container_width)
            
        else:
            st.write("Aucune information trouvée pour ce Code Massar.")
    elif selected_codes_massar:
        selected_student_info = data[data['Code Massar'].isin(selected_codes_massar)]
        st.subheader("Informations des apprenants sélectionnés")
        use_container_width = True
        st.dataframe(selected_student_info, use_container_width=use_container_width)
        #st.write(selected_student_info)
        ################################
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            selected_student_info.to_excel(writer, index=False, sheet_name='Data')

        excel_buffer.seek(0)
        b64 = base64.b64encode(excel_buffer.read()).decode()
        filename = f"{selected_codes_massar}_infos.xlsx"
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}" > 	                      Download Excel File</a>'
        st.markdown(href, unsafe_allow_html=True)
