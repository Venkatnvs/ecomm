import spacy
from transformers import pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from store.models import Product,ProductMedia
import torch
import pandas as pd
from django.template.loader import get_template
from django.conf import settings
import os

class ChatbotLogic:
    def __init__(self, request):
        self.request = request
        self.nlp = spacy.load("en_core_web_sm")
        self.sentiment_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment", framework="pt")
        self.vectorizer = CountVectorizer(lowercase=True)
        self.classifier = MultinomialNB()
        file_path = os.path.join(settings.BASE_DIR,'data_files/training_data.csv')
        data = pd.read_csv(file_path)
        # print(data[0:5],file_path)
        X = self.vectorizer.fit_transform(data['Message'])
        y = data['Intent']
        self.classifier.fit(X, y)

    def classify_intent(self, message):
        vectorized_message = self.vectorizer.transform([message])
        intent = self.classifier.predict(vectorized_message)[0]
        return intent

    def process_user_message(self, message):
        state = self.get_user_state()
        intent = self.classify_intent(message)
        if state == 'init':
            response = self.generate_response("greeting", message)
        else:
            response = self.generate_response(intent, message)
        sentiment = self.analyze_sentiment(message)
        named_entities = self.extract_named_entities(message)

        self.set_user_state(intent)
        return f"{response}<br>Sentiment: {sentiment}<br>Entities: {named_entities}"

    def analyze_sentiment(self, message):
        sentiment_score = self.sentiment_analyzer(message)[0]['label']
        return sentiment_score.capitalize()

    def extract_named_entities(self, message):
        doc = self.nlp(message)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities

    def generate_response(self, intent, message):
        if intent == 'greeting':
            response = self.process_greeting_intent()
        elif intent == 'product':
            response = self.process_product_intent(message)
        elif intent == 'service':
            response = self.process_service_intent(message)
        else:
            response = "I'm sorry, I didn't understand that."
        return response

    def process_product_intent(self, message):
        if 'list' in message.lower():
            response = self.get_products_info()
        elif 'details' in message.lower():
            product_id = self.extract_product_id(message)
            response = self.get_product_info(product_id)
        else:
            response = "I'm here to help with product information. You can ask about the list of products or specific product details."
        return response
    
    def process_greeting_intent(self):
        return "Hello! How can I assist you today?"

    def extract_product_id(self, message):
        product_id = None
        entities = self.extract_named_entities(message)
        for entity, label in entities:
            if label == 'CARDINAL':
                try:
                    product_id = int(entity)
                    break
                except ValueError:
                    pass
        return product_id

    def process_service_intent(self, message):
        # Implement your logic for service-related queries
        pass

    def get_user_state(self):
        return self.request.session.get('user_state', 'init')

    def set_user_state(self, state):
        self.request.session['user_state'] = state

    def get_products_info(self):
        products = Product.objects.filter(is_active=True,subcategories__category__is_active=True,subcategories__is_active=True).reverse()[0:5]
        context = {
            "products":products,
            "heading":"Top 5 Products:"
        }
        products_info = get_template("chatapp/chatbot_fullpg/ans_snippets/all_products.html").render(context)
        return products_info
    
    def get_product_info(self, product_id):
        product = Product.objects.filter(id=product_id,is_active=True,subcategories__category__is_active=True,subcategories__is_active=True).first()
        if product:
            message_a = f'<a href="/product/{product.slug}" target="_blank"><img class="api-image" src="{product.first_img}" alt="{product.name}"/></a>'
            product_info = f"{product.pk}) {product.name} - {product.new_price}<br>{message_a}<br>Description: {product.description}"
            return product_info
        return "Product not found."