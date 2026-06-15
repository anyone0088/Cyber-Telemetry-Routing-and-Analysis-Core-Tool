import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

# -----------------------------------------
# TSP Data Standardization Pipeline
# -----------------------------------------
def standardize_cdr(file_object):
    """
    Parses raw CDR files from different Telecom Service Providers (TSPs)
    and standardizes them into a uniform schema for the analytical engine.
    """
    raw_df = pd.read_csv(file_object)
    columns = raw_df.columns.tolist()
    
    mapping_dictionary = {}
    
    # Reliance Jio Pattern
    if "A_Party_MSISDN" in columns:
        mapping_dictionary = {
            "A_Party_MSISDN": "Caller_Number",
            "B_Party_MSISDN": "Receiver_Number",
            "Call_Duration": "Duration_Sec",
            "CGI_ID": "Tower_Location",
            "Call_Date": "Date",
            "Call_Time": "Time"
        }
    # Bharti Airtel Pattern
    elif "Calling_No" in columns:
        mapping_dictionary = {
            "Calling_No": "Caller_Number",
            "Dialled_No": "Receiver_Number",
            "Duration": "Duration_Sec",
            "Cell_Name": "Tower_Location",
            "Start_Date": "Date",
            "Start_Time": "Time"
        }
        
    # Apply mapping if a known TSP pattern was detected
    if mapping_dictionary:
        raw_df = raw_df.rename(columns=mapping_dictionary)
        
    # Ensure critical numeric and time values are parsed safely
    if 'Duration_Sec' in raw_df.columns:
        raw_df['Duration_Sec'] = pd.to_numeric(raw_df['Duration_Sec'], errors='coerce')
    if 'Time' in raw_df.columns:
        # Extract the hour for off-hour analytics
        raw_df['Hour'] = pd.to_datetime(raw_df['Time'], format='%H:%M:%S', errors='coerce').dt.hour
        
    return raw_df

# -----------------------------------------
# Dashboard Configuration & Theme
# -----------------------------------------
st.set_page_config(page_title="Amroha Police Cyber Suite", layout="wide")
st.title("🛡️ Cyber Crime Cell - Advanced Intelligence & CDR Suite")
st.markdown("🔒 *Secure Local Deployment — Strict Data Privacy Conforming to Law Enforcement Protocols*")
st.markdown("---")

# -----------------------------------------
# Core Operational Sidebar
# -----------------------------------------
st.sidebar.header("📋 Case Administration")
officer_name = st.sidebar.text_input("Investigating Officer (IO)", value="IO Inspector Amroha")
case_number = st.sidebar.text_input("FIR / Case Reference Number", value="FIR No. 102/2026")
district_cell = st.sidebar.text_input("Unit/Cell", value="Cyber Crime Cell, Amroha")

st.sidebar.markdown("---")
st.sidebar.subheader("Data Ingestion Gate")
# Accept multiple files to support the cross-matching operations
uploaded_files = st.sidebar.file_uploader("Upload Raw CDR Logs (CSV)", type=["csv"], accept_multiple_files=True)

# -----------------------------------------
# Main Execution Engine
# -----------------------------------------
if uploaded_files:
    dataframes = []
    
    # Process each uploaded file through the ingestion pipeline
    for file in uploaded_files:
        temp_df = standardize_cdr(file)
        temp_df['Source_Case_File'] = file.name
        dataframes.append(temp_df)
        
    # Merge into a single master working dataset
    df = pd.concat(dataframes, ignore_index=True)
    
    # -----------------------------------------
    # High-Level Metric Telemetry Panel
    # -----------------------------------------
    total_records = len(df)
    distinct_callers = df['Caller_Number'].nunique()
    distinct_receivers = df['Receiver_Number'].nunique()
    
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("Total Rows Analyzed", total_records)
    m_col2.metric("Distinct Target Suspects", distinct_callers)
    m_col3.metric("Unique External Intersections", distinct_receivers)
    
    st.markdown("---")
    
    # -----------------------------------------
    # Primary Investigation Workspaces
    # -----------------------------------------
    tabs = st.tabs(["📊 Target Profiling", "🌙 Off-Hour Operations", "🚨 Multi-Log Link Analysis", "🗺️ Geo Perimeter Mapping", "📄 Legal Notice Automator"])
    
    # --- TAB 1: Target Profiling ---
    with tabs[0]:
        st.subheader("Frequency Analytics & Equipment Profiles")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Top Intercept Targets (Most Contacted)**")
            freq = df['Receiver_Number'].value_counts().head(10).reset_index()
            freq.columns = ['Phone Number', 'Total Interchanges']
            st.dataframe(freq, use_container_width=True)
            
        with col2:
            st.markdown("**Device Equipment Footprint (IMEI Logs)**")
            if 'IMEI' in df.columns:
                imei_df = df.groupby(['Caller_Number', 'IMEI']).size().reset_index(name='Calls Made')
                st.dataframe(imei_df, use_container_width=True)
            else:
                st.info("No IMEI column detected in these specific logs.")
            
        st.markdown("**Call Volumetric Chart**")
        # Ensure numbers render as labels, not mathematical values
        freq['Phone Number'] = freq['Phone Number'].astype(str)
        fig = px.bar(freq, x='Phone Number', y='Total Interchanges', template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    # --- TAB 2: Off-Hour Operations ---
    with tabs[1]:
        st.subheader("Restrictive Night-Time Call Profiles")
        st.caption("Isolates interactions executing between 23:00 (11 PM) and 05:00 (5 AM).")
        
        if 'Hour' in df.columns:
            night_logs = df[(df['Hour'] >= 23) | (df['Hour'] <= 5)]
            if not night_logs.empty:
                st.error(f"Flagged {len(night_logs)} anomalies within off-hour windows.")
                st.dataframe(night_logs[['Date', 'Time', 'Caller_Number', 'Receiver_Number', 'Duration_Sec', 'Tower_Location']], use_container_width=True)
            else:
                st.success("No anomalies matching off-hour criteria discovered.")
        else:
            st.warning("Time column missing or unreadable. Cannot process off-hour analytics.")

    # --- TAB 3: Multi-Log Link Analysis ---
    with tabs[2]:
        st.subheader("Cross-Log Identity Intersection Engine")
        st.caption("Automatically extracts common entities across distinct source case files to identify shared co-conspirators.")
        
        if len(uploaded_files) > 1:
            # Group receivers by the files they appear in
            links = df.groupby('Receiver_Number')['Source_Case_File'].nunique().reset_index()
            intercepts = links[links['Source_Case_File'] > 1]
            
            if not intercepts.empty:
                st.warning(f"Identified {len(intercepts)} overlapping phone number intersections between separate files!")
                common_nums = intercepts['Receiver_Number'].tolist()
                match_details = df[df['Receiver_Number'].isin(common_nums)]
                st.dataframe(match_details[['Receiver_Number', 'Caller_Number', 'Source_Case_File', 'Date', 'Time']], use_container_width=True)
            else:
                st.success("Clean Matrix: No overlapping external links found between these files.")
        else:
            st.info("To run cross-matching operations, select and upload multiple CDR CSV files simultaneously via the sidebar panel.")

    # --- TAB 4: Geo Perimeter Mapping ---
    with tabs[3]:
        st.subheader("Geographic Tower Coverage Perimeter")
        
        tower_database = {
            "Amroha Sector 2": [28.9044, 78.4675],
            "Joyo Road Close": [28.9100, 78.4700],
            "Gajraula Highway": [28.8450, 78.2340],
            "Kanth Crossroad": [29.0550, 78.6250]
        }
        
        if 'Tower_Location' in df.columns:
            active_towers = df['Tower_Location'].dropna().unique()
            m = folium.Map(location=[28.9044, 78.4675], zoom_start=11)
            
            for tower in active_towers:
                if tower in tower_database:
                    coords = tower_database[tower]
                    g_url = f"https://www.google.com/maps/search/?api=1&query={coords[0]},{coords[1]}"
                    
                    popup_html = f"""
                    <div style='font-family: Arial, sans-serif; font-size: 13px; width: 200px;'>
                        <strong>Tower:</strong> {tower}<br><br>
                        <a href='{g_url}' target='_blank' style='display:block; text-align:center; padding:6px; background-color:#1a73e8; color:white; border-radius:4px; text-decoration:none; font-weight:bold;'>Open in Google Maps</a>
                    </div>
                    """
                    
                    folium.Marker(location=coords, popup=folium.Popup(popup_html, max_width=250), icon=folium.Icon(color="red", icon="tower")).add_to(m)
                    folium.Circle(location=coords, radius=2000, color="#1a73e8", fill=True, fill_opacity=0.15).add_to(m)
                    
            st_folium(m, width=1100, height=550)
        else:
            st.warning("No Tower Location data available in this file to map.")

    # --- TAB 5: Legal Notice Automator ---
    with tabs[4]:
        st.subheader("Section 91 CrPC Legal Notice Drafter")
        st.caption("Instantly compiles ready-to-print legal notices for Nodal Officers based on data insights.")
        
        col_form, col_preview = st.columns([1, 2])
        
        with col_form:
            target_tsp = st.selectbox("Select Target Provider (TSP)", ["Reliance Jio Infocomm Ltd", "Bharti Airtel Ltd", "Bharat Sanchar Nigam Limited (BSNL)", "Vodafone Idea Ltd"])
            flagged_number = st.selectbox("Select Target Number to Investigate", df['Receiver_Number'].dropna().unique())
            
            # Safely grab the first date available as a default
            default_date = df['Date'].iloc[0] if 'Date' in df.columns and not df.empty else "DD-MM-YYYY"
            evidence_date = st.text_input("Date of Offense Match", value=default_date)
            
        with col_preview:
            st.markdown("**Document Preview (Copy text for official letterhead)**")
            
            notice_text = f"""
OFFICE OF THE INVESTIGATING OFFICER
{district_cell.upper()}, UTTAR PRADESH

Ref No: AMR/{case_number.replace(' ', '_')}/2026
Date: 15-06-2026

To,
The Nodal Officer,
{target_tsp},
Uttar Pradesh Regulatory Zone.

SUBJECT: NOTICE UNDER SECTION 91 OF THE CODE OF CRIMINAL PROCEDURE (CrPC), 1973 FOR PROVISION OF SUBSCRIBER DETAIL INFORMATION.

In connection with the investigation of case number {case_number}, it has come to light that mobile connection number (+91) {flagged_number} is critically associated with cyber fraud activities logged within our jurisdiction on or around {evidence_date}.

Therefore, by virtue of powers vested in me under Section 91 of CrPC, you are hereby directed to provide the following subscriber details immediately to this office via secure channels:
1. Certified Subscriber Application Form (CAF) & Registered KYC Documents.
2. Complete Permanent Address Verification Files.
3. Linked Payment Instrument, Bank Account, or UPI Details used during account provisioning.

Treat this as time-sensitive operational evidence. Non-compliance will attract legal penal actions under relevant sections of the Bharatiya Nyaya Sanhita (BNS).

Signed,

({officer_name})
Investigating Officer, {district_cell}
            """
            st.text_area("Official Template Workspace", value=notice_text.strip(), height=420)

else:
    st.info("System Ready. Ingest raw CSV log data through the administrative sidebar to begin operations.")
