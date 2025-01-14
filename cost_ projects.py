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

def calculate_cost(row):
    rate = band_rates.get(row['Band Level'], 0)
    cost = row['Hours'] * rate
    total = cost * (1 + row['Margin'])
    return total

st.title("CRO Project Cost Estimation Tool with Sub-Activities")
st.write("Estimate costs for activities and sub-activities across 5 band levels.")

st.sidebar.header("Customize Sub-Activities")
selected_activity = st.sidebar.selectbox("Select Main Activity", activities)
new_sub_activity = st.sidebar.text_input("Add Sub-Activity")
if st.sidebar.button("Add Sub-Activity"):
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
        st.session_state.data 


# Initialize session state for sub-activities
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
    rate = band_rates[row['Band Level']]
    cost = row['Hours'] * rate
    total = cost * (1 + row['Margin'])
    return total


# Title
st.title("CRO Project Cost Estimation Tool with Sub-Activities")

# Description
st.write("This tool allows estimation of project costs for activities and sub-activities across 5 band levels.")

# Sidebar - Add/Remove Sub-Activities
st.sidebar.header("Customize Sub-Activities")

selected_activity = st.sidebar.selectbox("Select Main Activity", activities)

# Add a new sub-activity
new_sub_activity = st.sidebar.text_input("Add Sub-Activity")
if st.sidebar.button("Add Sub-Activity"):
    new_row = {
        'Activity': selected_activity,
        'Sub-Activity': new_sub_activity,
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
edited_data = st.data_editor(
    st.session_state.data,
    num_rows="dynamic",
    use_container_width=True
)

# Update session state
st.session_state.data = edited_data

# Calculate Costs
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
    key='download-csv'
)
