# Emergency Room Analytics Dashboard and AI Triage Pipeline

An interactive clinical data pipeline, simulation suite, and analytics dashboard built with Pandas and Streamlit to monitor and optimize emergency department workflows. This project processes over 10,000+ simulated patient logs to identify operational bottlenecks, track patient acuity splits, and streamline intake processing.

---

## Live Application

You can interact with the live, deployed dashboard directly in your browser here:  
**[Launch Live ER Analytics Dashboard](https://er-analytics-dashboard-fsna9qr99v494fqkvr9vl6.streamlit.app/)**

---

## Repository Structure

* **app.py** — The macro-level frontend analytics dashboard built with Streamlit. Tracks patient volume, length of stay, and operational bottlenecks.
* **triage_bot.py** — The micro-level point-of-care AI assistant. Simulates patient symptom intake, clinical categorization, and live acuity assignment.
* **generate_data.py** — The core data engine simulating realistic, high-throughput clinical logs.
* **er_patient_data.csv** — The comprehensive dataset driving the entire pipeline.

---

## Getting Started

### 1. Clone the repository
```bash
git clone [https://github.com/livarhassan-arch/er-analytics-dashboard.git](https://github.com/livarhassan-arch/er-analytics-dashboard.git)
cd er-analytics-dashboard
