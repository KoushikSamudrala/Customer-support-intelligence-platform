import os
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

RAG_CHUNK_SIZE = 400
RAG_CHUNK_OVERLAP = 100
RAG_TOP_K = 5
EMBED_MODEL = "all-MiniLM-L6-v2"

# Gemini LLM Config
GEMINI_MODEL = "gemini-2.5-pro"
GEMINI_TEMPERATURE = 0.7
GEMINI_MAX_TOKENS = 1024




docs = [
    Document(page_content="Our return policy allows returns within 30 days of purchase with a receipt. Items must be in original condition.", metadata={"topic": "returns", "id": "doc_01"}),
    Document(page_content="We offer free shipping on orders over €50 within the EU; standard shipping is 3-5 business days.", metadata={"topic": "shipping", "id": "doc_02"}),
    Document(page_content="Warranty claims must include the order number and photos of the damaged product. Warranty period is 1 year.", metadata={"topic": "warranty", "id": "doc_03"}),
    Document(page_content="To update billing information, go to Account > Payment Methods and edit your card or add a new one.", metadata={"topic": "billing", "id": "doc_04"}),
    Document(page_content="You can track your shipment using the tracking link emailed after dispatch. Delivery exceptions may occur due to customs.", metadata={"topic": "tracking", "id": "doc_05"}),
    Document(page_content="Subscription plans can be upgraded or downgraded from the subscription page — changes take effect at next billing cycle.", metadata={"topic": "subscription", "id": "doc_06"}),
    Document(page_content="To cancel an order within 1 hour of placing it, contact support; after that we may not be able to stop fulfillment.", metadata={"topic": "cancellation", "id": "doc_07"}),
    Document(page_content="Refunds are issued to the original payment method within 5-10 business days after approval.", metadata={"topic": "refunds", "id": "doc_08"}),
    Document(page_content="Promotions and discount codes cannot be combined unless explicitly stated in the offer terms.", metadata={"topic": "discounts", "id": "doc_09"}),
    Document(page_content="International orders may incur customs fees; customers are responsible for import taxes and duties.", metadata={"topic": "international", "id": "doc_10"}),
    Document(page_content="Account verification may require a government ID for high-value purchases or to comply with regional regulations.", metadata={"topic": "account", "id": "doc_11"}),
    Document(page_content="We take customer privacy seriously — see our privacy policy for data handling, retention and deletion requests.", metadata={"topic": "privacy", "id": "doc_12"}),
]