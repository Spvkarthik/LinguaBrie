import spacy
import streamlit as st
from spacy.lang.en.stop_words import STOP_WORDS as EN_STOP_WORDS
from spacy.lang.es.stop_words import STOP_WORDS as ES_STOP_WORDS
from spacy.lang.fr.stop_words import STOP_WORDS as FR_STOP_WORDS
from spacy.lang.de.stop_words import STOP_WORDS as DE_STOP_WORDS
from string import punctuation
from heapq import nlargest

# Load spaCy models for different languages
language_models = {
    "English": ("en_core_web_sm", EN_STOP_WORDS),
    "Spanish": ("es_core_news_sm", ES_STOP_WORDS),
    "French": ("fr_core_news_sm", FR_STOP_WORDS),
    "German": ("de_core_news_sm", DE_STOP_WORDS),
}

# User input for selecting language
language = st.selectbox("Select Language:", list(language_models.keys()))

# Load the selected language model and stop words
nlp_model, stopwords = language_models[language]
nlp = spacy.load(nlp_model)

# User input for text/paragraph
text = st.text_area(f"Enter your text or paragraph in {language}:")

# Asking for summarization percentage
percentage = st.number_input("Enter the percentage of summarization:", min_value=10, max_value=100, value=50, step=5)

# Check if the user has entered text
if text:
    doc = nlp(text)

    # Tokenize and calculate word frequencies
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            word_frequencies[word.text] = word_frequencies.get(word.text, 0) + 1

    # Normalize frequencies by the maximum frequency
    max_freq = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] = word_frequencies[word] / max_freq

    # Tokenize sentences and score them based on word frequencies
    sent_tokens = [sent for sent in doc.sents]
    sentence_scores = {}

    for sent in sent_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies:
                if sent not in sentence_scores:
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]

    # Select the top sentences for the summary
    select_length = int(len(sent_tokens) * percentage / 100)
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)

    # Display the summary on button click
    if st.button("Summarize"):
        st.subheader("Here is the summary:")
        summary_text = ' '.join([sent.text for sent in summary])
        st.write(summary_text)
