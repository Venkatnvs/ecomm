# chatbot_app/chatbot_logic.py
import spacy
from transformers import pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from store.models import Product
import torch

class ChatbotLogic:
    def __init__(self, request):
        self.request = request
        self.nlp = spacy.load("en_core_web_sm")
        self.sentiment_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment", framework="pt")
        self.vectorizer = CountVectorizer(lowercase=True)
        self.classifier = MultinomialNB()

        # Training data for intent classification
        self.training_data = [
            ("product", "Tell me about your products."),
            ("product", "What can I buy from you?"),
            ("service", "What services do you offer?"),
            ("service", "Tell me about your services."),
        ]
        self.labels, self.documents = zip(*self.training_data)
        self.vectorized_documents = self.vectorizer.fit_transform(self.documents)
        self.classifier.fit(self.vectorized_documents, self.labels)

    def classify_intent(self, message):
        vectorized_message = self.vectorizer.transform([message])
        intent = self.classifier.predict(vectorized_message)[0]
        return intent

    def process_user_message(self, message):
        state = self.get_user_state()
        intent = self.classify_intent(message)

        if intent == 'product':
            response = self.process_product_intent(message)
        elif intent == 'service':
            response = self.process_service_intent(message)
        else:
            response = "I'm sorry, I didn't understand that."

        sentiment = self.analyze_sentiment(message)
        named_entities = self.extract_named_entities(message)

        self.set_user_state(intent)
        return f"{response}\nSentiment: {sentiment}\nEntities: {named_entities}"

    def analyze_sentiment(self, message):
        sentiment_score = self.sentiment_analyzer(message)[0]['label']
        return sentiment_score.capitalize()

    def extract_named_entities(self, message):
        doc = self.nlp(message)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities

    def process_product_intent(self, message):
        if 'list' in message.lower():
            response = self.get_products_info()
        elif 'details' in message.lower():
            product_id = self.extract_named_entities(message)
            try :
                product_id = int(product_id[0][0])
            except Exception as e:
                product_id = None
            if product_id:
                response = self.get_product_info(product_id)
            else:
                response = "Please provide a valid product ID."
        else:
            response = "I'm here to help with product information. You can ask about the list of products or specific product details."

        return response

    def process_service_intent(self, message):
        pass
        # ... (your logic for service-related queries)

    def get_user_state(self):
        return self.request.session.get('user_state', 'init')

    def set_user_state(self, state):
        self.request.session['user_state'] = state

    def get_products_info(self):
        products = Product.objects.all()
        products_info = "\n".join([f"{product.id}. {product.name} - {product.new_price}" for product in products])
        return products_info
    
    def get_product_info(self, product_id):
        product = Product.objects.filter(id=product_id).first()
        if product:
            product_info = f"{product.name} - {product.new_price}\nDescription: {product.description}"
            return product_info
        return None