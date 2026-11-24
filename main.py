from pydantic import BaseModel, StrictStr, ValidationError, field_validator
from fastapi import FastAPI
import string
import os
import joblib


filepath = os.path.join('algorithm', 'algorithm.joblib')
algorithms = joblib.load(filepath)
loaded_vectorizer = algorithms['vectorizer']
loaded_log_regressor = algorithms['log_regressor']

def predict_sentiment(text, vectorizer, log_regressor):
    tfidf_text_matrix = vectorizer.transform([text, ])
    preds = log_regressor.predict(tfidf_text_matrix)
    if preds[0] == 1:
        return 'positive'
    else:
        return 'negative'

# print(predict_sentiment("That's was great!", loaded_vectorizer, loaded_log_regressor))
# print(predict_sentiment("Servers works so badly.", loaded_vectorizer, loaded_log_regressor))

class Text(BaseModel):
    text: StrictStr

    @field_validator('text')
    @classmethod
    def not_empty_string(cls, text: str) -> str:
        if len(text.strip()) == 0:
            raise ValueError("The text mustn't be an empty string")
        return text
    @field_validator('text')
    @classmethod
    def correct_symbols(cls, text: str) -> str:
        for c in text:
            if c.isalpha() and not (c in string.ascii_letters):
                raise ValueError("The text mustn't contain any letters outside the [a-zA-Z] range")
        return text

app = FastAPI()

@app.post('/predict')
def fastapi_handler(text: Text) -> dict:
    sent = predict_sentiment(text.text, loaded_vectorizer, loaded_log_regressor)
    return {'sentiment': sent}
