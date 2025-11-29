from app import clean_text, process_language, MisinformationDetector, detect_sensationalism, generate_preliminary_prediction

# A short Marathi sentence (Devanagari) - "WHO is hiding the true source" style in Marathi
sample = "घुष्टी बातमी! WHO खरी स्त्रोत लपवत आहे, हे त्वरित वाचा"

print('Original:', sample)
# Do NOT clean before language detection - preserve original scripts
analysis_text, detected_lang = process_language(sample)
print('Detected language:', detected_lang)
print('Analysis text (pre-clean):', analysis_text)

# Now clean the English analysis_text for downstream analysis
cleaned = clean_text(analysis_text)
print('Cleaned (for analysis):', cleaned)
print('Detected language:', detected_lang)
print('Analysis text:', analysis_text)

md = MisinformationDetector()
misinfo_score = md.score(analysis_text)
print('Misinformation score:', misinfo_score)
sens = detect_sensationalism(analysis_text)
print('Sensationalism score:', sens)
verdict = generate_preliminary_prediction(misinfo_score, sens)
print('Preliminary verdict:', verdict)
