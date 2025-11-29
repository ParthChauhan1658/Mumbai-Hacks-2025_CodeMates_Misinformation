from app import clean_text, process_language, MisinformationDetector, detect_sensationalism, generate_preliminary_prediction

sample = "SHOCKING news!!! The WHO is hiding the true source of the outbreak: read this urgent report http://bad.url/urgent-report"

print('Original:', sample)
cleaned = clean_text(sample)
print('Cleaned:', cleaned)
analysis_text, detected_lang = process_language(cleaned)
print('Detected language:', detected_lang)
print('Analysis text:', analysis_text)

md = MisinformationDetector()
misinfo_score = md.score(analysis_text)
print('Misinformation score:', misinfo_score)

sens = detect_sensationalism(analysis_text)
print('Sensationalism score:', sens)

verdict = generate_preliminary_prediction(misinfo_score, sens)
print('Preliminary verdict:', verdict)
