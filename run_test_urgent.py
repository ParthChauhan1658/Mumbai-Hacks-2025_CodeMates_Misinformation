from app import clean_text, process_language, MisinformationDetector, detect_sensationalism, generate_preliminary_prediction, query_google_fact_check, calculate_confidence_score

sample = "urgent alert the who has just confirmed that the new virus is spreading rapidly"

print('Original:', sample)
# Do not clean before language detection
analysis_text, detected_lang = process_language(sample)
print('Detected language:', detected_lang)
print('Analysis text (pre-clean):', analysis_text)

cleaned = clean_text(analysis_text)
print('Cleaned (for analysis):', cleaned)

md = MisinformationDetector()
misinfo_score = md.score(cleaned)
print('Misinformation score:', misinfo_score)

sens = detect_sensationalism(cleaned)
print('Sensationalism score:', sens)

prelim = generate_preliminary_prediction(misinfo_score, sens)
print('Preliminary verdict:', prelim)

api_results = query_google_fact_check(cleaned)
print('API results:', api_results)

final_confidence, final_verdict = calculate_confidence_score(misinfo_score, api_results)
print('Final confidence:', final_confidence)
print('Final verdict:', final_verdict)
