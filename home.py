import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Massar",page_icon="📊",layout="wide")
#st.header("Exploration des données du système de gestion scolaire MASSAR")
# Add title using Markdown
#st.markdown("# Exploration des données du système de gestion scolaire MASSAR")

# Add some styling to the title
st.markdown("---")
st.markdown("<small>@FAHMI Marouane</small>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #1E90FF;'>Exploration des données du système de gestion scolaire MASSAR</h1>", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        # Load the uploaded file
        return pd.read_excel(uploaded_file)
    else:
        # Return an empty DataFrame if no file is uploaded
        return pd.DataFrame()


# Requette 1: Age
def requette_1(df):
    st.subheader("Age")

    # Define subqueries for request 1
    sub_queries = ['Répartition par l\'age', 'Répartition de l\'age par Classe', 'Répartition de l\'age par Sous Classe']
    sub_query = st.sidebar.selectbox('Select Sub Query', sub_queries, key="sub_query_requette_1")
    

    # Define the main container for the page
    main_container = st.container()

    with main_container:
        if sub_query == 'Répartition par l\'age':
            with st.expander("Répartition par l'age", expanded=False):
                st.subheader("Répartition par l'age")
                count_age_df = df['Age'].value_counts().reset_index()
                count_age_df.columns = ['Age', 'Count']
                
                # Define columns with minimum padding
                col1, col2 = st.columns([1, 2])

                with col1:
                    st.write(count_age_df)

                with col2:
                    fig_count_age = px.bar(count_age_df, x='Age', y='Count', title='Count of Age', 
                                        labels={'Age': 'Age', 'Count': 'Count'}, color='Age',
                                        color_discrete_map={'Age': 'darkblue'})
                    st.plotly_chart(fig_count_age)

       


       
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
                    
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.write(count_age_by_classe_df)
                    with col2:
                        fig = px.bar(count_age_by_classe_df, 
                            x='Age', 
                            y='Count', 
                            color='Classe',
                            barmode='group',
                            title='Count of Age by Classe', 
                            labels={'Age': 'Age', 'Count': 'Count', 'Classe': 'Classe'},
                            color_discrete_map={'Classe': 'darkred'})
                        st.plotly_chart(fig)
            else:
                for classe in classes:
                    count_age_by_classe_df = filtered_data[filtered_data['Classe'] == classe].groupby('Age').size().reset_index(name='Count')

                    with st.expander(f"Classe: {classe}", expanded=False):
                        st.write(f"Classe: {classe}")
                        #st.write(count_age_by_classe_df)

                        col1, col2 = st.columns([1, 2])

                        with col1:
                            st.write(count_age_by_classe_df)

                        with col2:
                            fig_age_by_classe = px.bar(count_age_by_classe_df, x='Age', y='Count', 
                                                    title=f'Count of Age for {classe}', 
                                                    labels={'Age': 'Age', 'Count': 'Count'}, color='Age',
                                                    color_discrete_map={'Age': 'darkblue'})
                            st.plotly_chart(fig_age_by_classe)


                
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
                    
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.write(count_age_by_subclasse_df)
                    with col2:
                        fig = px.bar(count_age_by_subclasse_df, 
                                    x='Age', 
                                    y='Count', 
                                    color='Sub Classe',
                                    barmode='group',
                                    title='Count of Age by Sub Classe', 
                                    labels={'Age': 'Age', 'Count': 'Count', 'Sub Classe': 'Sub Classe'},
                                    color_discrete_map={'Sub Classe': 'darkgreen'})
                        st.plotly_chart(fig)
            else:
                for sub_classe in sub_classes:
                    count_age_by_sub_classe_df = filtered_data[filtered_data['Sub Classe'] == sub_classe].groupby('Age').size().reset_index(name='Count')

                    with st.expander(f"Sub Classe: {sub_classe}", expanded=False):
                        st.write(f"Sub Classe: {sub_classe}")
                        
                        col1, col2 = st.columns([1, 2])

                        with col1:
                            st.write(count_age_by_sub_classe_df)

                        with col2:
                            fig_age_by_sub_classe = px.bar(count_age_by_sub_classe_df, x='Age', y='Count', 
                                                        title=f'Count of Age for {sub_classe}', 
                                                        labels={'Age': 'Age', 'Count': 'Count'}, color='Age',
                                                        color_discrete_map={'Age': 'darkblue'})
                            st.plotly_chart(fig_age_by_sub_classe)



# Requette 2: Sexe
def requette_2(df):
    st.subheader("Sexe")

    # Define subqueries for request 2
    sub_queries = ['Répartition par Sexe', 'Répartition du Sexe par Classe', 'Répartition du Sexe par Sous Classe']
    sub_query = st.sidebar.selectbox('Select Sub Query', sub_queries)
    
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
                col1, col2 = st.columns([1, 2])
                col3 = st.columns([8])[0]  # Full width for the third column
                
            
                with col1:
                    st.write(count_sexe_df)

                with col2:
                    fig = px.bar(count_sexe_df, x='Sexe', y='Count', title='Count of Sexe',
                                labels={'Sexe': 'Sexe', 'Count': 'Count'}, color='Sexe',
                                color_discrete_map={'Sexe': 'darkblue'})
                    fig.update_layout(showlegend=True)
                    st.plotly_chart(fig)
            
                with col3:
                    count_sexe_df['Percentage'] = (count_sexe_df['Count'] / count_sexe_df['Count'].sum()) * 100
                    fig_pie = px.pie(count_sexe_df, values='Percentage', names='Sexe', title='Percentage Distribution of Sexe')
                    st.plotly_chart(fig_pie)


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
                    col1, col2 = st.columns([1, 2])
                    col3 = st.columns([8])[0]  # Full width for the third column
                    with col1:
                        st.write(count_sexe_by_classe_df)
                    with col2:
                        fig_all_classes = px.bar(count_sexe_by_classe_df, x='Sexe', y='Count', color='Classe',
                                                barmode='group', title='Count of Sexe by Classe',
                                                labels={'Sexe': 'Sexe', 'Count': 'Count', 'Classe': 'Classe'},
                                                color_discrete_map={'Classe': 'darkred'})
                        st.plotly_chart(fig_all_classes)
                    with col3:
                        count_sexe_by_classe_df['Percentage'] = (count_sexe_by_classe_df['Count'] / count_sexe_by_classe_df['Count'].sum()) * 100
                        fig_pie = px.pie(count_sexe_by_classe_df, values='Percentage', names='Sexe', title=f'Percentage Distribution of Sexe for all classes')
                        st.plotly_chart(fig_pie)
            else:
                for classe in classes:
                    count_sexe_by_classe_df = filtered_data[filtered_data['Classe'] == classe]['Sexe'].value_counts().reset_index()
                    count_sexe_by_classe_df.columns = ['Sexe', 'Count']
                    count_sexe_by_classe_df['Percentage'] = (count_sexe_by_classe_df['Count'] / count_sexe_by_classe_df['Count'].sum()) * 100
                    count_sexe_by_classe_df['Percentage'] = count_sexe_by_classe_df['Percentage'].round(2)

                    with st.expander(f"Classe: {classe}", expanded=False):
                        st.write(f"Classe: {classe}")

                        #col1, col2, col3 = st.columns([1, 1, 1])
                        col1, col2 = st.columns([1, 2])
                        col3 = st.columns([8])[0]  # Full width for the third column

                        with col1:
                            st.write(count_sexe_by_classe_df)

                        with col2:
                            fig_bar = px.bar(count_sexe_by_classe_df, x='Sexe', y='Count', color='Sexe',
                                            barmode='group', title=f'Count of Sexe for {classe}',
                                            labels={'Sexe': 'Sexe', 'Count': 'Count'},
                                            color_discrete_map={'Sexe': 'darkblue'})
                            st.plotly_chart(fig_bar)

                        with col3:
                            count_sexe_by_classe_df['Percentage'] = (count_sexe_by_classe_df['Count'] / count_sexe_by_classe_df['Count'].sum()) * 100
                            fig_pie = px.pie(count_sexe_by_classe_df, values='Percentage', names='Sexe', title=f'Percentage Distribution of Sexe for {classe}')
                            st.plotly_chart(fig_pie)

        
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
                    col1, col2 = st.columns([1, 2])
                    col3 = st.columns([8])[0]  # Full width for the third column
                    with col1:
                        st.write(count_sexe_by_sub_classe_df)
                    with col2:
                        fig_all_sub_classes = px.bar(count_sexe_by_sub_classe_df, x='Sexe', y='Count', color='Sub Classe',
                                                    barmode='group', title='Count of Sexe by Sub Classe',
                                                    labels={'Sexe': 'Sexe', 'Count': 'Count', 'Sub Classe': 'Sub Classe'},
                                                    color_discrete_map={'Sub Classe': 'darkgreen'})
                        st.plotly_chart(fig_all_sub_classes)
                    with col3:
                        count_sexe_by_sub_classe_df['Percentage'] = (count_sexe_by_sub_classe_df['Count'] / count_sexe_by_sub_classe_df['Count'].sum()) * 100
                        fig_pie = px.pie(count_sexe_by_sub_classe_df, values='Percentage', names='Sexe', title='Percentage Distribution of Sexe for all sub-classes')
                        st.plotly_chart(fig_pie)
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
    st.subheader("Nombre d'élèves")

    # Define subqueries for request 3
    sub_queries = ['Nombre d\'élèves par Classe', 'Nombre d\'élèves par Sous Classe']
    sub_query = st.sidebar.selectbox('Select Sub Query', sub_queries)
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

                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.write(count_by_classe_df)
                        with col2:
                            fig_bar = px.bar(count_by_classe_df, x='Classe', y='Count', 
                                            title='Count of Students by Classe',
                                            color='Classe', 
                                            color_discrete_sequence=px.colors.qualitative.Set1)
                            fig_bar.update_layout(showlegend=True)
                            st.plotly_chart(fig_bar)
                else:
                    for classe in classes:
                        count_by_classe_df = filtered_data[filtered_data['Classe'] == classe]['Classe'].value_counts().reset_index()
                        count_by_classe_df.columns = ['Classe', 'Count']

                        with st.expander(f"Count by Classe: {classe}", expanded=False):
                            st.write(f"Classe: {classe}")

                            col1, col2 = st.columns([1, 2])

                            with col1:
                                st.write(count_by_classe_df)

                            with col2:
                                fig_bar = px.bar(count_by_classe_df, x='Classe', y='Count', 
                                                title=f'Count of Students for {classe}',
                                                color='Classe', 
                                                color_discrete_sequence=px.colors.qualitative.Set1)
                                fig_bar.update_layout(showlegend=True)
                                st.plotly_chart(fig_bar)

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

                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.write(count_by_subclasse_df)
                        with col2:
                            fig_bar_subclasse = px.bar(count_by_subclasse_df, x='Sub Classe', y='Count', 
                                                    title='Count of Students by Sub Classe',
                                                    color='Sub Classe', 
                                                    color_discrete_sequence=px.colors.qualitative.Set2)
                            fig_bar_subclasse.update_layout(showlegend=True)
                            st.plotly_chart(fig_bar_subclasse)
                else:
                    for sub_classe in sub_classes:
                        count_by_subclasse_df = filtered_data[filtered_data['Sub Classe'] == sub_classe]['Sub Classe'].value_counts().reset_index()
                        count_by_subclasse_df.columns = ['Sub Classe', 'Count']

                        with st.expander(f"Count by Sub Classe: {sub_classe}", expanded=False):
                            st.write(f"Sub Classe: {sub_classe}")

                            col1, col2 = st.columns([1, 2])

                            with col1:
                                st.write(count_by_subclasse_df)

                            with col2:
                                fig_bar_subclasse = px.bar(count_by_subclasse_df, x='Sub Classe', y='Count', 
                                                        title=f'Count of Students for {sub_classe}',
                                                        color='Sub Classe', 
                                                        color_discrete_sequence=px.colors.qualitative.Set2)
                                fig_bar_subclasse.update_layout(showlegend=True)
                                st.plotly_chart(fig_bar_subclasse)


# Requette 4: Notes Controle 1
def requette_4(df):
    st.subheader("Controle 1")

    # Define subqueries for request 4
    sub_queries = ['Valeur Maximale, valeur minimale et la moyenne dans chaque sous classe', 'Eleves ayant note au dessus et au dessous la moyenne par Classe', 'Eleves ayant note au dessus et au dessous la moyenne par Sous Classe']
    sub_query = st.sidebar.selectbox('Select Sub Query', sub_queries)
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
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.write(subclasse_stats_df)
                    with col2:
                        fig = px.bar(subclasse_stats_df, x='Sub Classe', y=['Max Note', 'Min Note', 'Moyenne'],
                                    title='Max Note, Min Note, and Moyenne of Note Ctrl 1 for Each Sub Classe',
                                    labels={'value': 'Note', 'variable': 'Statistic'},
                                    barmode='group')
                        fig.update_layout(xaxis_title='Sub Classe', yaxis_title='Note')
                        st.plotly_chart(fig)
            else:
                # Display dataframe and plot for each selected subclass
                for subclass in selected_subclasses:
                    subclass_data = filtered_data[filtered_data['Sub Classe'] == subclass]
                    subclass_stats_df = subclass_data.agg({'Note Ctrl 1': ['max', 'min', 'mean']}).reset_index()
                    subclass_stats_df.columns = ['Statistique', 'Valeur']
                    subclass_stats_df['Valeur'] = subclass_stats_df['Valeur'].round(2)

                    with st.expander(f"Max Note, Min Note, and Moyenne of Note Ctrl 1 for Sub Classe: {subclass}", expanded=False):
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.write(subclass_stats_df)
                        with col2:
                            fig = px.bar(subclass_stats_df, x='Statistique', y='Valeur',
                                        title=f'Max Note, Min Note, and Moyenne of Note Ctrl 1 for Sub Classe: {subclass}',
                                        labels={'Valeur': 'Note', 'Statistique': 'Statistic'},
                                        color_discrete_sequence=px.colors.qualitative.Set1)
                            fig.update_layout(xaxis_title='Statistic', yaxis_title='Note')
                            st.plotly_chart(fig)


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
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.write(total_counts_classe_df)

                    with col2:
                        fig_bar = px.bar(total_counts_classe_df, x='Classe', y=['Total >= 10', 'Total < 10'],
                                        title='Total Counts of Note Ctrl 1 >= 10 and <= 10 for Each Class',
                                        labels={'value': 'Count', 'variable': 'Note Ctrl 1'},
                                        color_discrete_map={'Total >= 10': 'green', 'Total < 10': 'red'},
                                        barmode='group')
                        fig_bar.update_layout(xaxis_title='Classe', yaxis_title='Count')
                        st.plotly_chart(fig_bar)

                        colors = ['green', 'red']
                        
                        # Prepare DataFrame with required columns
                        total_percentage_classe_moyenne_df =  total_counts_classe_df[['Classe','Percentage >= 10','Percentage < 10']]

                        # Plotting Sunburst chart with legend
                        fig = px.sunburst(total_percentage_classe_moyenne_df, path=['Classe', 'Percentage >= 10', 'Percentage < 10'], 
                                title='Percentage Moyenne >= 10 and Moyenne < 10 in each Classe',
                                labels={'Percentage >= 10': 'Percentage >= 10', 'Percentage < 10': 'Percentage < 10'})
                        st.plotly_chart(fig)
                        



                        # Iterate over each class
                        #for index, row in total_counts_classe_df.iterrows():
                            # Data for current class
                        #   labels = ["Percentage >= 10", "Percentage < 10"]
                        #   values = [row['Percentage >= 10'], row['Percentage < 10']]

                            # Create pie chart for current class with custom colors
                        #  fig_pie = px.pie(names=labels, values=values, title=f"Class: {row['Classe']}",
                        #                 color_discrete_sequence=colors)
                        # st.plotly_chart(fig_pie)

            else:
                for classe in selected_classes:
                    total_counts_classe_df = filtered_data[filtered_data['Classe'] == classe].groupby('Classe')['Note Ctrl 1'].agg([('Total >= 10', lambda x: (x >= 10).sum()), ('Total < 10', lambda x: (x < 10).sum())]).reset_index()

                    with st.expander(f"Eleves ayant note au dessus et au dessous la moyenne pour la classe: {classe}", expanded=False):
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.write(total_counts_classe_df)

                        with col2:
                            fig_bar = px.bar(total_counts_classe_df, x='Classe', y=['Total >= 10', 'Total < 10'],
                                            title=f'Total Counts of Note Ctrl 1 >= 10 and <= 10 for Classe: {classe}',
                                            labels={'value': 'Count', 'variable': 'Note Ctrl 1'},
                                            color_discrete_map={'Total >= 10': 'green', 'Total < 10': 'red'},
                                            barmode='group')
                            fig_bar.update_layout(xaxis_title='Classe', yaxis_title='Count')
                            st.plotly_chart(fig_bar)

                            colors = ['green', 'red']

                            # Data for current class
                            labels = ["Percentage >= 10", "Percentage < 10"]
                            values = [(total_counts_classe_df['Total >= 10'].iloc[0] / (total_counts_classe_df['Total >= 10'].iloc[0] + total_counts_classe_df['Total < 10'].iloc[0])) * 100, (total_counts_classe_df['Total < 10'].iloc[0] / (total_counts_classe_df['Total >= 10'].iloc[0] + total_counts_classe_df['Total < 10'].iloc[0])) * 100]

                            # Create pie chart for current class with custom colors
                            fig_pie = px.pie(names=labels, values=values, title=f"Class: {classe}",
                                            color_discrete_sequence=colors)
                            st.plotly_chart(fig_pie)

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
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.write(total_counts_subclasse_df)

                    with col2:
                        fig_bar = px.bar(total_counts_subclasse_df, x='Sub Classe', y=['Total >= 10', 'Total < 10'],
                                        title='Total Counts of Note Ctrl 1 >= 10 and <= 10 for Each Sub Classe',
                                        labels={'value': 'Count', 'variable': 'Note Ctrl 1'},
                                        color_discrete_map={'Total >= 10': 'green', 'Total < 10': 'red'},
                                        barmode='group')
                        fig_bar.update_layout(xaxis_title='Sub Classe', yaxis_title='Count')
                        st.plotly_chart(fig_bar)

                        colors = ['green', 'red']
                        
                        # Prepare DataFrame with required columns
                        total_percentage_sub_classe_moyenne_df = total_counts_subclasse_df[['Sub Classe','Percentage >= 10','Percentage < 10']]

                        # Plotting Sunburst chart with legend
                        fig = px.sunburst(total_percentage_sub_classe_moyenne_df, path=['Sub Classe', 'Percentage >= 10', 'Percentage < 10'], 
                                title='Percentage Moyenne >= 10 and Moyenne < 10 in each Classe',
                                labels={'Percentage >= 10': 'Percentage >= 10', 'Percentage < 10': 'Percentage < 10'})
                        st.plotly_chart(fig)



                        #########################
                        # Iterate over each sub class
                        #for index, row in total_counts_subclasse_df.iterrows():
                            # Data for current sub class
                        #   labels = ["Percentage >= 10", "Percentage < 10"]
                        #  values = [row['Percentage >= 10'], row['Percentage < 10']]

                            # Create pie chart for current sub class with custom colors
                        # fig_pie = px.pie(names=labels, values=values, title=f"Sub Classe: {row['Sub Classe']}",
                            #                 color_discrete_sequence=colors)
                            #st.plotly_chart(fig_pie)
                        #########################

            else:
                for subclass in selected_subclasses:
                    total_counts_subclasse_df = filtered_data[filtered_data['Sub Classe'] == subclass].groupby('Sub Classe')['Note Ctrl 1'].agg([('Total >= 10', lambda x: (x >= 10).sum()), ('Total < 10', lambda x: (x < 10).sum())]).reset_index()

                    with st.expander(f"Eleves ayant note au dessus et au dessous la moyenne par Sous Classe: {subclass}", expanded=False):
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.write(total_counts_subclasse_df)

                        with col2:
                            fig_bar = px.bar(total_counts_subclasse_df, x='Sub Classe', y=['Total >= 10', 'Total < 10'],
                                            title=f'Total Counts of Note Ctrl 1 >= 10 and <= 10 for Sous Classe: {subclass}',
                                            labels={'value': 'Count', 'variable': 'Note Ctrl 1'},
                                            color_discrete_map={'Total >= 10': 'green', 'Total < 10': 'red'},
                                            barmode='group')
                            fig_bar.update_layout(xaxis_title='Sub Classe', yaxis_title='Count')
                            st.plotly_chart(fig_bar)

                            colors = ['green', 'red']

                            # Data for current sub class
                            labels = ["Percentage >= 10", "Percentage < 10"]
                            values = [(total_counts_subclasse_df['Total >= 10'].iloc[0] / (total_counts_subclasse_df['Total >= 10'].iloc[0] + total_counts_subclasse_df['Total < 10'].iloc[0])) * 100, (total_counts_subclasse_df['Total < 10'].iloc[0] / (total_counts_subclasse_df['Total >= 10'].iloc[0] + total_counts_subclasse_df['Total < 10'].iloc[0])) * 100]

                            # Create pie chart for current sub class with custom colors
                            fig_pie = px.pie(names=labels, values=values, title=f"Sub Classe: {subclass}",
                                            color_discrete_sequence=colors)
                            st.plotly_chart(fig_pie)



# Requette 5: Notes Moyenne
def requette_5(df):
    st.subheader("Moyenne")

    # Define subqueries for request 5
    sub_queries = ['Valeur Maximale, valeur minimale et la moyenne dans chaque sous classe', 'Eleves ayant note au dessus et au dessous la moyenne par Classe', 'Eleves ayant note au dessus et au dessous la moyenne par Sous Classe']
    sub_query = st.sidebar.selectbox('Select Sub Query', sub_queries)
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
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.write(subclasse_stats_df)
                    with col2:
                        fig = px.bar(subclasse_stats_df, x='Sub Classe', y=['Max Note', 'Min Note', 'Moyenne'],
                                    title='Max Note, Min Note, and Moyenne of Note Ctrl 1 for Each Sub Classe',
                                    labels={'value': 'Note', 'variable': 'Statistic'},
                                    barmode='group')
                        fig.update_layout(xaxis_title='Sub Classe', yaxis_title='Note')
                        st.plotly_chart(fig)
            else:
                # Display dataframe and plot for each selected subclass
                for subclass in selected_subclasses:
                    subclass_data = filtered_data[filtered_data['Sub Classe'] == subclass]
                    subclass_stats_df = subclass_data.agg({'Moyenne': ['max', 'min', 'mean']}).reset_index()
                    subclass_stats_df.columns = ['Statistique', 'Valeur']
                    subclass_stats_df['Valeur'] = subclass_stats_df['Valeur'].round(2)

                    with st.expander(f"Max Note, Min Note, and Moyenne of Note Ctrl 1 for Sub Classe: {subclass}", expanded=False):
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.write(subclass_stats_df)
                        with col2:
                            fig = px.bar(subclass_stats_df, x='Statistique', y='Valeur',
                                        title=f'Max Note, Min Note, and Moyenne of Note Ctrl 1 for Sub Classe: {subclass}',
                                        labels={'Valeur': 'Note', 'Statistique': 'Statistic'},
                                        color_discrete_sequence=px.colors.qualitative.Set1)
                            fig.update_layout(xaxis_title='Statistic', yaxis_title='Note')
                            st.plotly_chart(fig)

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
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.write(total_counts_classe_df)

                    with col2:
                        fig_bar = px.bar(total_counts_classe_df, x='Classe', y=['Total >= 10', 'Total < 10'],
                                        title='Total Counts of Moyenne >= 10 and <= 10 for Each Class',
                                        labels={'value': 'Count', 'variable': 'Moyenne'},
                                        color_discrete_map={'Total >= 10': 'green', 'Total < 10': 'red'},
                                        barmode='group')
                        fig_bar.update_layout(xaxis_title='Classe', yaxis_title='Count')
                        st.plotly_chart(fig_bar)

                        colors = ['green', 'red']
                        
                        # Prepare DataFrame with required columns
                        total_percentage_classe_moyenne_df =  total_counts_classe_df[['Classe','Percentage >= 10','Percentage < 10']]

                        # Plotting Sunburst chart with legend
                        fig = px.sunburst(total_percentage_classe_moyenne_df, path=['Classe', 'Percentage >= 10', 'Percentage < 10'], 
                                title='Percentage Moyenne >= 10 and Moyenne < 10 in each Classe',
                                labels={'Percentage >= 10': 'Percentage >= 10', 'Percentage < 10': 'Percentage < 10'})
                        st.plotly_chart(fig)

                        ####### 
                        # Iterate over each class
                        #for index, row in total_counts_classe_df.iterrows():
                            # Data for current class
                        #   labels = ["Percentage >= 10", "Percentage < 10"]
                        #  values = [row['Percentage >= 10'], row['Percentage < 10']]

                            # Create pie chart for current class with custom colors
                        # fig_pie = px.pie(names=labels, values=values, title=f"Class: {row['Classe']}",
                            #                color_discrete_sequence=colors)
                            #st.plotly_chart(fig_pie)
                        #######

            else:
                for classe in selected_classes:
                    total_counts_classe_df = filtered_data[filtered_data['Classe'] == classe].groupby('Classe')['Moyenne'].agg([('Total >= 10', lambda x: (x >= 10).sum()), ('Total < 10', lambda x: (x < 10).sum())]).reset_index()

                    with st.expander(f"Eleves ayant note au dessus et au dessous la moyenne pour la classe: {classe}", expanded=False):
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.write(total_counts_classe_df)

                        with col2:
                            fig_bar = px.bar(total_counts_classe_df, x='Classe', y=['Total >= 10', 'Total < 10'],
                                            title=f'Total Counts of Moyenne >= 10 and <= 10 for Classe: {classe}',
                                            labels={'value': 'Count', 'variable': 'Moyenne'},
                                            color_discrete_map={'Total >= 10': 'green', 'Total < 10': 'red'},
                                            barmode='group')
                            fig_bar.update_layout(xaxis_title='Classe', yaxis_title='Count')
                            st.plotly_chart(fig_bar)

                            colors = ['green', 'red']

                            # Data for current class
                            labels = ["Percentage >= 10", "Percentage < 10"]
                            values = [(total_counts_classe_df['Total >= 10'].iloc[0] / (total_counts_classe_df['Total >= 10'].iloc[0] + total_counts_classe_df['Total < 10'].iloc[0])) * 100, (total_counts_classe_df['Total < 10'].iloc[0] / (total_counts_classe_df['Total >= 10'].iloc[0] + total_counts_classe_df['Total < 10'].iloc[0])) * 100]

                            # Create pie chart for current class with custom colors
                            fig_pie = px.pie(names=labels, values=values, title=f"Class: {classe}",
                                            color_discrete_sequence=colors)
                            st.plotly_chart(fig_pie)

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
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.write(total_counts_subclasse_df)

                    with col2:
                        fig_bar = px.bar(total_counts_subclasse_df, x='Sub Classe', y=['Total >= 10', 'Total < 10'],
                                        title='Total Counts of Moyenne >= 10 and <= 10 for Each Sub Classe',
                                        labels={'value': 'Count', 'variable': 'Note Ctrl 1'},
                                        color_discrete_map={'Total >= 10': 'green', 'Total < 10': 'red'},
                                        barmode='group')
                        fig_bar.update_layout(xaxis_title='Sub Classe', yaxis_title='Count')
                        st.plotly_chart(fig_bar)

                        colors = ['green', 'red']
                        
                        # Prepare DataFrame with required columns
                        total_percentage_sub_classe_moyenne_df = total_counts_subclasse_df[['Sub Classe','Percentage >= 10','Percentage < 10']]

                        # Plotting Sunburst chart with legend
                        fig = px.sunburst(total_percentage_sub_classe_moyenne_df, path=['Sub Classe', 'Percentage >= 10', 'Percentage < 10'], 
                                title='Percentage Moyenne >= 10 and Moyenne < 10 in each Classe',
                                labels={'Percentage >= 10': 'Percentage >= 10', 'Percentage < 10': 'Percentage < 10'})
                        st.plotly_chart(fig)


                        ################
                        # Iterate over each sub class
                        #for index, row in total_counts_subclasse_df.iterrows():
                            # Data for current sub class
                        #   labels = ["Percentage >= 10", "Percentage < 10"]
                        #   values = [row['Percentage >= 10'], row['Percentage < 10']]

                            # Create pie chart for current sub class with custom colors
                        #  fig_pie = px.pie(names=labels, values=values, title=f"Sub Classe: {row['Sub Classe']}",
                        #                  color_discrete_sequence=colors)
                        # st.plotly_chart(fig_pie)
                        #################

            else:
                for subclass in selected_subclasses:
                    total_counts_subclasse_df = filtered_data[filtered_data['Sub Classe'] == subclass].groupby('Sub Classe')['Moyenne'].agg([('Total >= 10', lambda x: (x >= 10).sum()), ('Total < 10', lambda x: (x < 10).sum())]).reset_index()

                    with st.expander(f"Eleves ayant note au dessus et au dessous la moyenne par Sous Classe: {subclass}", expanded=False):
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.write(total_counts_subclasse_df)

                        with col2:
                            fig_bar = px.bar(total_counts_subclasse_df, x='Sub Classe', y=['Total >= 10', 'Total < 10'],
                                            title=f'Total Counts of Moyenne >= 10 and <= 10 for Sous Classe: {subclass}',
                                            labels={'value': 'Count', 'variable': 'Moyenne'},
                                            color_discrete_map={'Total >= 10': 'green', 'Total < 10': 'red'},
                                            barmode='group')
                            fig_bar.update_layout(xaxis_title='Sub Classe', yaxis_title='Count')
                            st.plotly_chart(fig_bar)

                            colors = ['green', 'red']

                            # Data for current sub class
                            labels = ["Percentage >= 10", "Percentage < 10"]
                            values = [(total_counts_subclasse_df['Total >= 10'].iloc[0] / (total_counts_subclasse_df['Total >= 10'].iloc[0] + total_counts_subclasse_df['Total < 10'].iloc[0])) * 100, (total_counts_subclasse_df['Total < 10'].iloc[0] / (total_counts_subclasse_df['Total >= 10'].iloc[0] + total_counts_subclasse_df['Total < 10'].iloc[0])) * 100]

                            # Create pie chart for current sub class with custom colors
                            fig_pie = px.pie(names=labels, values=values, title=f"Sub Classe: {subclass}",
                                            color_discrete_sequence=colors)
                            st.plotly_chart(fig_pie)


# Requette 6: Notes Mentions
def requette_6(df):
    st.subheader("Mentions")

    # Define subqueries for request 6
    sub_queries = ['Répartition par Mention', 'Répartition de la Mention par Classe', 'Répartition de la Mention par Sous Classe']
    sub_query = st.sidebar.selectbox('Select Sub Query', sub_queries)
    main_container = st.container()
    with main_container:
        if sub_query == 'Répartition par Mention':
            st.subheader("Répartition par Mention")
            with st.expander("Répartition par Mention", expanded=False):
                count_mentions_df = df['Mention'].value_counts().reset_index()
                count_mentions_df.columns = ['Mention', 'Count']    
                col1, col2 = st.columns([1, 2])
                col3 = st.columns([8])[0]  # Full width for the third column
                
            
                with col1:
                    st.write(count_mentions_df)

                with col2:
                    fig_bar_mentions = px.bar(count_mentions_df, x='Mention', y='Count', title='Count of Mentions', 
                                        labels={'Mention': 'Mention', 'Count': 'Count'}, color='Mention',
                                        color_discrete_map={'Mention': 'darkblue'})
                    st.plotly_chart(fig_bar_mentions)

            
                with col3:
                    count_mentions_df['Percentage'] = (count_mentions_df['Count'] / count_mentions_df['Count'].sum()) * 100
                    fig_pie_mentions = px.pie(count_mentions_df, values='Percentage', names='Mention', title='Percentage Distribution of Mentions')
                    st.plotly_chart(fig_pie_mentions)
                        
    
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
                    col1, col2 = st.columns([1, 2])
                    col3 = st.columns([8])[0]  # Full width for the third column
                    with col1:
                        st.write(count_mention_by_classe_df)
                    with col2:
                        fig = px.bar(count_mention_by_classe_df, 
                            x='Mention', 
                            y='Count', 
                            color='Mention',
                            title='Count of Mentions by Classe',
                            barmode='group')
                        st.plotly_chart(fig)
                    with col3:
                        count_mention_by_classe_df['Percentage'] = (count_mention_by_classe_df['Count'] / count_mention_by_classe_df['Count'].sum()) * 100
                        count_mention_by_classe_df['Percentage'] = count_mention_by_classe_df['Percentage'].round(2)
                        fig_pie = px.pie(count_mention_by_classe_df, values='Percentage', names='Mention', title=f'Percentage Distribution of Mention for all classes')
                        st.plotly_chart(fig_pie)


                
                
            else:
                for classe in classes:
                    count_mention_by_classe_df = filtered_data[filtered_data['Classe'] == classe]['Mention'].value_counts().reset_index()
                    count_mention_by_classe_df.columns = ['Mention', 'Count']
                    count_mention_by_classe_df['Percentage'] = (count_mention_by_classe_df['Count'] / count_mention_by_classe_df['Count'].sum()) * 100
                    count_mention_by_classe_df['Percentage'] = count_mention_by_classe_df['Percentage'].round(2)

                    with st.expander(f"Classe: {classe}", expanded=False):
                        st.write(f"Classe: {classe}")

                        #col1, col2, col3 = st.columns([1, 1, 1])
                        col1, col2 = st.columns([1, 2])
                        col3 = st.columns([8])[0]  # Full width for the third column

                        with col1:
                            st.write(count_mention_by_classe_df)

                        with col2:
                            fig_mention_by_classe = px.bar(count_mention_by_classe_df, x='Mention', y='Count', 
                                                title=f'Count of Mentions for {classe}', 
                                                labels={'Mention': 'Mention', 'Count': 'Count'}, color='Mention',
                                                color_discrete_map={'Mention': 'darkblue'})
                            st.plotly_chart(fig_mention_by_classe)

                        with col3:
                            fig_pie_mention_by_classe = px.pie(count_mention_by_classe_df, values='Percentage', names='Mention', title=f'Percentage Distribution of Mentions for {classe}')
                            st.plotly_chart(fig_pie_mention_by_classe)

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
                    col1, col2 = st.columns([1, 2])
                    col3 = st.columns([8])[0]  # Full width for the third column
                    with col1:
                        st.write(count_mention_by_sub_classe_df)
                    with col2:
                        fig = px.bar(count_mention_by_sub_classe_df, 
                            x='Mention', 
                            y='Count', 
                            color='Mention',
                            title='Count of Mentions by Sub Classe',
                            barmode='group')
                        st.plotly_chart(fig)
                    with col3:
                        count_mention_by_sub_classe_df['Percentage'] = (count_mention_by_sub_classe_df['Count'] / count_mention_by_sub_classe_df['Count'].sum()) * 100
                        count_mention_by_sub_classe_df['Percentage'] = count_mention_by_sub_classe_df['Percentage'].round(2)
                        fig_pie = px.pie(count_mention_by_sub_classe_df, values='Percentage', names='Mention', title=f'Percentage Distribution of Mention for all sub classes')
                        st.plotly_chart(fig_pie)


                
                
            else:
                for sub_classe in sub_classes:
                    count_mention_by_sub_classe_df = filtered_data[filtered_data['Sub Classe'] == sub_classe]['Mention'].value_counts().reset_index()
                    count_mention_by_sub_classe_df.columns = ['Mention', 'Count']
                    count_mention_by_sub_classe_df['Percentage'] = (count_mention_by_sub_classe_df['Count'] / count_mention_by_sub_classe_df['Count'].sum()) * 100
                    count_mention_by_sub_classe_df['Percentage'] = count_mention_by_sub_classe_df['Percentage'].round(2)

                    with st.expander(f"Sub Classe: {sub_classe}", expanded=False):
                        st.write(f"Sub Classe: {sub_classe}")

                        #col1, col2, col3 = st.columns([1, 1, 1])
                        col1, col2 = st.columns([1, 2])
                        col3 = st.columns([8])[0]  # Full width for the third column

                        with col1:
                            st.write(count_mention_by_sub_classe_df)

                        with col2:
                            fig_mention_by_sub_classe = px.bar(count_mention_by_sub_classe_df, x='Mention', y='Count', 
                                                title=f'Count of Mentions for {sub_classe}', 
                                                labels={'Mention': 'Mention', 'Count': 'Count'}, color='Mention',
                                                color_discrete_map={'Mention': 'darkblue'})
                            st.plotly_chart(fig_mention_by_sub_classe)

                        with col3:
                            fig_pie_mention_by_sub_classe = px.pie(count_mention_by_sub_classe_df, values='Percentage', names='Mention', title=f'Percentage Distribution of Mentions for {sub_classe}')
                            st.plotly_chart(fig_pie_mention_by_sub_classe)


def top_students_by_subclass(df, subclass):
    # Filter the DataFrame for the specified subclass
    subclass_df = df[df['Sub Classe'] == subclass]

    # Sort the students by their average score (Moyenne) in descending order
    sorted_df = subclass_df.sort_values(by='Moyenne', ascending=False)

    # Extract the top 3 students for this subclass
    top_students_df = sorted_df.head(3)[['Code Massar','Nom et prénom', 'Moyenne', 'Sub Classe']]

    return top_students_df

def requette_7(df):
    st.subheader("Trois premiers éleves")
    # Get unique subclasses
    sub_classes = st.multiselect("Select Sub Classe", df['Sub Classe'].unique())

    # If no subclass is selected, return
    if not sub_classes:
        st.warning("Please select at least one Sub Classe.")
        return

    # Define custom colors
    custom_colors = px.colors.qualitative.Set2

    # If all subclasses are selected
    if set(sub_classes) == set(df['Sub Classe'].unique()):
        # Concatenate top students data for all subclasses
        top_students_all_df = pd.concat([top_students_by_subclass(df, subclass) for subclass in sub_classes])

        # Plotting the bar chart for all subclasses
        fig_all = px.bar(top_students_all_df, x='Nom et prénom', y='Moyenne', 
                         title=f'Top 3 Students for All Sub Classes',
                         labels={'Moyenne': 'Moyenne', 'Nom et prénom': 'Nom et prénom'},
                         color='Nom et prénom',  # Assign colors based on student names
                         color_discrete_sequence=custom_colors)
        
        # Display the DataFrame and plot within separate columns
        with st.expander(f"All Sub Classes", expanded=False):
            # Divide the space into two columns
            col1, col2 = st.columns([1, 2])

            # Col 1: DataFrame
            with col1:
                st.write("DataFrame:")
                st.write(top_students_all_df)

            # Col 2: Bar Plot
            with col2:
                st.write("Bar Plot:")
                st.plotly_chart(fig_all)
    else:
        # Iterate over each subclass and create plots
        for subclass in sub_classes:
            # Get the top students for the current subclass
            top_students = top_students_by_subclass(df, subclass)
            
            # Plotting the bar chart for the current subclass
            fig = px.bar(top_students, x='Nom et prénom', y='Moyenne', 
                         title=f'Top 3 Students for Sub Classe: {subclass}',
                         labels={'Moyenne': 'Moyenne', 'Nom et prénom': 'Nom et prénom'},
                         color='Nom et prénom',  # Assign colors based on student names
                         color_discrete_sequence=custom_colors)
            
            # Display the DataFrame and plot within separate columns
            with st.expander(f"Sub Classe: {subclass}", expanded=False):
                # Divide the space into two columns
                col1, col2 = st.columns([1, 2])

                # Col 1: DataFrame
                with col1:
                    st.write("DataFrame:")
                    st.write(top_students)

                # Col 2: Bar Plot
                with col2:
                    st.write("Bar Plot:")
                    st.plotly_chart(fig)



                
# Define the main function
def main():
    #st.title("Streamlit App")
    st.sidebar.title("Upload your data file")

    # File uploader in the sidebar
    uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=["xlsx"])

    data = load_data(uploaded_file)
    
    # Check if data is uploaded
    if not data.empty:
        st.sidebar.title("Queries")
        selected_query = st.sidebar.selectbox('Select Query', ['Age', 'Sexe', 'Nombre d\'élèves', 'Controle 1', 'Moyennes', 'Mentions', 'Trois premiers éleves'])

        if selected_query == 'Age':
            requette_1(data)
        elif selected_query == 'Sexe':
            requette_2(data)
        elif selected_query == 'Nombre d\'élèves':
            requette_3(data)
        elif selected_query == 'Controle 1':
            requette_4(data)
        elif selected_query == 'Moyennes':
            requette_5(data)
        elif selected_query == 'Mentions':
            requette_6(data)
        elif selected_query == 'Trois premiers éleves':
            requette_7(data)

if __name__ == '__main__':
    main()
