# 🛡️ TruthLens: AI-Powered Misinformation Detector & Explainer

**Track: Misinformation | Event: MumbaiHacks 2025**
***Team: CodeMates***

---

## 💡 The Problem We Solved

During crises (pandemics, elections, natural disasters), misinformation spreads rapidly on digital platforms. **People struggle to identify credible information**, leading to panic, mistrust, and **misinformation-driven harm**. We focused on building an easily accessible, real-time verification system to provide contextual explanations.

## 🎯 Our Objective & Solution

We built **TruthLens**, an **AI-powered system** designed to **detect, verify, and explain misinformation in real-time**, focusing on high-impact claims spread during crises.

### The Integrated AI Workflow

TruthLens utilizes a multi-layered workflow to ensure reliability and speed:

1.  **AI Analyzer:** Uses NLP models (BERT/RoBERTa/GPT) to detect patterns of misinformation and performs Emotion & Sensationalism Detection.
2.  **Fact Verification:** Cross-checks claims with trusted APIs including Google Fact Check, PIB, WHO, and Reuters.
3.  **Explainable Verdict:** Delivers a clear prediction (**Fake / Real / Unclear**) with a **Confidence Score**.
4.  **Multilingual Support:** The Explanation Generator converts fact-check data into short, easy-to-understand summaries, supporting **English, Hindi, and Marathi**.

## ✨ Key Innovations

| Innovation | Function / Impact |
| :--- | :--- |
| **Crisis Stability Logic** | Priority logic ensures high-risk claims (e.g., hoaxes about bank closures or government subsidies) receive a high-confidence **Fake** verdict, even if internal AI scores are inconclusive, by prioritizing external validation (e.g., WHO, PIB). |
| **Cross-Platform Access** | Developing the solution for instant verification via a **Chrome extension** and **WhatsApp bot**. |
| **Multilingual Explainer** | Full system support for **English, Hindi, and Marathi** summaries throughout the analysis pipeline. |
| **Trend Mapping** | Utilizes data stored in MongoDB to enable a **Misinformation Trend Map** for real-time regional insights. |

## 💻 Prototype Demo: High-Confidence Verification

The current **Streamlit prototype** successfully implements the core AI workflow, demonstrating how TruthLens handles various types of high-risk claims.

### Demo 1: Multilingual Bank Hoax (Internal Reliance)

*   **Input:** Hindi text ("अगले 48 घंटों में, सभी बैंक अनिश्चित काल के लिए बंद हो जाएंगे...")
*   **Result Highlight:** Successfully detects Hindi input, translates for analysis, and assigns a high initial score (Misinfo Score **0.93**). Since no external checks were found, the system still confidently flags the high-risk claim with **Final Confidence 76 / Fake**, relying on the internal crisis logic.

<p align="center">
  <img src="assets/demo 1.png" alt="TruthLens Analysis of Multilingual Bank Hoax - Final Confidence 76" width="600"/>
</p>

### Demo 2: Financial Hoax Override (PIB Validation)

*   **Input:** English text ("The Government of India is giving 5000 rupees subsidy... Send your account details immediately on WhatsApp...")
*   **Result Highlight:** The AI Analyzer gave a moderate initial score (**0.56 / Unclear**), but the Fact Verification Layer immediately found a **PIB Fact Check: False** result. This external evidence **overrode** the internal score, locking the verdict to **Final Confidence 95 / Fake**, demonstrating the stability logic in action.

<p align="center">
  <img src="assets/demo 2.png" alt="TruthLens Financial Hoax Override - PIB Validation" width="600"/>
</p>

### Demo 3: Health Crisis Verification (WHO Validation)

*   **Input:** English text ("Drinking hot salt water cures the pandemic virus confirmed by the WHO.")
*   **Result Highlight:** The system quickly identifies the claim, finds a corresponding **WHO Fact-check: False** result, and delivers the highest confidence verdict: **Final Confidence 95 / Fake**, complete with source links and multilingual explanations.

<p align="center">
  <img src="assets/demo 3.png" alt="TruthLens Health Crisis Verification - WHO Validation" width="600"/>
</p>

## 🏗️ System Architecture & Technology Stack

| Component | Technologies Used |
| :--- | :--- |
| **Frontend (Prototype)** | Streamlit (Python) |
| **Core Logic** | Python, NLP Libraries |
| **AI / ML Models** | BERT / RoBERTa / GPT (Simulated Proxies) |
| **Data Storage** | MongoDB (Used for Verified Claims & Trend Insights) |
| **External Verification**| Google Fact Check API, PIB, WHO |

## 🚀 Getting Started

This repository contains the minimal Streamlit prototype (`app.py`) for the TruthLens project.

### Requirements

-   **Python 3.9+**
-   Dependencies listed in `requirements.txt`

### Setup and Running

1.  **Clone the repository:**
    ```bash
    git clone [Your-Repo-Link]
    cd TruthLens
    ```
2.  **Install dependencies (Virtual environment recommended):**
    ```powershell
    python -m venv .venv
    .\.venv\Scripts\activate # On Windows/PowerShell
    # source .venv/bin/activate # On macOS/Linux
    python -m pip install -r requirements.txt
    ```
3.  **Run the Streamlit application:**
    ```powershell
    streamlit run app.py
    ```

## 📈 Future Vision

TruthLens aims to go beyond a simple tool. With continued enhancement—including launching the **Chrome extension** and **WhatsApp bot**, and establishing **partnership** with verified fact-checkers—this system is poised to serve as a **national-level misinformation control platform**, enhancing public trust and encouraging responsible digital consumption.

---
*We are excited to build with innovation and impact at MumbaiHacks 2025!*





