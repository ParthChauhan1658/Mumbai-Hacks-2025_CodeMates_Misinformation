# TruthLens — Misinformation Detector & Explainer (Prototype)

This is a minimal Streamlit prototype for TruthLens. It implements the User Input Layer (Priority 1 Feature 1): a page where users can paste or type text, tweets, or a news link and submit it for analysis.

Requirements

- Python 3.9+ (test with your environment)

Virtual environment (recommended)

You can create and activate a virtual environment named `.venv` and install dependencies. There is a helper PowerShell script included.

Using the helper script (PowerShell):

```powershell
.\setup_venv.ps1
```

# TruthLens — Misinformation Detector & Explainer (Prototype)

This is a minimal Streamlit prototype for TruthLens. It implements the User Input Layer (Priority 1 Feature 1): a page where users can paste or type text, tweets, or a news link and submit it for analysis.

Requirements

- Python 3.9+ (test with your environment)
 - Install dependencies:

 ```powershell
 python -m pip install -r requirements.txt
 ```



```powershell
python -m pip install -r requirements.txt
```

Run the app

```powershell
# from the project root
streamlit run app.py
```

Notes

- The current prototype captures user input into the variable `raw_input` when the "Analyze Claim" button is clicked and shows it inside an expander. This is intended as the input layer only; connect to the backend processing pipeline next.
