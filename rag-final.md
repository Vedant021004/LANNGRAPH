
# 🚀 Job-Ready RAG Roadmap

> **Goal:** Go from basic RAG → Advanced RAG → Agentic RAG → Production RAG
> **Method:** Learn → Implement → Evaluate → Deploy → Contribute

---

## 🗺️ Roadmap

```text
RAG Fundamentals
       ↓
Document Processing
       ↓
Chunking
       ↓
Embeddings
       ↓
Vector Databases
       ↓
Retrieval
       ↓
Hybrid Search
       ↓
Reranking
       ↓
Query Transformation
       ↓
Advanced RAG
       ↓
RAG Evaluation
       ↓
Agentic RAG
       ↓
GraphRAG
       ↓
Multimodal RAG
       ↓
Production RAG
       ↓
Security
       ↓
Deployment
       ↓
Open Source Contribution
```

---

# 01 — RAG Fundamentals

### Study

* [ ] What is RAG?
* [ ] Why RAG?
* [ ] RAG vs Fine-tuning
* [ ] Naive RAG architecture
* [ ] Retrieval-Augmented Generation pipeline
* [ ] Context window
* [ ] Hallucination
* [ ] Grounding

### 🎥 Video

**RAG Explained End-to-End**

[Watch on YouTube — RAG Explained End-to-End](https://www.youtube.com/watch?v=3flmVt3gz-U&utm_source=chatgpt.com)

It covers chunking, embeddings, vector databases, similarity search, hybrid search and reranking. ([YouTube][2])

---

# 02 — Document Loading

### Study

* [ ] PDF
* [ ] HTML
* [ ] Markdown
* [ ] DOCX
* [ ] CSV
* [ ] JSON
* [ ] Images
* [ ] OCR
* [ ] Tables
* [ ] Metadata

### 🎥 Video

[Production RAG — Document Loader & Processing](https://www.youtube.com/watch?v=mHxLXzYjQRE&t=935s&utm_source=chatgpt.com)

Start around **15:35** for document loaders and **28:27** for the indexing/document-processing pipeline. ([YouTube][1])

---

# 03 — Chunking ⭐

### Study

* [ ] Fixed-size chunking
* [ ] Recursive chunking
* [ ] Sentence chunking
* [ ] Token chunking
* [ ] Semantic chunking
* [ ] Chunk overlap
* [ ] Parent-child chunking
* [ ] Contextual chunking
* [ ] Late chunking
* [ ] Chunk-size optimization

### 🎥 Video

[Production RAG — Contextual Retrieval & Late Chunking](https://www.youtube.com/watch?v=mHxLXzYjQRE&t=22469s&utm_source=chatgpt.com)

The course covers contextual retrieval around **6:14:29** and late vs early chunking around **6:24:26**. ([YouTube][1])

### 🛠️ Implement

Take your current:

```python
RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
```

and experiment with:

```text
500 / 50
1000 / 100
semantic chunking
parent-child
```

Then compare retrieval quality.

---

# 04 — Embeddings

### Study

* [ ] What is an embedding?
* [ ] Dense vectors
* [ ] Embedding dimensions
* [ ] Cosine similarity
* [ ] Dot product
* [ ] Euclidean distance
* [ ] Embedding normalization
* [ ] Sentence Transformers
* [ ] Local embeddings
* [ ] Multilingual embeddings
* [ ] Multimodal embeddings

### 🎥 Video

[Production RAG — Embedding Dimensions Deep Dive](https://www.youtube.com/watch?v=mHxLXzYjQRE&t=2892s&utm_source=chatgpt.com)

The course's embedding deep dive begins around **48:12**. ([YouTube][1])

---

# 05 — Vector Databases

### Study

* [ ] Chroma
* [ ] FAISS
* [ ] Qdrant
* [ ] Pinecone
* [ ] Weaviate
* [ ] PostgreSQL + pgvector
* [ ] Collections
* [ ] Metadata filtering
* [ ] ANN
* [ ] HNSW
* [ ] Indexing

### 🎥 Video

[Production RAG — Chroma Vector Database](https://www.youtube.com/watch?v=mHxLXzYjQRE&t=3653s&utm_source=chatgpt.com)

The course demonstrates Chroma around **1:01:05** and later covers Supabase/PGVector. ([YouTube][1])

---

# 06 — Retrieval ⭐⭐⭐

### Study

* [ ] Similarity search
* [ ] Top-K
* [ ] Metadata filtering
* [ ] Dense retrieval
* [ ] Sparse retrieval
* [ ] BM25
* [ ] Keyword search
* [ ] Hybrid search
* [ ] Multi-vector retrieval

### 🎥 Video

[Production RAG — Hybrid Search](https://www.youtube.com/watch?v=mHxLXzYjQRE&t=6826s&utm_source=chatgpt.com)

The course covers hybrid search around **1:53:46**. ([YouTube][1])

---

# 07 — Reranking 🔥

### Study

* [ ] Why reranking?
* [ ] Bi-encoder
* [ ] Cross-encoder
* [ ] Reranker models
* [ ] BGE reranker
* [ ] ColBERT
* [ ] Top-K → rerank → Top-N
* [ ] Reciprocal Rank Fusion

### 🎥 Video

[Production-ready Retrieval RAG — Hybrid Search, Reranking & HyDE](https://www.youtube.com/watch?v=YU_aQOjcQM0&utm_source=chatgpt.com)

This covers BM25 + hybrid search, ColBERT reranking, HyDE and the complete retrieval pipeline. ([Class Central][3])

---

# 08 — Query Transformation

### Study

* [ ] Query rewriting
* [ ] Query expansion
* [ ] Multi-query retrieval
* [ ] HyDE
* [ ] RAG Fusion
* [ ] Query decomposition
* [ ] Query routing
* [ ] Self-query retrieval

### 🎥 Recommended

[Learn RAG from Scratch — Multi-Query, HyDE & Fusion](https://skillagents.ai/videos/learn-rag-from-scratch?utm_source=chatgpt.com)

---

# 09 — Advanced RAG

### Study

* [ ] Advanced RAG
* [ ] Modular RAG
* [ ] Self-RAG
* [ ] Corrective RAG
* [ ] CRAG
* [ ] Adaptive RAG
* [ ] Context compression
* [ ] Long-context RAG
* [ ] Recursive RAG

### 🛠️ Practice

Take your current RAG:

```text
Question
 ↓
Similarity Search
 ↓
LLM
```

and transform it into:

```text
Question
 ↓
Query Rewriter
 ↓
Retriever
 ↓
Reranker
 ↓
Context Compressor
 ↓
LLM
```

---

# 10 — RAG Evaluation ⭐⭐⭐⭐⭐

This is **extremely important for becoming job-ready**.

### Study

* [ ] Why evaluate RAG?
* [ ] Ground truth
* [ ] Retrieval evaluation
* [ ] Precision@K
* [ ] Recall@K
* [ ] Hit Rate
* [ ] MRR
* [ ] NDCG
* [ ] Context Precision
* [ ] Context Recall
* [ ] Faithfulness
* [ ] Answer Relevancy
* [ ] RAGAS
* [ ] LLM-as-a-Judge
* [ ] Regression testing

### 🎥 Course

[Learn RAG from Scratch — Evaluation Metrics](https://skillagents.ai/videos/learn-rag-from-scratch?utm_source=chatgpt.com)

### 🛠️ Your project

Create:

```text
questions.json
answers.json
ground_truth.json
```

Then evaluate:

```text
Retrieval
    ↓
Precision
Recall
MRR
    ↓
Generation
    ↓
Faithfulness
Answer Relevancy
```

---

# 11 — Agentic RAG 🔥🔥🔥

Now bring in your **LangGraph knowledge**.

### Study

* [ ] Agentic RAG
* [ ] Query router
* [ ] Retrieval agent
* [ ] Tool calling
* [ ] Retrieval tools
* [ ] State
* [ ] Conditional routing
* [ ] Reflection
* [ ] Self-correction
* [ ] Planning
* [ ] Multi-agent RAG
* [ ] Human-in-the-loop

### 🎥 Video

[Agentic RAG with LangGraph + ChromaDB](https://www.classcentral.com/course/youtube-build-an-agentic-rag-pipeline-with-langgraph-chromadb-step-by-step-tutorial-511266?utm_source=chatgpt.com)

The tutorial specifically builds an Agentic RAG system using **LangGraph + ChromaDB**, including StateGraph, tools and agent loops. ([Class Central][4])

---

# 12 — GraphRAG

### Study

* [ ] Knowledge graphs
* [ ] Entities
* [ ] Relationships
* [ ] Entity extraction
* [ ] Graph databases
* [ ] Neo4j
* [ ] Graph retrieval
* [ ] Multi-hop reasoning
* [ ] GraphRAG

### 🎥 Video

[Production RAG — GraphRAG](https://www.youtube.com/watch?v=mHxLXzYjQRE&t=25485s&utm_source=chatgpt.com)

The freeCodeCamp course covers GraphRAG and multi-hop reasoning around **7:04:45**. ([YouTube][1])

---

# 13 — Multimodal RAG 🔥

Since you've already been interested in **PDF + image + video RAG**, this should be one of your major projects.

### Study

* [ ] Text RAG
* [ ] Image RAG
* [ ] PDF RAG
* [ ] Table RAG
* [ ] Chart RAG
* [ ] Vision-language models
* [ ] Multimodal embeddings
* [ ] Image retrieval
* [ ] Layout understanding
* [ ] ColPali
* [ ] Multimodal document RAG

### 🎥 Video

[Production RAG — Multimodal RAG with ColPali](https://www.youtube.com/watch?v=mHxLXzYjQRE&t=26668s&utm_source=chatgpt.com)

The course covers vision-based document RAG using ColPali around **7:24:28**. ([YouTube][1])

---

# 14 — Production RAG 🚀

### Study

* [ ] FastAPI
* [ ] REST API
* [ ] Async RAG
* [ ] Streaming
* [ ] PostgreSQL
* [ ] pgvector
* [ ] Redis
* [ ] Caching
* [ ] Semantic caching
* [ ] Batch processing
* [ ] Docker
* [ ] CI/CD
* [ ] Cloud deployment

### 🎥 Main Course

[Production RAG — Full 7.5 Hour Course](https://www.youtube.com/watch?v=mHxLXzYjQRE&utm_source=chatgpt.com)

Useful chapters include scaling, production hosting, PGVector, FastAPI and LangGraph. ([YouTube][1])

---

# 15 — Observability

### Study

* [ ] Logging
* [ ] Tracing
* [ ] LangSmith
* [ ] Langfuse
* [ ] Arize Phoenix
* [ ] Retrieval traces
* [ ] Latency
* [ ] Token usage
* [ ] Cost tracking
* [ ] Error monitoring

### 🎥 Video

[Production RAG — LangSmith & Observability](https://www.youtube.com/watch?v=mHxLXzYjQRE&t=7976s&utm_source=chatgpt.com)

The course introduces observability around **2:21:10** and LangSmith around **2:29:56**. ([YouTube][1])

---

# 16 — RAG Security 🔐

### Study

* [ ] Prompt injection
* [ ] Indirect prompt injection
* [ ] Data poisoning
* [ ] Retrieval poisoning
* [ ] PII
* [ ] Access control
* [ ] Document permissions
* [ ] Authentication
* [ ] Authorization
* [ ] Rate limiting
* [ ] Guardrails
* [ ] Output validation

### 🎥 Video

[Production RAG — Security Layer](https://www.youtube.com/watch?v=mHxLXzYjQRE&t=16456s&utm_source=chatgpt.com)

The course has a dedicated security section beginning around **4:34:36** and a security checklist around **5:41:36**. ([YouTube][1])

---

# 17 — Production Architecture

Your final architecture should look something like:

```text
                       USER
                         │
                         ▼
                     FastAPI
                         │
                         ▼
                  LangGraph Agent
                         │
             ┌───────────┼───────────┐
             │           │           │
             ▼           ▼           ▼
         Vector DB     BM25        SQL
             │           │
             └─────┬─────┘
                   ▼
              Hybrid Search
                   │
                   ▼
                Reranker
                   │
                   ▼
            Context Compression
                   │
                   ▼
                  LLM
                   │
                   ▼
              Grounded Answer
                   │
                   ▼
               Citations
                   │
                   ▼
              LangSmith
```

---

# 18 — Capstone Projects

## 🟢 Project 1 — Basic RAG

```text
PDF
 ↓
Chunking
 ↓
Embeddings
 ↓
Chroma
 ↓
Similarity Search
 ↓
LLM
```

---

## 🟡 Project 2 — Production RAG

```text
PDF
 ↓
Semantic Chunking
 ↓
Dense + BM25
 ↓
Hybrid Search
 ↓
Reranker
 ↓
LLM
 ↓
Citations
 ↓
RAGAS
```

---

## 🔴 Project 3 — Agentic RAG

```text
                    Query
                      ↓
                 LangGraph
                      ↓
                  Router
             ┌────────┼────────┐
             ↓        ↓        ↓
          Vector     SQL      Web
             │
             ▼
          Reranker
             ↓
        Answer Checker
             ↓
            LLM
```

---

## 🔥 Project 4 — Multimodal RAG

```text
PDF
 ├── Text
 ├── Images
 ├── Tables
 ├── Charts
 └── Layout
       ↓
Multimodal Retrieval
       ↓
Vision LLM
       ↓
Answer + Citations
```

---

# 🏆 Project 5 — Job-Ready RAG

Build this as your **main portfolio project**:

```text
                    React
                      │
                      ▼
                   FastAPI
                      │
                      ▼
                 LangGraph
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   Vector Search   BM25 Search    SQL
        │             │
        └──────┬──────┘
               ▼
          Hybrid Search
               ↓
            Reranker
               ↓
       Context Compression
               ↓
              LLM
               ↓
       Citation Generator
               ↓
          RAGAS Evaluation
               ↓
          LangSmith
               ↓
          Docker + Cloud
```

---

# 📚 Bonus — One GitHub Repository to Study

This repository is particularly aligned with the roadmap:

[Advanced RAG Systems — GitHub](https://github.com/mohd-faizy/Advanced-RAG-Systems?utm_source=chatgpt.com)

It covers basic RAG → advanced retrieval → Hybrid Search → Reranking → HyDE → CRAG → Self-RAG → GraphRAG → LangGraph Agentic RAG → RAGAS → production-style capstones. ([GitHub][5])

Another useful reference:

[LangChain RAG Tutorial — GitHub](https://github.com/gianlucamazza/langchain-rag-tutorial?utm_source=chatgpt.com)

It includes advanced RAG architectures, multimodal RAG, RAGAS, SQL/Graph support, Docker and testing/CI/CD templates. ([GitHub][6])

---

# ✅ Final Checklist

```text
[ ] RAG Fundamentals
[ ] Document Loading
[ ] Chunking
[ ] Embeddings
[ ] Vector DB
[ ] Dense Retrieval
[ ] BM25
[ ] Hybrid Search
[ ] Reranking
[ ] Query Rewriting
[ ] Multi-Query
[ ] HyDE
[ ] RAG Fusion
[ ] Context Compression
[ ] RAGAS
[ ] Evaluation
[ ] Agentic RAG
[ ] LangGraph
[ ] GraphRAG
[ ] Multimodal RAG
[ ] FastAPI
[ ] PostgreSQL / pgvector
[ ] Docker
[ ] Redis / Caching
[ ] LangSmith
[ ] Security
[ ] Deployment
[ ] Open Source Contribution
```

### 🎯 Your rule

**Don't move to the next checkbox until you've built the current one.**

For you specifically, I'd start at **Chunking → Embeddings → Retrieval → Hybrid Search**, because you've already built the basic `PyPDFLoader → Chroma → similarity_search → ChatOllama` pipeline.

And the big **7.5-hour freeCodeCamp course** can act as your backbone: its chapters already cover most of the journey from basic RAG through production, Agentic RAG, GraphRAG and Multimodal RAG. ([YouTube][1])

[1]: https://www.youtube.com/watch?v=mHxLXzYjQRE&utm_source=chatgpt.com "Production RAG with LangChain & Vector Databases – Full Course - YouTube"
[2]: https://www.youtube.com/watch?v=3flmVt3gz-U&utm_source=chatgpt.com "RAG Explained End-to-End | Chunking, Embeddings, Vector Databases & Retrieval - YouTube"
[3]: https://www.classcentral.com/course/youtube-build-production-ready-retrieval-rag-pipeline-in-langchain-hybrid-search-bm25-re-ranking-hyde-478185?utm_source=chatgpt.com "Free Video: Build Production-Ready Retrieval RAG Pipeline in LangChain - Hybrid Search, Re-ranking and HyDE from Venelin Valkov | Class Central"
[4]: https://www.classcentral.com/course/youtube-build-an-agentic-rag-pipeline-with-langgraph-chromadb-step-by-step-tutorial-511266?utm_source=chatgpt.com "Free Video: Build an Agentic RAG Pipeline with LangGraph and ChromaDB - Step-by-Step Tutorial from AI Bites | Class Central"
[5]: https://github.com/mohd-faizy/Advanced-RAG-Systems?utm_source=chatgpt.com "GitHub - mohd-faizy/Advanced-RAG-Systems: Hands-on implementation of modern Retrieval-Augmented Generation (RAG) systems using LangChain, LangGraph, vector databases, RAGAS, and Agentic AI workflows. · GitHub"
[6]: https://github.com/gianlucamazza/langchain-rag-tutorial?utm_source=chatgpt.com "GitHub - gianlucamazza/langchain-rag-tutorial: Production-ready tutorial for building Retrieval-Augmented Generation (RAG) systems with LangChain. · GitHub"
