import os
from pageindex import PageIndexClient
from config import PAGEINDEX_API_KEY


class DocumentProcessor:
    """Handle document submission and processing with PageIndex."""
    
    def __init__(self):
        self.client = PageIndexClient(api_key=PAGEINDEX_API_KEY)
    
    def submit_document(self, pdf_path):
        """Submit a PDF document to PageIndex."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        print(f"Submitting PDF: {pdf_path}")
        doc_id = self.client.submit_document(pdf_path)["doc_id"]
        print(f"Document submitted with ID: {doc_id}")
        return doc_id
    
    def is_ready(self, doc_id):
        """Check if document is ready for retrieval."""
        return self.client.is_retrieval_ready(doc_id)
    
    def get_tree(self, doc_id, node_summary=True):
        """Get the tree structure of a document."""
        if not self.is_ready(doc_id):
            raise ValueError("Document is still processing. Please try again later.")
        
        return self.client.get_tree(doc_id, node_summary=node_summary)['result']
