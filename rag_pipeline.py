import json
from pageindex import utils
from document_processor import DocumentProcessor
from llm_client import call_llm


class RAGPipeline:
    """End-to-end RAG pipeline using PageIndex and Groq."""
    
    def __init__(self):
        self.doc_processor = DocumentProcessor()
        self.tree = None
        self.node_map = None
    
    def load_document(self, doc_id):
        """Load document tree structure."""
        print("Loading document tree...")
        self.tree = self.doc_processor.get_tree(doc_id)
        self.node_map = utils.create_node_mapping(self.tree)
        print(f"Document loaded with {len(self.node_map)} nodes")
        return self.tree
    
    def search_nodes(self, query):
        """Search for relevant nodes using LLM."""
        if self.tree is None:
            raise ValueError("No document loaded. Call load_document() first.")
        
        print(f"\nSearching for: {query}")
        
        # Remove text field for more efficient search
        tree_without_text = utils.remove_fields(self.tree.copy(), fields=['text'])
        
        search_prompt = f"""
You are given a question and a tree structure of a document.
Each node contains a node id, node title, and a corresponding summary.
Your task is to find all nodes that are likely to contain the answer to the question.

Question: {query}

Document tree structure:
{json.dumps(tree_without_text, indent=2)}

Please reply in the following JSON format:
{{
    "thinking": "<Your thinking process on which nodes are relevant to the question>",
    "node_list": ["node_id_1", "node_id_2", ..., "node_id_n"]
}}
Directly return the final JSON structure. Do not output anything else.
"""
        
        result = call_llm(search_prompt)
        
        # Strip markdown code blocks if present
        cleaned_result = result.strip()
        if cleaned_result.startswith("```json"):
            cleaned_result = cleaned_result[7:]
        if cleaned_result.startswith("```"):
            cleaned_result = cleaned_result[3:]
        if cleaned_result.endswith("```"):
            cleaned_result = cleaned_result[:-3]
        cleaned_result = cleaned_result.strip()
        
        search_result = json.loads(cleaned_result)
        
        print("\nReasoning:")
        utils.print_wrapped(search_result['thinking'])
        
        print("\nRelevant nodes found:")
        for node_id in search_result["node_list"]:
            node = self.node_map[node_id]
            print(f"  - Node {node['node_id']} (Page {node['page_index']}): {node['title']}")
        
        return search_result["node_list"]
    
    def retrieve_context(self, node_list):
        """Retrieve text content from selected nodes."""
        if self.node_map is None:
            raise ValueError("No document loaded. Call load_document() first.")
        
        relevant_content = "\n\n".join(
            self.node_map[node_id]["text"] for node_id in node_list
        )
        
        print(f"\nRetrieved {len(relevant_content)} characters of context")
        return relevant_content
    
    def generate_answer(self, query, context):
        """Generate answer using LLM based on retrieved context."""
        answer_prompt = f"""
Answer the question based on the context:

Question: {query}

Context: {context}

Provide a clear, concise answer based only on the context provided.
"""
        
        print("\nGenerating answer...")
        answer = call_llm(answer_prompt)
        return answer
    
    def query(self, doc_id, question):
        """Complete RAG pipeline: load, search, retrieve, and answer."""
        # Load document
        self.load_document(doc_id)
        
        # Search for relevant nodes
        node_list = self.search_nodes(question)
        
        # Retrieve context
        context = self.retrieve_context(node_list)
        
        # Generate answer
        answer = self.generate_answer(question, context)
        
        print("\n" + "="*80)
        print("ANSWER:")
        print("="*80)
        utils.print_wrapped(answer)
        print("="*80)
        
        return answer
