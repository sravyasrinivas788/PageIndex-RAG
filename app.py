import streamlit as st
import os
import time
from document_processor import DocumentProcessor
from rag_pipeline import RAGPipeline

st.set_page_config(
    page_title="PageIndex RAG Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 PageIndex RAG Assistant")
st.markdown("Upload PDF documents and ask questions using AI-powered retrieval")

if 'doc_processor' not in st.session_state:
    st.session_state.doc_processor = DocumentProcessor()
    st.session_state.pipeline = RAGPipeline()

if 'documents' not in st.session_state:
    st.session_state.documents = {}

if 'current_doc_id' not in st.session_state:
    st.session_state.current_doc_id = None

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

col1, col2 = st.columns([1, 2])

with col1:
    st.header("📄 Document Management")
    
    uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])
    
    if uploaded_file is not None:
        if st.button("Submit Document", type="primary"):
            with st.spinner("Uploading and processing document..."):
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                try:
                    doc_id = st.session_state.doc_processor.submit_document(temp_path)
                    st.session_state.documents[doc_id] = {
                        'name': uploaded_file.name,
                        'status': 'processing'
                    }
                    st.session_state.current_doc_id = doc_id
                    st.success(f"Document submitted! ID: {doc_id}")
                    
                    with st.spinner("Waiting for processing to complete..."):
                        max_wait = 60
                        waited = 0
                        while waited < max_wait:
                            if st.session_state.doc_processor.is_ready(doc_id):
                                st.session_state.documents[doc_id]['status'] = 'ready'
                                st.success("✅ Document is ready for querying!")
                                break
                            time.sleep(2)
                            waited += 2
                        else:
                            st.warning("Document is still processing. Check back in a moment.")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
    
    st.divider()
    
    st.subheader("📋 Your Documents")
    if st.session_state.documents:
        for doc_id, info in st.session_state.documents.items():
            status_icon = "✅" if info['status'] == 'ready' else "⏳"
            if st.button(f"{status_icon} {info['name']}", key=doc_id):
                st.session_state.current_doc_id = doc_id
                st.session_state.chat_history = []
                st.rerun()
    else:
        st.info("No documents uploaded yet")
    
    if st.session_state.current_doc_id:
        st.divider()
        current_doc = st.session_state.documents.get(st.session_state.current_doc_id)
        if current_doc:
            st.success(f"**Active:** {current_doc['name']}")
            
            if st.button("🔄 Check Status"):
                is_ready = st.session_state.doc_processor.is_ready(st.session_state.current_doc_id)
                if is_ready:
                    st.session_state.documents[st.session_state.current_doc_id]['status'] = 'ready'
                    st.success("Document is ready!")
                else:
                    st.warning("Still processing...")
            
            if st.button("🌳 View Document Tree"):
                if current_doc['status'] == 'ready':
                    with st.spinner("Loading tree structure..."):
                        tree = st.session_state.doc_processor.get_tree(st.session_state.current_doc_id)
                        st.session_state.show_tree = tree
                else:
                    st.warning("Document is still processing")

with col2:
    st.header("💬 Ask Questions")
    
    if st.session_state.current_doc_id:
        current_doc = st.session_state.documents.get(st.session_state.current_doc_id)
        
        if current_doc and current_doc['status'] == 'ready':
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            
            if prompt := st.chat_input("Ask a question about the document..."):
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                with st.chat_message("assistant"):
                    with st.spinner("Searching document and generating answer..."):
                        try:
                            message_placeholder = st.empty()
                            
                            st.session_state.pipeline.load_document(st.session_state.current_doc_id)
                            
                            node_list = st.session_state.pipeline.search_nodes(prompt)
                            
                            with st.expander("📍 Relevant Sections Found"):
                                for node_id in node_list:
                                    node = st.session_state.pipeline.node_map[node_id]
                                    st.write(f"**{node['title']}** (Page {node['page_index']})")
                            
                            context = st.session_state.pipeline.retrieve_context(node_list)
                            
                            answer = st.session_state.pipeline.generate_answer(prompt, context)
                            
                            message_placeholder.markdown(answer)
                            
                            st.session_state.chat_history.append({"role": "assistant", "content": answer})
                            
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            
            if st.session_state.chat_history:
                if st.button("🗑️ Clear Chat"):
                    st.session_state.chat_history = []
                    st.rerun()
        
        elif current_doc and current_doc['status'] == 'processing':
            st.info("⏳ Document is still processing. Please wait...")
            if st.button("🔄 Refresh Status"):
                st.rerun()
        else:
            st.warning("Please select a ready document from the sidebar")
    else:
        st.info("👈 Upload a document to get started")
        
        st.markdown("### Example Questions:")
        st.markdown("""
        - What are the main conclusions?
        - Summarize the methodology
        - What are the key findings?
        - What limitations are mentioned?
        """)

if 'show_tree' in st.session_state:
    with st.expander("🌳 Document Tree Structure", expanded=True):
        def display_tree(node, level=0):
            indent = "  " * level
            title = node.get('title', 'Untitled')
            page = node.get('page_index', '?')
            st.text(f"{indent}├── {title} (Page {page})")
            for child in node.get('children', []):
                display_tree(child, level + 1)
        
        display_tree(st.session_state.show_tree)
        
        if st.button("Close Tree View"):
            del st.session_state.show_tree
            st.rerun()

st.divider()
st.caption("Powered by PageIndex + Groq LLaMA 3.3")
