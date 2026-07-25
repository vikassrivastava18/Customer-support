from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

documents = [
    Document(
        page_content=f"""
            Company Overview
                • BookLeaf Publishing is a self-publishing company operating in India and the US.
                • We offer publishing packages: Standard Free (no upfront cost) and Bestseller Breakthrough
                (premium, paid package with marketing and distribution add-ons).
                • We handle cover design, typesetting, ISBN assignment, printing, distribution, and royalty
                management for our authors.
                • Our in-house printing facility and warehouse are located in Delhi. We also work with print partners
                including Repro India and Epitome Books.
            """
    ),
    Document(
        page_content=f"""
            Royalty Policy
                • BookLeaf follows an 80/20 royalty split: 80% of the net profit per book goes to the author, 20% to
                BookLeaf.
                • Net profit = MRP minus printing cost, platform commission (Amazon/Flipkart), and shipping charges.
                • Royalties are calculated quarterly and paid within 45 days of the quarter ending.
                • Minimum payout threshold: ₹1,000. If accumulated royalties are below this, they roll over to the next
                quarter.
                • Payouts are made via bank transfer to the account linked in the author’s dashboard.
                • Authors can view a detailed royalty breakdown in their dashboard, showing sales figures per
                platform.
            """
    ),
    Document(
        page_content=f"""
            ISBN Policy
                • Every book published through BookLeaf receives a unique ISBN assigned by BookLeaf.
                • ISBNs are registered under BookLeaf’s publisher imprint. If an author wants an ISBN under their
                own imprint, they need to obtain it independently.
                • If an author reports an ISBN error (duplicate, wrong book linked), it is treated as a high-priority issue
                and escalated to the production team.
            """
    ),
    Document(
        page_content=f"""
        Printing & Quality
            • In-house printing handles most orders. Overflow or specific format requirements go to Repro India
            or Epitome Books.
            • Standard print turnaround: 5–7 business days from order confirmation.
            • If an author reports a quality issue (misprints, binding defects, color inconsistency), BookLeaf
            arranges a free reprint after verification. The author may need to share photos of the defective copy.
        """
    ),
    Document(
        page_content=f"""
        Distribution & Availability
            • Books are listed on Amazon India, Flipkart, Amazon US, Amazon UK, and the BookLeaf Store.
            • New listings typically go live within 7–10 business days after publication is complete.
            • If a book is showing as unavailable on a platform, it usually indicates a stock sync issue—
            BookLeaf’s team can trigger a re-sync within 24–48 hours.
        """
    ),
    Document(
        page_content=f"""
        Production Stages
            • A book goes through the following stages: Manuscript Received → Editing (if opted) → Cover
            Design → Typesetting → Proofreading → ISBN Assignment → Printing → Distribution Setup →
            Published & Live.
            • Authors are updated at each stage via email. Delays typically happen at Cover Design (waiting for
            author approval) and Proofreading (revision rounds).
        """
    ),
]

def similarity_search(query):
    # get the info chunks
    chunks = documents

    # Create in-memory vector store (FAISS)
    vector_store = FAISS.from_documents(chunks, embeddings)

    # perform similarity search with score
    results = vector_store.similarity_search_with_score(query, k=5)

    # unpack result
    doc, dist = results[0]
    context = doc.page_content

    return {
        "context": context,
        "distance": float(dist)
    }