"""
Main script to run the PageIndex RAG pipeline.

Usage:
    # Submit a new document
    python main.py --submit path/to/document.pdf
    
    # Query an existing document
    python main.py --doc-id <doc_id> --query "Your question here"
    
    # View document tree
    python main.py --doc-id <doc_id> --show-tree
"""

import argparse
from pageindex import utils
from document_processor import DocumentProcessor
from rag_pipeline import RAGPipeline


def main():
    parser = argparse.ArgumentParser(description="PageIndex RAG Pipeline")
    parser.add_argument("--submit", type=str, help="Path to PDF file to submit")
    parser.add_argument("--doc-id", type=str, help="Document ID to query")
    parser.add_argument("--query", type=str, help="Question to ask about the document")
    parser.add_argument("--show-tree", action="store_true", help="Display document tree structure")
    
    args = parser.parse_args()
    
    # Submit new document
    if args.submit:
        processor = DocumentProcessor()
        doc_id = processor.submit_document(args.submit)
        print(f"\nDocument ID: {doc_id}")
        print("Save this ID to query the document later.")
        
        if processor.is_ready(doc_id):
            tree = processor.get_tree(doc_id)
            print("\nDocument is ready! Tree structure:")
            utils.print_tree(tree)
        else:
            print("\nDocument is processing. Check back later.")
        return
    
    # Show tree structure
    if args.show_tree and args.doc_id:
        processor = DocumentProcessor()
        tree = processor.get_tree(args.doc_id)
        print("Document Tree Structure:")
        utils.print_tree(tree)
        return
    
    # Query document
    if args.doc_id and args.query:
        pipeline = RAGPipeline()
        pipeline.query(args.doc_id, args.query)
        return
    
    # No valid arguments
    parser.print_help()


if __name__ == "__main__":
    main()
