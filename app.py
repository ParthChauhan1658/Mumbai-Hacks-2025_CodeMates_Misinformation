import logging
import math
import re
from typing import Optional, List

import streamlit as st
from langdetect import detect, LangDetectException
try:
    from googletrans import Translator
except Exception:
    Translator = None

# Create a module-level Translator instance if available (reuse across calls)
translator = None
if Translator is not None:
    try:
        translator = Translator()
    except Exception:
        translator = None


def clean_text(input_text: str) -> str:
    """Clean and normalize input text:

    Steps:
    1. Lowercase
    2. Remove URLs (http, https, www)
    3. Remove punctuation but preserve letters in all scripts (keep spaces)
    4. Collapse multiple spaces
    """
    if not input_text:
        return ""

    text = input_text.lower()

    # remove URLs
    url_pattern = r"https?://\S+|www\.\S+"
    text = re.sub(url_pattern, "", text)

    # remove punctuation but preserve letters/digits across Unicode scripts
    # using \w (Unicode-aware) and keeping whitespace; underscores removed after
    text = re.sub(r"[^\w\s]", "", text, flags=re.UNICODE)
    # replace underscores introduced by \w with space
    text = text.replace("_", " ")

    # collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def truthlens_app():
    """Main Streamlit app for TruthLens: User Input Layer.

    Features:
    - Page config
    - Header
    - Large text area for user input (text, tweet, or news link)
    - 'Analyze Claim' button that captures input into `raw_input`
    - Display the captured input in an expander for verification
    """

    # Streamlit page configuration
    st.set_page_config(page_title="TruthLens", layout="wide")

    # Header
    st.title("TruthLens: Misinformation Analyzer")

    st.markdown(
        "Paste or type any text, tweet, or news link below. When ready, click 'Analyze Claim' to submit."
    )

    # Large text area for user input
    raw_text = st.text_area(
        "Enter text, tweet, or news link:", height=250, placeholder="Paste text, tweet, or a URL to a news article here..."
    )

    # Analyze button
    analyze = st.button("Analyze Claim")

    if analyze:
        # Capture input into variable `submitted_text`
        submitted_text = raw_text.strip()

        if not submitted_text:
            st.warning("No input detected. Please paste or type the claim you want to analyze.")
        else:
            # Preprocess and translate while preserving critical tokens/numbers
            processed_text, detected_lang = preprocessing_and_translation(submitted_text)

            # Show success and display the captured raw_input and analysis_text
            st.success("Claim submitted — ready for backend processing.")
            with st.expander("View submitted input"):
                st.write(submitted_text)

            # Display detection/translation results
            st.markdown(f"**Detected language:** {detected_lang}")
            st.markdown("**Text used for analysis (English):**")
            st.write(processed_text)

            # Core analysis: use improved analyze_text pipeline (includes sensitivity boosts)
            misinfo_score, sensationalism_score, preliminary = analyze_text(processed_text)

            st.subheader("Automated Analysis")
            st.metric("Misinformation score (0-1)", f"{misinfo_score:.2f}")
            st.metric("Sensationalism score (0-1)", f"{sensationalism_score:.2f}")
            st.markdown(f"**Preliminary prediction:** {preliminary}")

            # --- Fact verification layer (simulated) ---
            api_results = query_google_fact_check(processed_text)

            if api_results:
                st.subheader("External Fact-checks")
                for r in api_results:
                    st.markdown(f"- **{r['verdict']}** — [{r['title']}]({r['url']})")
            else:
                st.info("No matching external fact-checks found.")

            # Combine misinfo score with API results to compute final confidence and verdict
            final_confidence, final_verdict = calculate_confidence_score(misinfo_score, api_results)

            st.subheader("Fact Verification Result")
            st.metric("Final Confidence (0-100)", f"{final_confidence}")
            st.markdown(f"**Final verdict:** {final_verdict}")

            # Explanation generator and multilingual support
            english_summary = summarize_verified_facts(api_results, final_verdict)
            translations = generate_multilingual_explanation(english_summary)

            st.subheader("Explanation Summary")
            st.markdown("**English:**")
            st.write(english_summary)
            st.markdown("**Hindi (हिन्दी):**")
            st.write(translations.get("hi", "(translation unavailable)"))
            st.markdown("**Marathi (मराठी):**")
            st.write(translations.get("mr", "(translation unavailable)"))

            if api_results:
                st.subheader("Source links")
                for r in api_results:
                    st.write(f"- [{r['title']}]({r['url']}) — {r['verdict']}")


def process_language(text: str) -> tuple[str, str]:
    """Detect the language of `text`. If it's not English, translate it to English.

    Heuristics added:
    - If text contains Devanagari characters, prefer 'hi'/'mr' detection based on simple keyword checks.
    - Fall back to `langdetect.detect()` when needed.
    - Wrap detection and translation in try/except and return sensible defaults on error.

    Returns:
        analysis_text: the English text to use for downstream analysis
        detected_lang: ISO 639-1 language code detected for the original text
    """
    detected_lang = "unknown"
    analysis_text = text

    # Quick check for Devanagari script characters (covers Hindi, Marathi, Nepali, etc.)
    try:
        if text and re.search(r"[\u0900-\u097F]", text):
            # Heuristic: check for Marathi-specific words (simple list) to prefer 'mr'
            marathi_clues = ["आहे","नाही","लोकना","म्हणजे","मला","तुम्हाला"]
            lower = text.lower()
            if any(clue in lower for clue in marathi_clues):
                detected_lang = "mr"
            else:
                # Default to Hindi if Devanagari is present and Marathi clues not found
                detected_lang = "hi"
        else:
            # Fallback to langdetect
            try:
                detected_lang = detect(text)
            except Exception:
                detected_lang = "unknown"

        # Only translate if detected language is known and not English
        if detected_lang and detected_lang.lower() != "en" and detected_lang != "unknown":
            try:
                if translator is not None:
                    translated = translator.translate(text, src=detected_lang, dest="en")
                    analysis_text = translated.text
                else:
                    # translator unavailable; keep original
                    analysis_text = text
            except Exception:
                # translation failed; keep original text as fallback
                analysis_text = text
        else:
            analysis_text = text

    except Exception as e:
        # Any unexpected failure should not crash the app. Log to console and return originals.
        print(f"process_language error: {e}")
        detected_lang = detected_lang if detected_lang else "unknown"
        analysis_text = text

    return analysis_text, detected_lang


def preprocessing_and_translation(raw_input: str) -> tuple[str, str]:
    """Robust preprocessing and translation.

    - Preserve numerical sequences (dates, long numbers) and critical tokens by
      replacing them with placeholders before translation and restoring after.
    - Ensures critical tokens like 'indefinitely', 'closed', 'government' remain present
      in the English text used for analysis.

    Returns: (processed_english_text, detected_language)
    """
    if not raw_input:
        return "", "unknown"

    # tokens to preserve (case-insensitive)
    critical_tokens = [
        r"indefinitely",
        r"closed",
        r"government",
        r"lockdown",
        r"schools",
        r"withdraw",
        r"withdraw money",
        r"urgent",
        r"urgently",
        r"emergency",
    ]

    # find numeric sequences of length >=3 (dates like 01012025 or long IDs)
    num_pattern = re.compile(r"\d{3,}")
    nums = num_pattern.findall(raw_input)

    # prepare placeholders
    placeholder_map = {}
    tmp = raw_input
    for i, n in enumerate(nums):
        key = f"__NUM{i}__"
        placeholder_map[key] = n
        tmp = tmp.replace(n, key, 1)

    # protect critical tokens by simple placeholder replacement (longer phrases first)
    for i, tok in enumerate(sorted(critical_tokens, key=len, reverse=True)):
        prog = re.compile(re.escape(tok), flags=re.IGNORECASE)
        matches = list(prog.finditer(tmp))
        for j, m in enumerate(matches):
            key = f"__TK{i}_{j}__"
            placeholder_map[key] = tmp[m.start(): m.end()]
            tmp = tmp[: m.start()] + key + tmp[m.end():]

    # detect language and translate via existing process_language but on placeholder text
    try:
        translated_text, detected_lang = process_language(tmp)
    except Exception:
        translated_text, detected_lang = tmp, "unknown"

    # restore placeholders
    for key, val in placeholder_map.items():
        translated_text = translated_text.replace(key, val)

    # finally clean but ensure we don't strip numeric/date tokens
    processed = clean_text(translated_text)
    return processed, detected_lang


class MisinformationDetector:
    """Simple heuristic misinformation scorer.

    For the prototype we implement a lightweight heuristic:
    - Score is based on presence of words often seen in misinformation (e.g., 'false', 'hoax', 'conspiracy', 'hidden', 'coverup')
    - Longer texts dilute single-word signals; we normalize by length.
    """

    def __init__(self, suspicious_terms: Optional[List[str]] = None):
        if suspicious_terms is None:
            suspicious_terms = [
                "false",
                "hoax",
                "conspiracy",
                "hidden",
                "coverup",
                "fake",
                "exposed",
                "lying",
                # financial/hoax indicators
                "withdrawn",
                "bank",
                "account",
                "whatsapp",
                "scam",
                "modi",
                "important",

                # ADDED: Political / Election / Urgency / Health terms
                "election",
                "protest",
                "results",
                "tomorrow",
                "immediately",
                "fraud",
                "vote",
                "scandal",
                "corrupt",
                "who",
                "cure",
                "virus",
                "pandemic",
                "confirmed",
                "officially",
                "health",
            ]
        self.suspicious_terms = set(suspicious_terms)

    def score(self, text: str) -> float:
        if not text:
            return 0.0
        tokens = text.split()
        lower = text.lower()

        # count suspicious term occurrences as substrings to catch joined tokens (e.g., 'newsmodi')
        count = 0
        for term in self.suspicious_terms:
            if term in lower:
                count += lower.count(term)

        # Boost heuristic: look for sensational patterns that often indicate misinformation
        sensational_markers = [
            "urgent",
            "alert",
            "shocking",
            "you won't believe",
            "just confirmed",
            "has just confirmed",
            "breaking",
            "important news",
            "important",
        ]

        # financial markers increase suspicion
        financial_markers = ["withdrawn", "bank", "account", "5000", "rupees", "whatsapp", "transfer"]

        boost = 0.0
        if any(marker in lower for marker in sensational_markers):
            boost += 0.45
        if any(marker in lower for marker in financial_markers):
            boost += 0.35
        # if the claim mentions WHO or a government and sensational markers, increase suspicion further
        if ("who" in lower or "government" in lower or "modi" in lower) and any(marker in lower for marker in sensational_markers):
            boost += 0.2

        # compute density of suspicious terms in the text (count per token)
        # density is a clearer signal for short/high-signal texts than log-normalization
        token_count = max(1, len(tokens))
        base = float(count) / token_count

        score = base + boost
        # clamp between 0 and 1
        return float(max(0.0, min(1.0, score)))


def detect_sensationalism(text: str) -> float:
    """Detect sensationalism by counting high-intensity adjectives and urgency words.

    Returns a score between 0 and 1 indicating the strength of sensational language.
    """
    if not text:
        return 0.0

    sensational_terms = [
        "shocking",
        "urgent",
        "breaking",
        "unbelievable",
        "horrific",
        "shocker",
        "alert",
        "exclusive",
        "must read",
        "you won't believe",
        "hidden",
        "hiding",
        "important",
        "important news",
        "withdrawn",
        "bank",
        "whatsapp",
        "modi",
        # ADDED Urgency/Action Terms
        "protest",
        "immediately",
        "fake news alert",
        "crisis",
        "emergency",
    ]

    text_lower = text.lower()
    score = 0
    for term in sensational_terms:
        if term in text_lower:
            score += 1

    # normalize
    return min(1.0, score / len(sensational_terms))


def generate_preliminary_prediction(misinfo_score: float, sensationalism_score: float) -> str:
    """Combine misinfo score and sensationalism score to produce a provisional verdict.

    Simple rules:
    - If misinfo_score > 0.6 and sensationalism_score > 0.3 => 'Fake'
    - If misinfo_score < 0.3 and sensationalism_score < 0.3 => 'Real'
    - Otherwise => 'Unclear'
    """
    if misinfo_score > 0.6 and sensationalism_score > 0.3:
        return "Fake"
    if misinfo_score < 0.3 and sensationalism_score < 0.3:
        return "Real"
    return "Unclear"


def analyze_text(processed_text: str) -> tuple[float, float, str]:
    """Analyze text to produce misinformation and sensationalism scores with
    increased sensitivity for high-impact crisis keywords.

    This function uses the existing heuristic detectors as model stand-ins
    but applies the requested CRITICAL FIX: boosting scores when crisis keywords
    appear so that high-risk, unverified public-safety claims do not get a 0.0 score.
    """
    # Use existing heuristics as model proxies (replaceable with real models later)
    md = MisinformationDetector()
    misinfo_score = md.score(processed_text)
    sensationalism_score = detect_sensationalism(processed_text)

    # --- CRITICAL FIX IMPLEMENTATION: Increase Sensitivity ---
    crisis_keywords = [
        "schools closed",
        "lockdown",
        "government mandate",
        "withdraw money",
        "urgently",
        "emergency",
        "closed indefinitely",
        # health-related crisis keywords
        "who",
        "pandemic",
        "virus cure",
        "virus",
        "health",
        # ADDED Political/Election/Health Crisis Terms
        "election results fake",
        "protest immediately",
        "voting fraud",
        "who cure",
        "pandemic virus",
    ]

    lower = processed_text.lower()
    if any(keyword in lower for keyword in crisis_keywords):
        if misinfo_score < 0.70:
            misinfo_score = min(1.0, misinfo_score + 0.50)
        if sensationalism_score < 0.20:
            sensationalism_score = min(1.0, sensationalism_score + 0.20)

    # Generate preliminary prediction based on boosted scores
    if misinfo_score > 0.80 or sensationalism_score > 0.80:
        preliminary_prediction = "Fake"
    elif misinfo_score < 0.20 and sensationalism_score < 0.20:
        preliminary_prediction = "Real"
    else:
        preliminary_prediction = "Unclear"

    return misinfo_score, sensationalism_score, preliminary_prediction


def query_google_fact_check(claim_text: str) -> list:
    """Simulated Google Fact Check query.

    Returns a list of dicts with keys: 'verdict' (True/False/Mixed), 'url', 'title'.
    This is a placeholder that heuristically matches claims to mocked fact-checks.
    """
    results = []
    if not claim_text:
        return results

    lower = claim_text.lower()

    # Heuristic matches to simulate fact-check results
    if any(k in lower for k in ["fake", "hoax", "conspiracy", "coverup", "lying", "exposed"]):
        results.append({
            "verdict": "False",
            "url": "https://factcheck.google.com/claim-false",
            "title": "Google Fact Check: Claim found to be false",
        })

    # FIX: Updated WHO check to include health/cure/pandemic keywords
    if "who" in lower and any(k in lower for k in ["hiding", "hidden", "cure", "virus", "pandemic", "health", "confirmed"]):
        results.append({
            "verdict": "False",
            "url": "https://www.who.int/news/factcheck-cure-hoax",
            "title": "WHO Fact-check: No evidence for specific virus cure (Health Hoax)",
        })

    # ADD: PIB fact-check heuristic for government/finance related claims
    if any(k in lower for k in ["government", "modi", "finance", "subsidy", "bank account", "pension"]):
        results.append({
            "verdict": "False",
            "url": "https://pib.gov.in/factcheck-govt-scheme-hoax",
            "title": "PIB Fact Check: Government has not announced this scheme.",
        })

    if any(k in lower for k in ["vaccine", "vaccination"]):
        results.append({
            "verdict": "Mixed",
            "url": "https://example.com/factcheck-vaccine",
            "title": "Fact-check: Mixed evidence on vaccine claim",
        })

    # if nothing matched, return empty list (no external checks found)
    return results


def calculate_confidence_score(misinfo_score: float, api_results: list) -> tuple[int, str]:
    """Combine the internal misinfo_score (0-1) with external API results to produce
    a final confidence (0-100) and a final verdict (Fake/Real/Unclear).

    Strategy (prototype):
    - Internal component: misinfo_score weighted to 0-50
    - External component: based on fraction of 'False' results among API hits, mapped to 0-50
    - Final confidence = internal + external, clamped 0-100
    - Final verdict thresholds: >=66 -> Fake, <=33 -> Real, else Unclear
    """
    # Internal component (scaled 0-50)
    internal = float(misinfo_score) * 50

    # If there are no external results, keep a neutral external component
    if not api_results:
        # New behavior: when no external verification exists, rely more on internal
        # model signal. If the internal misinfo_score is high (>0.70) we treat the
        # claim as likely Fake with moderately high confidence (60-80).
        if misinfo_score > 0.70:
            # Map misinfo_score 0.70->60 up to 1.0->80 linearly
            span = max(0.0001, 1.0 - 0.70)
            final_score = int(min(80, max(60, round(60 + ((misinfo_score - 0.70) / span) * 20))))
            return final_score, "Fake"

        # otherwise keep a neutral external component as before
        external = 25.0  # neutral
        final_score = int(max(0, min(100, round(internal + external))))
        # map to verdict as before
        if final_score >= 66:
            final_verdict = "Fake"
        elif final_score <= 33:
            final_verdict = "Real"
        else:
            final_verdict = "Unclear"
        return final_score, final_verdict

    # Analyze external verdicts
    verdicts = [str(r.get("verdict", "")).lower() for r in api_results]
    has_false = any(v == "false" for v in verdicts)
    has_true = any(v == "true" for v in verdicts)
    has_mixed = any(v == "mixed" for v in verdicts)

    # Priority rules when external evidence exists
    if has_false and not has_true:
        # Strong external evidence of falsehood -> high confidence Fake
        return 95, "Fake"
    if has_true and not has_false:
        # Strong external evidence of truth -> high confidence Real
        return 95, "Real"
    if has_mixed and not (has_false or has_true):
        # Mixed external evidence only -> Unclear with medium confidence
        return 60, "Unclear"
    if has_false and has_true:
        # Contradictory external evidence -> Unclear
        return 60, "Unclear"

    # Fallback: compute weighted score from fraction of false among external
    total = len(api_results)
    false_count = sum(1 for r in api_results if str(r.get("verdict", "")).lower() == "false")
    external = (false_count / total) * 50.0

    final_score = int(max(0, min(100, round(internal + external))))
    if final_score >= 66:
        final_verdict = "Fake"
    elif final_score <= 33:
        final_verdict = "Real"
    else:
        final_verdict = "Unclear"

    return final_score, final_verdict


def summarize_verified_facts(api_results: list, final_verdict: str) -> str:
    """Generate a short English summary explaining the verification outcome.

    For 'Unclear' with mixed results, explain why evidence is mixed and cite sources.
    """
    if not api_results:
        return (
            "No external fact-checks were found for this claim. "
            "The analysis relies on internal signals which may indicate risk but external "
            "corroboration is unavailable."
        )

    verdicts = [str(r.get("verdict", "")).lower() for r in api_results]
    titles = [r.get("title", "source") for r in api_results]

    if final_verdict == "Unclear" and any(v == "mixed" for v in verdicts):
        # Build a mixed-evidence summary
        cites = ", ".join(titles[:2])
        return (
            f"Verification attempts show mixed evidence. Some sources ({cites}) provide partial or "
            f"conflicting information. While some safety data or context is available, the specific "
            f"claim lacks strong official confirmation, making the overall verdict unclear."
        )

    if final_verdict == "Fake":
        cites = ", ".join(titles[:2])
        return (
            f"External fact-checks (e.g., {cites}) contradict the claim. Available evidence indicates "
            f"the claim is false or unsupported. Proceed with caution and rely on verified sources."
        )

    if final_verdict == "Real":
        cites = ", ".join(titles[:2])
        return (
            f"External fact-checks (e.g., {cites}) support the claim or provide corroborating evidence. "
            f"The claim appears to be supported by available sources."
        )

    # Default fallback
    return "The verification result is unclear based on available data."


def generate_multilingual_explanation(english_summary: str) -> dict:
    """Translate the English summary into Hindi and Marathi.

    Uses the existing Translator; if translation fails, returns the English text as fallback.
    """
    out = {"en": english_summary}
    if translator is None:
        # Translator not available; return English text for fallbacks
        out["hi"] = english_summary
        out["mr"] = english_summary
        return out

    try:
        hi = translator.translate(english_summary, dest="hi").text
        out["hi"] = hi
    except Exception:
        out["hi"] = english_summary

    try:
        mr = translator.translate(english_summary, dest="mr").text
        out["mr"] = mr
    except Exception:
        out["mr"] = english_summary

    return out


if __name__ == "__main__":
    truthlens_app()
