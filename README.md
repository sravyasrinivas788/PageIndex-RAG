# PageIndex RAG Pipeline

A clean, modular RAG (Retrieval-Augmented Generation) system that combines PageIndex for document processing and Groq for LLM-powered question answering.

## Features

- 🌐 **Web UI**: Interactive Streamlit interface for easy document upload and querying
- 📄 **Document Processing**: Submit and process PDF documents using PageIndex
- 🔍 **Smart Search**: LLM-powered node search to find relevant document sections
- 🤖 **Answer Generation**: Generate accurate answers using Groq's LLaMA models
- 💬 **Chat Interface**: Conversational Q&A with chat history
- 🏗️ **Modular Architecture**: Clean separation of concerns with reusable components
- 🔐 **Secure Configuration**: Environment-based API key management

## Project Structure

```
PageIndex/
├── app.py                # Web UI (Streamlit)
├── config.py              # Configuration and API keys
├── llm_client.py          # Groq LLM integration
├── document_processor.py  # PageIndex document handling
├── rag_pipeline.py        # Complete RAG pipeline
├── main.py               # CLI interface
├── example.py            # Usage examples
├── .env                  # API keys (not committed to git)
└── README.md             # This file
```

## Setup

### 1. Install Dependencies

```bash
pip install pageindex groq python-dotenv
```

### 2. Configure API Keys

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
PAGEINDEX_API_KEY=your_pageindex_api_key_here
```

## Usage

### Web UI (Recommended)

The easiest way to use the RAG pipeline is through the web interface:

```bash
streamlit run app.py
```

This will open a web browser with an interactive interface where you can:
- 📤 Upload PDF documents
- ⏳ Track processing status
- 💬 Ask questions in a chat interface
- 🌳 View document tree structure
- 📍 See which sections were used to answer your questions

**Features:**
- Drag-and-drop PDF upload
- Real-time processing status
- Chat-style Q&A interface
- Multi-document support
- Visual feedback on relevant sections

### Command Line Interface

#### Query an Existing Document

```bash
python main.py --doc-id <document_id> --query "Your question here"
```

**Example:**
```bash
python main.py --doc-id pi-cmmn2qtdl00t51oqnfpjpbgq0 --query "What are the conclusions in this document?"
```

#### Submit a New Document

```bash
python main.py --submit path/to/document.pdf
```

**Example:**
```bash
python main.py --submit input.pdf
```

This will return a document ID that you can use for querying.

#### View Document Tree Structure

```bash
python main.py --doc-id <document_id> --show-tree
```

**Example:**
```bash
python main.py --doc-id pi-cmmn2qtdl00t51oqnfpjpbgq0 --show-tree
```

### Programmatic Usage

#### Simple Query

```python
from rag_pipeline import RAGPipeline

pipeline = RAGPipeline()
answer = pipeline.query(
    doc_id="pi-cmmn2qtdl00t51oqnfpjpbgq0",
    question="What are the main findings?"
)
print(answer)
```

#### Custom Workflow

```python
from rag_pipeline import RAGPipeline

pipeline = RAGPipeline()

# Load document
pipeline.load_document("pi-cmmn2qtdl00t51oqnfpjpbgq0")

# Search for relevant nodes
node_list = pipeline.search_nodes("What are the limitations?")

# Retrieve context
context = pipeline.retrieve_context(node_list)

# Generate answer
answer = pipeline.generate_answer("What are the limitations?", context)
print(answer)
```

#### Submit New Document

```python
from document_processor import DocumentProcessor

processor = DocumentProcessor()
doc_id = processor.submit_document("path/to/document.pdf")
print(f"Document ID: {doc_id}")

# Check if ready
if processor.is_ready(doc_id):
    tree = processor.get_tree(doc_id)
    print("Document is ready!")
```

## Examples

Run the example script to see the pipeline in action:

```bash
python example.py
```

This will query the existing document with sample questions.

## Configuration

### LLM Settings

Edit `config.py` to change the default LLM model or temperature:

```python
DEFAULT_LLM_MODEL = "llama-3.3-70b-versatile"  # Groq model
DEFAULT_TEMPERATURE = 0  # 0 for deterministic, higher for creative
```

### Available Groq Models

- `llama-3.3-70b-versatile` (default, recommended)
- `llama-3.1-70b-versatile`
- `mixtral-8x7b-32768`
- `gemma2-9b-it`

## How It Works

1. **Document Loading**: PageIndex processes the PDF and creates a hierarchical tree structure
2. **Node Search**: The LLM analyzes the tree to identify relevant sections for your question
3. **Context Retrieval**: Text content is extracted from the identified nodes
4. **Answer Generation**: The LLM generates an answer based on the retrieved context

## API Reference

### RAGPipeline

Main class for the RAG pipeline.

**Methods:**
- `load_document(doc_id)` - Load document tree structure
- `search_nodes(query)` - Search for relevant nodes using LLM
- `retrieve_context(node_list)` - Retrieve text from nodes
- `generate_answer(query, context)` - Generate answer from context
- `query(doc_id, question)` - Complete end-to-end pipeline

### DocumentProcessor

Handle document operations with PageIndex.

**Methods:**
- `submit_document(pdf_path)` - Submit a PDF document
- `is_ready(doc_id)` - Check if document is processed
- `get_tree(doc_id)` - Get document tree structure

### LLM Client

**Functions:**
- `call_llm(prompt, model, temperature)` - Synchronous LLM call
- `call_llm_async(prompt, model, temperature)` - Asynchronous LLM call

## Troubleshooting

### Document Not Ready

If you get "Document is still processing", wait a few moments and try again. Large documents may take time to process.

### API Key Errors

Ensure your `.env` file is in the project root and contains valid API keys:
```bash
cat .env  # Linux/Mac
type .env  # Windows
```

### Import Errors

Make sure all dependencies are installed:
```bash
pip install pageindex groq python-dotenv
```

## Security

- Never commit your `.env` file to version control
- Add `.env` to your `.gitignore` file
- Keep your API keys secure and rotate them regularly

## License

This project is provided as-is for educational and development purposes.
