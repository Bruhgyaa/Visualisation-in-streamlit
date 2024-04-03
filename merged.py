import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# Load datasets
try:
    df1 = pd.read_csv("data/lastupdate-item360.csv")
    df2 = pd.read_csv("data/sitevisit.csv")
except FileNotFoundError:
    st.error("File not found. Please check the file paths.")
    st.stop()

# Sidebar for dataset selection
dataset_choice = st.sidebar.selectbox("Choose Dataset", ["Dataset 1", "Dataset 2"])

# Report section
st.header("Report Section")

if dataset_choice == "Dataset 1":
    st.subheader("Dataset 1 Analysis")

    # Filter data based on selected year
    selected_year = st.sidebar.selectbox('Select Year', df1['Year'].unique())
    df_filtered = df1[df1['Year'] == selected_year]

    # Visualization 1: Bar Plot using Plotly
    st.subheader("Bar Plot")
    project_counts = df_filtered['Project'].value_counts()
    bar_plot = px.bar(x=project_counts.index, y=project_counts.values,
                      labels={'x': 'Project', 'y': 'Count'},
                      title='Bookings per Project', color=project_counts.index,
                      color_discrete_sequence=px.colors.qualitative.Alphabet)
    st.plotly_chart(bar_plot)

    # Heatmap
    st.subheader('Heatmap: Bookings by Month and Project')
    heatmap = alt.Chart(df_filtered).mark_rect().encode(
        y=alt.Y('Month:O', axis=alt.Axis(title="Booking Date")),
        x=alt.X('Project:O', axis=alt.Axis(title="Project")),
        color=alt.Color('count():Q',
                        legend=alt.Legend(title="Count"),
                        ),
        stroke=alt.value('black'),
        strokeWidth=alt.value(0.25),
    ).properties(width=900
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    )
    st.altair_chart(heatmap)

    # Donut Chart
    st.subheader('PDC Status Distribution')
    pdc_counts = df_filtered['PDCStatus'].value_counts()
    donut_chart = px.pie(names=pdc_counts.index, values=pdc_counts.values,
                         title='PDC Status Distribution',
                         hole=0.3, color=pdc_counts.index)
    donut_chart.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(donut_chart)

    # Table Chart
    st.subheader('Summary Table: Sales Value and Sales Order Value by Month')
    summary_table = df_filtered.groupby(['Year', 'Month']).agg({'SalesValue': 'sum', 'SalesOrderValue': 'sum'}).reset_index()
    st.write(summary_table)

    # Report Section
    st.sidebar.title('Report')
    generate_report = st.sidebar.button('Generate Report')

    if generate_report:
        st.sidebar.subheader('Report Generated')
        st.sidebar.write('Here is the report based on the analysis:')
        
        st.sidebar.subheader('Bookings per Project')
        st.sidebar.write('The bar plot displays the distribution of bookings across different projects.')
        
        st.sidebar.subheader('Heatmap: Bookings by Month and Project')
        st.sidebar.write('The heatmap illustrates the distribution of bookings by month and project, providing insights into the booking trends over time.')
        
        st.sidebar.subheader('PDC Status Distribution')
        st.sidebar.write('The donut chart visualizes the distribution of PDC (Post-Dated Cheque) status, indicating the proportion of received and not received statuses.')
else:
    st.subheader("Dataset 2 Analysis")

    # Visualization 1: Bar Plot using Plotly
    st.subheader("Bar Plot")
    fig = px.bar(df2, x='sv_owner_name', y='Budget', color='purchasedetails_purpose')
    st.plotly_chart(fig, use_container_width=True)

    # Visualization 2: Heatmap using Altair
    st.subheader("Heatmap")
    # Skipping heatmap for now due to mixed data types causing errors

    # Visualization 3: Line Chart using Altair
    st.subheader("Line Chart")
    line_chart = alt.Chart(df2).mark_line().encode(
        x='sv_start_date_time',
        y='Budget',
        color='purchasedetails_purpose',
    ).properties(
        width=600,
        height=300
    )
    st.altair_chart(line_chart)

    # Visualization 4: Donut Chart using Plotly
    st.subheader("Donut Chart")
    fig = px.pie(df2, names='is_claim', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

    # Visualization 5: Table Chart using Pandas
    st.subheader("Table Chart")
    st.write(df2)


# Display a hyperlink
st.markdown("[Dataset Dashboad](http://localhost:8501/)")

