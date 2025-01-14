import streamlit as st
import pandas as pd

# Band levels and hourly rates
band_rates = {
    "Band 1 - Junior Analyst": 50,
    "Band 2 - Associate": 80,
    "Band 3 - Senior Associate": 120,
    "Band 4 - Manager": 150,
    "Band 5 - Director/Expert": 200
}

default_margin = 0.25  # 25%
activities = [f"Activity {i+1}" for i in range(10)]
sub_activities_dict = {
    "Activity 1": ["Design Phase", "Risk Assessment", "Documentation"],
    "Activity 2": ["Data Collection", "Patient Recruitment"],
    "Activity 3": ["Trial Monitoring", "Reporting"],
    "Activity 4": ["Data Analysis", "Validation"],
    "Activity 5": ["Regulatory Submission", "Compliance Check"],
    "Activity 6": ["Protocol Design"],
    "Activity 7": ["Site Selection", "Setup"],
    "Activity 8": ["Staff Training", "Ethics Review"],
    "Activity 9": ["Budget Planning", "Approval Processes"],
    "Activity 10": ["Audit and Quality Control"],
}

# Initialize session state for data storage
if 'data' not in st.session_state:
    data = []
    for activity in activities:
        for sub_activity in sub_activities_dict.get(activity, ["General Task"]):
            data.append({
                'Activity': activity,
                'Sub-Activity': sub_activity,
                'Band Level': 'Band 1 - Junior Analyst',
                'Hours': 10,
                'Margin': default_margin
            })
    st.session_state.data = pd.DataFrame(data)

# Function to calculate cost
def calculate_cost(row):
    rate = band_rates.get(row['Band Level'], 0)
    cost = row['Hours'] * rate
    total = cost * (1 + row['Margin'])
    return total

# Title
st.title("CRO Project Cost Estimation Tool with Sub-Activities")
st.write("Estimate costs for activities and sub-activities across 5 band levels.")

# Display Band Level Costs in an Info Box
band_cost_info = "\n".join([f"- **{band}**: ${rate}/hour" for band, rate in band_rates.items()])
st.info(f"### Band Level Costs\n{band_cost_info}")

# Sidebar - Add/Remove Sub-Activities
st.sidebar.header("Customize Sub-Activities")
selected_activity = st.sidebar.selectbox(
    "Select Main Activity", 
    activities, 
    key="main_activity_selector_sidebar"
)
new_sub_activity = st.sidebar.text_input(
    "Add Sub-Activity", 
    key="new_sub_activity_input"
)

if st.sidebar.button("Add Sub-Activity", key="add_sub_activity_button"):
    if new_sub_activity.strip() == "":
        st.sidebar.error("Sub-Activity name cannot be empty.")
    else:
        new_row = {
            'Activity': selected_activity,
            'Sub-Activity': new_sub_activity.strip(),
            'Band Level': 'Band 1 - Junior Analyst',
            'Hours': 5,
            'Margin': default_margin
        }
        st.session_state.data = pd.concat(
            [st.session_state.data, pd.DataFrame([new_row])], 
            ignore_index=True
        )
        st.sidebar.success(f"Added sub-activity '{new_sub_activity}' to {selected_activity}.")

# Editable Data Table
st.write("### Input Project Details")

# Loop through each row to allow Band Level changes
updated_data = []
for index, row in st.session_state.data.iterrows():
    # Show editable fields for each row
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        activity = row['Activity']
        st.text_input(f"Activity {index + 1}", activity, disabled=True)

    with col2:
        sub_activity = row['Sub-Activity']
        st.text_input(f"Sub-Activity {index + 1}", sub_activity, disabled=True)

    with col3:
        band_level = st.selectbox(
            f"Band Level {index + 1}", 
            list(band_rates.keys()), 
            index=list(band_rates.keys()).index(row['Band Level']),
            key=f"band_level_selectbox_{index}"  # Unique key using the row index
        )

    with col4:
        hours = st.number_input(
            f"Hours {index + 1}", 
            value=row['Hours'], 
            min_value=0, 
            step=1,
            key=f"hours_{index}"  # Unique key using the row index
        )

    with col5:
        margin = st.number_input(
            f"Margin {index + 1}", 
            value=row['Margin'], 
            min_value=0.0, 
            max_value=1.0, 
            step=0.01,
            key=f"margin_{index}"  # Unique key using the row index
        )

    # Append the updated row
    updated_data.append({
        'Activity': activity,
        'Sub-Activity': sub_activity,
        'Band Level': band_level,
        'Hours': hours,
        'Margin': margin
    })

# Update session state with the modified data
st.session_state.data = pd.DataFrame(updated_data)

# Calculate Total Cost
st.session_state.data['Total Cost'] = st.session_state.data.apply(calculate_cost, axis=1)

# Display Results
st.write("### Cost Breakdown by Sub-Activity")
st.dataframe(st.session_state.data)

# Summary
total_cost = st.session_state.data['Total Cost'].sum()
st.write(f"## Total Project Cost: ${total_cost:,.2f}")

# Visualization
st.write("### Cost Breakdown Visualization")
cost_summary = st.session_state.data.groupby('Activity')['Total Cost'].sum().reset_index()
st.bar_chart(cost_summary.set_index('Activity'))

# Download Button
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(st.session_state.data)
st.download_button(
    "Download Proposal as CSV",
    csv,
    "cro_cost_estimation.csv",
    "text/csv",
    key='download_csv_button'
)
