# LLM-Based Domain-Aware Knowledge Extraction and Querying System (Finance)

## 📌 Project Overview

This project implements an **end-to-end LLM-powered system** for extracting structured knowledge from unstructured text and enabling natural language querying over the extracted information.

The current implementation is **finance-oriented** and demonstrates how Large Language Models (LLMs) can be used to:

* Extract **entities and relationships** from raw text (financial news / transcripts)
* Store them as structured data (triplets)
* Answer user questions by reasoning over the extracted knowledge

> **Core idea:** Convert unstructured domain text → structured knowledge → natural language answers using LLMs.

---

## 🎯 Objectives

* Use LLMs for **relation extraction** (beyond traditional NLP)
* Build a **domain-aware knowledge base** from raw text
* Enable **semantic question answering** over extracted relations
* Demonstrate a practical **LLM + Information Extraction** pipeline

---

## 🧠 System Architecture

```
Raw Text (.txt)
      ↓
Text Cleaning & Preprocessing
      ↓
LLM-based Relation Extraction
      ↓
Structured Knowledge (JSON Triplets)
      ↓
LLM-powered Query & Summarization API
      ↓
Web Frontend (User Interaction)
```

---

## 📁 Project Structure

```
Raw/
│
├── clean_text.py           # Preprocesses raw annotated text
├── process_transcript.py  # Extracts (subject, relation, object) using LLM
├── relations.json         # Stored structured knowledge base
├── app.py                 # Flask backend for querying
│
├── frontend/
│   ├── index.html         # UI for querying the system
│   ├── style.css          # Frontend styling
│   └── script.js          # Frontend logic
│
├── raw_text.txt           # Cleaned input text
└── test.txt               # Original annotated input text
```

---

## 🔍 Component-wise Description

### 1️⃣ Text Cleaning (`clean_text.py`)

**Purpose:**

* Reads annotated input text (`test.txt`)
* Removes labels and noise
* Outputs clean sentences to `raw_text.txt`

**Why this matters:**
LLMs perform better when input text is clean and free from annotation artifacts.

---

### 2️⃣ Relation Extraction (`process_transcript.py`)

**Purpose:**

* Uses a **REBEL-style sequence-to-sequence LLM**
* Extracts structured triplets:

  * **Subject**
  * **Relation**
  * **Object**

**Example Output:**

```json
{
  "subject": "Apple",
  "relation": "acquired",
  "object": "startup"
}
```

**Key Features:**

* Regex-based triplet parsing
* Noise removal and normalization
* Converts unstructured text → structured knowledge

---

### 3️⃣ Knowledge Storage (`relations.json`)

**Purpose:**

* Acts as a lightweight **knowledge base**
* Stores extracted relations in JSON format

**Why JSON:**

* Human-readable
* Easy to extend
* Suitable for prototyping

---

### 4️⃣ Query Engine & API (`app.py`)

**Purpose:**

* Flask-based backend
* Uses **FLAN-T5-Large** for:

  * Entity extraction from user questions
  * Natural language summarization of relevant facts

**Workflow:**

1. User asks a question
2. LLM extracts the main entity
3. Relevant relations are retrieved
4. LLM generates a coherent answer

---

### 5️⃣ Frontend (`frontend/`)

**Purpose:**

* Simple web interface to interact with the system
* Sends questions to backend API
* Displays generated answers

---

## 🚀 How to Run the Project

### 🔧 Prerequisites

* Python 3.8+
* pip
* Internet connection (for model downloads)

### 📦 Install Dependencies

```bash
pip install flask transformers torch sentencepiece
```

### ▶️ Step-by-Step Execution

1. **Clean the raw text**

```bash
python clean_text.py
```

2. **Extract relations using LLM**

```bash
python process_transcript.py
```

3. **Start the Flask server**

```bash
python app.py
```

4. **Open the frontend**

* Open `frontend/index.html` in your browser
* Ask questions related to the extracted text

---

## 📊 Use Case Example

**Question:**

> What companies were acquired recently?

**System Output:**

> The extracted data shows that Company A acquired Company B, indicating a recent acquisition activity.

---

## ✅ Key Highlights

* Uses **LLMs for structured knowledge extraction**
* End-to-end pipeline (Text → Knowledge → Answer)
* Domain-adaptable architecture
* Suitable for:

  * Final-year projects
  * Research prototypes
  * LLM demonstrations

---

## ⚠ Limitations

* No formal evaluation metrics (precision/recall)
* Exact string matching for entities
* No domain-specific ontology enforcement
* Not optimized for large-scale data

---

## 🔮 Future Enhancements

* Finance-specific ontology (earnings, mergers, risk, regulation)
* Knowledge Graph integration (Neo4j / NetworkX)
* RAG-based retrieval instead of JSON
* Evaluation against traditional NLP baselines
* Caching and performance optimization

---

## 🧑‍🎓 Academic Relevance

This project demonstrates:

* Practical use of **Large Language Models**
* Information Extraction & Knowledge Representation
* Applied NLP in the **financial domain**

It is well-suited for **final-year engineering projects** and introductory **research work**.

---

## 📜 License

This project is for **educational and research purposes only**.

---

## 🙌 Acknowledgements

* Hugging Face Transformers
* REBEL Relation Extraction approach
* FLAN-T5 models
