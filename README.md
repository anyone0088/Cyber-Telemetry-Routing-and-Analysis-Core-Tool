# C-TRACT: Cyber Telemetry Routing and Analysis Core Tool 🛡️

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Deployment](https://img.shields.io/badge/Deployment-Local_Offline-success.svg)
![Security](https://img.shields.io/badge/Security-LEA_Compliant-red.svg)

**A secure, offline-first intelligence suite designed for Law Enforcement Agencies (LEAs) and Cyber Crime Cells to parse, map, and cross-reference Call Detail Records (CDRs).**

---

## 📌 Overview
C-TRACT is an enterprise-grade tactical intelligence dashboard built to reduce investigative latency in cyber crime operations. Operating 100% locally to comply with strict evidentiary data privacy protocols, the suite automates the ingestion of raw telecom logs, isolates behavioral anomalies, and maps physical device perimeters to accelerate target profiling.

## 🚀 Core Investigative Modules
1. **Target Profiling:** Aggregates massive datasets to instantly surface high-frequency target nodes, equipment footprints (IMEI), and exact call volumetrics.
2. **Off-Hour Operations:** Isolates tactical communication signatures executing within restrictive night-time windows (23:00 - 05:00) to bypass standard background chatter.
3. **Cross-Log Link Analysis:** An advanced intersection engine that evaluates multiple suspect logs simultaneously to uncover hidden middlemen, handlers, and shared network entities.
4. **Geo-Perimeter Mapping:** Extracts Cell Tower IDs (CGI) to render interactive street-level maps with 2KM physical coverage radii, featuring direct integration with live Google Maps coordinates.
5. **Section 91 CrPC Automator:** Dynamically generates formatted, ready-to-print legal notices demanding KYC and CAF details from Nodal Officers based on flagged intelligence.

---

## 💻 Step-by-Step Installation (Linux Environment)

Because law enforcement handles highly sensitive data, this application is designed to run locally on an isolated workstation. **Internet access is only required for the initial installation.**

### Step 1: Clone the Repository
Download the intelligence suite to your local terminal.
```bash
git clone [https://github.com/YourUsername/Cyber-Telemetry-Routing-and-Analysis-Core-Tool.git](https://github.com/YourUsername/Cyber-Telemetry-Routing-and-Analysis-Core-Tool.git)
cd Cyber-Telemetry-Routing-and-Analysis-Core-Tool
Step 2: Initialize Secure Virtual Environment
Create an isolated Python environment to prevent system package conflicts.

Bash
python3 -m venv venv
source venv/bin/activate
Step 3: Install Required Dependencies
Install the required data engineering and visualization libraries.

Bash
pip install -r requirements.txt
⚙️ Step-by-Step Execution & Deployment
Step 4: Generate Synthetic Intelligence Data (For Testing)
Do not test the application with real case files. Use the integrated data synthesizer to create functionally accurate dummy CDRs containing artificial anomalies (scam bursts, shared middlemen).

Bash
python3 generate_data.py
This command will automatically generate two files (suspect_1_cdr.csv and suspect_2_cdr.csv) in your root directory.

Step 5: Launch the C-TRACT Engine
Spin up the local Streamlit server.

Bash
streamlit run app.py
The dashboard will initialize automatically in your default web browser at http://localhost:8501.

📋 Standard Operating Procedure (SOP) for Investigators
Once the dashboard is live, follow this workflow to analyze telecommunications data:

Case Initialization: On the left administrative sidebar, input the Investigating Officer (IO) Name, FIR/Case Reference, and Unit Designation.

Data Ingestion: * Click Browse Files in the sidebar.

To utilize the Cross-Log Link Analysis module, you must upload two or more CDR files simultaneously (hold Ctrl to select multiple files).

The ingestion gate will automatically map column formats from Jio, Airtel, or BSNL to the C-TRACT standard schema.

Triage & Review:

Review the Target Profiling tab for an immediate snapshot of the most contacted external numbers.

Check the Off-Hour Operations tab to identify suspect night-time activity.

If investigating a syndicate, navigate to the Multi-Log Link Analysis tab to instantly expose overlapping phone numbers operating between multiple targets.

Legal Execution: When a high-priority suspect number is identified, navigate to the Legal Notice Automator tab. Select the target TSP and phone number to instantly draft a formal Section 91 CrPC request, ready to be exported to official departmental letterhead.

⚠️ Disclaimer & Ethical Use
This software is developed strictly for authorized law enforcement, digital forensics, and academic cybersecurity research. Users are solely responsible for ensuring compliance with local data privacy laws (including the Indian DPDP Act) and departmental protocols when handling real-world telecommunications data.
