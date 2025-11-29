# 🛡️ TruthLens: AI-Powered Misinformation Detector & Explainer

**Track: Misinformation | Event: MumbaiHacks 2025**
***Team: CodeMates*** | *Members: Bhumi Shetty, Parth Chauhan*

---

## 💡 The Problem We Solved

During crises (pandemics, elections, natural disasters), misinformation spreads rapidly on digital platforms. **People struggle to identify credible information**, leading to panic, mistrust, and **misinformation-driven harm** [1, 2]. We focused on building an easily accessible, real-time verification system to provide contextual explanations [2].

## 🎯 Our Objective & Solution

We built **TruthLens**, an **AI-powered system** designed to **detect, verify, and explain misinformation in real-time** [2].

### The Integrated AI Workflow [3]

TruthLens utilizes a multi-layered workflow to ensure reliability and speed:

1.  **AI Analyzer:** Uses **NLP models (BERT/RoBERTa/GPT)** to detect patterns of misinformation and performs Emotion & Sensationalism Detection.
2.  **Fact Verification:** Cross-checks claims with **trusted APIs** including **Google Fact Check, PIB, WHO, and Reuters**.
3.  **Explainable Verdict:** Delivers a clear prediction (**Fake / Real / Unclear**) with a **Confidence Score**.
4.  **Multilingual Support:** The Explanation Generator converts fact-check data into short, easy-to-understand summaries, supporting **English, Hindi, and Marathi**.

## ✨ Key Innovations

| Innovation | Function / Impact |
| :--- | :--- |
| **Crisis Stability Logic** | Priority logic ensures high-risk claims (e.g., hoaxes about bank closures [4, 5] or government subsidies [6, 7]) receive a high-confidence **Fake** verdict, even if internal AI scores are inconclusive, by prioritizing external validation (e.g., WHO, PIB [6, 8]). |
| **Cross-Platform Access** | Developing the solution for instant verification via a **Chrome extension** and **WhatsApp bot** [9]. |
| **Multilingual Explainer** | Full system support for **English, Hindi, and Marathi** summaries [3, 7, 10]. |
| **Trend Mapping** | Utilizes data stored in **MongoDB** to enable a **Misinformation Trend Map** for real-time regional insights [11]. |

## 💻 Prototype Demo

The current **Streamlit prototype** demonstrates the User Input Layer and the full analysis pipeline, resulting in a confidence score and a clear, multilingual explanation.

### Screenshot 1: Bank Hoax Analysis (Hindi Input)

*Demonstrates multilingual processing and internal score reliance when external checks fail.*

`[INSERT SCREENSHOT 1 IMAGE HERE]`

### Screenshot 2: Health Hoax Analysis (WHO Check)

*Demonstrates high-confidence verdict (95) based on external fact-check overriding internal scores.*

`[INSERT SCREENSHOT 2 IMAGE HERE]`

### Screenshot 3: Financial Hoax Analysis (PIB Check)

*Demonstrates external fact-check (PIB) overriding a low internal score (0.56) to lock the verdict to 95/Fake [6].*

`[INSERT SCREENSHOT 3 IMAGE HERE]`

## 🏗️ System Architecture & Technology Stack

| Component | Technologies Used |
| :--- | :--- |
| **Frontend (Prototype)** | Streamlit (Python) |
| **Core Logic** | Python, NLP Libraries |
| **AI / ML Models** | BERT / RoBERTa / GPT (Simulated Proxies) [3] |
| **Data Storage** | MongoDB (Used for Verified Claims & Trend Insights) [11] |
| **External Verification**| Google Fact Check API, PIB, WHO [3] |

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

TruthLens aims to go beyond a simple tool. With continued enhancement—including launching the **Chrome extension** and **WhatsApp bot**, and beginning **partnership** with verified fact-checkers [9]—this system can serve as a **national-level misinformation control platform**, enhancing public trust and encouraging responsible digital consumption [12].

---
*We're excited to build with innovation and impact at MumbaiHacks 2025! [12]*
