# Urban Lab Information Repository Project  
_AI-Driven Content Curation for Knowledge Management_

> NYU SPS – Urban Lab  
> Applied Project Capstone, Fall 2025  

---

## 1. Project Overview

The **Urban Lab Information Repository Project** is an AI-assisted content curation pipeline designed to help the NYU SPS Urban Lab keep its knowledge base up to date with high-quality, well-tagged articles on urban development.

1. **Goal**  
   Reduce manual effort in finding and curating relevant urban-development news while keeping faculty reviewers in control of final decisions.

2. **What the system does**  
   Automatically ingest articles from trusted sources, classify them into Urban Lab pillars, present them in a review dashboard, and generate wiki-ready entries.

3. **Data storage**  
   All curated article metadata is stored in a **Supabase (Postgres)** database, which can later power a Retrieval-Augmented Generation (RAG) knowledge base.

4. **Repository contents**  
   Includes the ingestion workflow (n8n JSON), the Streamlit dashboard (`app.py`), Supabase integration code, and helper scripts/configs.

---

## 2. Urban Lab Context

The NYU SPS **Urban Lab** focuses on research and practice around urban development.

1. **Four key pillars**  
   Net Zero Cities, Housing Affordability, Public/Private Development, and Culture-Led Development.

2. **Problem today**  
   Faculty and students manually search across multiple news sites, copy content into the wiki, and tag articles by hand.

3. **Intended impact**  
   Provide a scalable pipeline so the Urban Lab can keep its repository current, consistent, and easier to use for teaching and research.

---

## 3. Key Features

1. **Automated Article Ingestion**  
   Uses an **n8n workflow** (`News collector final.json`) and/or Python scripts to pull articles from selected news sources (RSS/API), normalize metadata, and remove duplicates, then write them into a Supabase table.

2. **AI-Powered Classification**  
   Applies an LLM-based classifier or prompt to assign each article to one of the four Urban Lab pillars and filter out clearly off-topic items, targeting ≥80% accuracy on labeled data.

3. **Human-in-the-Loop Review Dashboard (`app.py`)**  
   A Streamlit UI that connects to Supabase, lets reviewers browse articles, inspect titles/snippets/full links, correct tags, add notes, and approve or reject items.

4. **Wiki-Ready Export**  
   For approved items, generates standardized wiki snippets (title, summary, tags, source, date, URL) so reviewers can copy-paste directly into the Urban Lab wiki.

5. **RAG-Ready Design (Future Work)**  
   Supabase stores approved articles in a consistent schema, ready to be chunked, embedded, and indexed in a vector DB for a future “Ask the Urban Lab” RAG interface.

---

## 4. System Architecture

At a high level, the system looks like this:

1. **News Sources**  
   Selected publishers / RSS feeds that produce urban development content.

2. **Ingestion & Normalization (n8n + Python)**  
   n8n workflow defined in `News collector final.json` pulls articles (RSS/API); optional helper scripts such as `rss_to_notion.py` can be used for backfilling or integration; articles are cleaned, normalized, and sent to Supabase.

3. **Supabase Storage**  
   Supabase (hosted Postgres) stores raw and curated article records and acts as the single source of truth for the pipeline.

4. **Classification & Filtering**  
   An LLM-based classifier (invoked from Python / n8n) tags each article with a pillar or marks it as off-topic.

5. **Review Dashboard (Streamlit, `app.py`)**  
   `app.py` queries Supabase, shows a review queue, and lets reviewers validate, edit, approve, or reject articles.

6. **Wiki Export**  
   Approved articles are converted into wiki-ready blocks and displayed in the dashboard for copy-and-paste.

7. **RAG Preparation (Design)**  
   Approved articles in Supabase are ready to be chunked and embedded into a future vector DB for Q&A.

---

## 5. Tech Stack

1. **Language**  
   Python 3.10+.

2. **Orchestration / Agents**  
   n8n (workflow exported as `News collector final.json`).

3. **Web UI**  
   Streamlit (`app.py`).

4. **Database**  
   Supabase (Postgres) for all article metadata and curated records.

5. **LLM / AI Services**  
   OpenAI API (for classification / summarization).

6. **Other Libraries**  
   `supabase-py` (or PostgREST client) for DB access (`supabase_io.py`), `requests` / `httpx` for HTTP calls, `pandas` for data handling.

7. **Note**  
   Adjust this list to match your actual environment and dependencies.

---

## 6. Repository Structure

1. **app.py**  
   Main Streamlit dashboard for reviewing, tagging, and exporting wiki-ready articles.

2. **supabase_io.py**  
   Supabase helper functions (CRUD operations for article tables and related metadata).

3. **rss_to_notion.py**  
   Legacy / optional script for pushing RSS items to Notion or use as a backfill helper.

4. **News collector final.json**  
   n8n workflow definition used to collect and normalize news articles from external sources.

5. **articles.json**  
   Sample or backup article data used during development and testing.

6. **requirements.txt**  
   List of Python dependencies required to run the project.

7. **.env**  
   Local environment variables (not committed in production) for API keys and DB credentials.

8. **.devcontainer/**  
   VS Code Dev Container configuration for a reproducible development environment.

9. **__pycache__/**  
   Python bytecode cache directory (can be safely ignored).

---

## 7. Getting Started

1. **Prerequisites**  
   Python 3.10+, n8n (self-hosted or cloud, if you want to run ingestion), a Supabase project (URL + keys and an `articles` table), and an OpenAI API key (or compatible LLM provider).

2. **Clone the Repository**  
   ```bash
   git clone https://github.com/z18007910999/Urban-lab.git
   cd Urban-lab
3. **Install Dependencies**

  1. **Install Python packages**  
     From the project root, run the following command to install all dependencies:  
         pip install -r requirements.txt

  2. **(Optional) Dev Container / VS Code**  
     If you use VS Code Dev Containers, you can open the repository with the `.devcontainer/` configuration and let dependencies install automatically inside the container.


 4. **Set Environment Variables**

1. **Create `.env` file**  
   → In the project root, create a new `.env` file (or copy from `.env.example` if you create one and rename it).

2. **Fill in required keys**  
   → Add the following variables (example) to `.env`:  
       OPENAI_API_KEY=sk-...  
       SUPABASE_URL=https://xxxx.supabase.co  
       SUPABASE_ANON_KEY=...  
       SUPABASE_SERVICE_ROLE_KEY=...   # if needed for server-side operations  
       SUPABASE_TABLE_NAME=articles  
       # STREAMLIT or other settings  

3. **Keep secrets out of Git**  
   → Make sure `.env` is listed in `.gitignore` so that secrets are not committed to GitHub.

---

## 8. Running the Project

### 8.1 Start the Ingestion Workflow (n8n)

1. **Import workflow**  
   Import `News collector final.json` into your n8n instance to create the news collection workflow.

2. **Configure credentials**  
   In n8n, configure news API keys, Supabase URL, and Supabase API keys so the workflow can write to Supabase.

3. **Set schedule**  
   Add a schedule trigger (for example, once per day) so n8n periodically fetches new articles.

4. **Optional Python ingestion**  
   If you extend the project with custom Python ingestion scripts, you can also run them via cron or manually.

### 8.2 Launch the Streamlit Dashboard

1. **Run Streamlit app**  
   From the project root, run:  
       streamlit run app.py  

2. **Open in browser**  
   Open the URL printed in the terminal (typically `http://localhost:8501`) to access the review dashboard.

3. **Verify Supabase connection**  
   Check that the page loads article lists and can read/write to Supabase; if there are errors, verify the `.env` configuration.

---

## 9. Using the Dashboard

1. **Review Queue**  
   On the main screen, view the latest articles fetched from Supabase and filter by predicted pillar, source, or date.

2. **Inspect Articles**  
   Click an article to see its title, summary, source, and link to the full content; open the original page if needed.

3. **Edit & Decide**  
   For each article, adjust pillar tags, add reviewer notes, and mark it as **Approved**, or **Rejected**.

4. **Wiki Export Area**  
   In the export section, see all approved articles and copy pre-formatted wiki text blocks directly into the Urban Lab wiki.

5. **Feedback Loop**  
   Use misclassified or rejected articles to refine prompts/models and thresholds, improving classification quality over time.

---

## 10. Evaluation & Metrics

1. **Classification Accuracy**  
   Compute the percentage of correctly assigned pillars on a labeled test set (target ≥ 80%) and monitor per-pillar performance.

2. **Reviewer Effort**  
   Compare average review time per article before and after using the dashboard to quantify efficiency gains.

3. **Throughput**  
   Track how many relevant articles are processed and approved per week to measure coverage and output.

4. **Data Quality**  
   Sample wiki entries to confirm that they follow the Urban Lab standard format (title, summary, tags, source, date, URL) consistently.

---

## 11. Roadmap / Future Work

1. **RAG Implementation**  
   Chunk approved article content from Supabase, store embeddings in a vector database, and build an “Ask the Urban Lab” Q&A interface.

2. **More Sources & Languages**  
   Add more trusted news outlets and, where appropriate, non-English sources to broaden coverage.

3. **Active Learning Loop**  
   Feed reviewer label corrections back into Supabase and use them to refine prompts or train updated classifiers.

4. **User Management & Logging**  
   Add authentication and detailed activity logs for faculty, TAs, and student reviewers to strengthen governance and collaboration.

---

## 12. Acknowledgements

1. **Institutional Context**  
   This project is part of the **MS in Management and Systems** program at **NYU School of Professional Studies**, in collaboration with the **Urban Lab**.

2. **Key People**  
   Project Sponsor: Researcher Fernao Ferreira Reimao, NYU SPS Urban Lab  
   Capstone Course: MASY-GC 4100 – Applied Technical Project  
   Student Developer: Xuanzhe Zheng (`xz3223@nyu.edu`)


