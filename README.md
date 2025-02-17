# Guiding assistant for Vietnamese university admissions powered by Advanced RAG
The University Admission Assistant is an AI-powered system designed to support admission inquiries for 15 universities in Ho Chi Minh City. The system leverages Retrieval-Augmented Generation (RAG) techniques to enhance query responses by integrating structured data retrieval with generative AI models. This ensures accurate and context-aware answers to users' admission-related questions.

# Link 
- Github: https://github.com/HoangVuSnape/UNI_HCM_AI
- Web deploy: https://huggingface.co/spaces/HoangVuSnape/TuyenSinh_v2
- Link dataset: https://drive.google.com/drive/folders/1iPG2Sw53wbe7uVmyQZwGQtZeMc4Q4YmF


# Table of content

<!--ts-->
- [Guiding assistant for Vietnamese university admissions powered by Advanced RAG](#guiding-assistant-for-vietnamese-university-admissions-powered-by-advanced-rag)
- [Link](#link)
- [Table of content](#table-of-content)
- [Project structure](#project-structure)
- [Getting started](#getting-started)
  - [Note:](#note)
  - [Run local](#run-local)
    - [Prepare enviroment](#prepare-enviroment)
- [Application services](#application-services)
  - [RAG (Retrieval-Augmented Generation)](#rag-retrieval-augmented-generation)
    - [System overview](#system-overview)
    - [RAG flow answering](#rag-flow-answering)
    - [Evaluate](#evaluate)
- [DEMO](#demo)
- [References](#references)
- [Contact](#contact)
<!--te-->

# Project structure
```bash
├── UNIVERSITY_ADMISSIONS_ASSISTANT
│   ├── src                                      # Source code
│   │   ├── adaptive_rag.py                     # Adaptive retrieval-augmented generation
│   │   ├── corrective_rag.py                   # Corrective RAG implementation
│   │   ├── gemi_agent_v1.py                    # First version of GEMI agent
│   │   ├── gemi_agent_v2.py                    # Updated version of GEMI agent
│   │   ├── grader.py                           # Grading system logic
│   │   ├── load_key.py                         # API key loading utilities
│   │   ├── main.py                             # Main entry point for the application
│   │   ├── query_router.py                     # Routing queries to appropriate modules
│   │   ├── query_to_sql.py                     # Convert queries to SQL statements
│   │   ├── query_transformation.py             # Transform query formats
│   │   ├── retrieval_hybrid.py                 # Hybrid retrieval techniques
│   │   ├── retrieval_nv.py                     # Named-variant retrieval implementation
│   │   ├── serve.py                            # Server-related functionalities
│   │   ├── university_admissions.db            # Database for university admissions
│   │   ├── web_search.py                       # Web-based search utilities
│   ├── README.md                               # Project documentation
│   ├── requirements.txt                        # Dependencies for the project
│   ├── .env                                    # Environment variables (API keys, etc.)
│   ├── .env.example                            # Example of environment configuration
│   ├── .gitignore                              # Ignore files for Git
│   ├── creadientials_vertex.json               # JSON config file (possibly credentials)
```
# Getting started

To get starte with this project, we need to do the following

Config all api key in .env.example(Qdrant, Tavily, GROQ, GEMINAI, LANGCHAIN SMITH)

## Note:  

The reason for using two Qdrant APIs is that one is used for storing the database with recursive chunking, while the other is used for semantic chunking.  

Additionally, during development, you can experiment with the free $300 Google Cloud Console credits to obtain API keys.  

- While configuring, I also use **LLM ChatVertexAI**, and the setup involves configuring Google Console and downloading the JSON file. This file is required to load the LLM values for the agent.  

You can refer to the following link for a guide on setup and credential creation:  
[LangChain Google Vertex AI Setup](https://python.langchain.com/docs/integrations/chat/google_vertex_ai_palm/)

Or you can see step by step to get file creadiential json in this below:
Step 1: Create a Google Cloud Project
- Go to Google Cloud Console.
- Click on "Select a project" (or "Create Project" if you don’t have one).
- Enter a Project Name and click "Create".

Step 2: Enable Vertex AI API
- In the Google Cloud Console, navigate to APIs & Services → Library.
- Search for "Vertex AI API".
- Click Enable.

Step 3: Create a Service Account
- Go to APIs & Services → Credentials.
- Click "Create Credentials" → "Service account".
- Enter a Name, ID, and Description, then click Create.
- Assign the Vertex AI User and Editor roles (or a custom role with sufficient permissions).
- Click Done.

Step 4: Generate and Download the JSON Key
- In the Credentials section, find the newly created Service Account.
- Click on it → Navigate to the Keys tab.
- Click "Add Key" → "Create new key".
- Select "JSON" format and click "Create".
- A JSON file will be downloaded to your system (e.g., tdtuchat-16614553b756.json).

Step 5: 
- Rename file json in 2 files python gemi_agent_v1.py, gemi_agent_v2.py correctively

-----------------------

## Run local 

### Prepare enviroment 
Install all dependencies dedicated to the project in local

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

After configuring all JSON files, setting up all API keys in the `.env` file, and installing dependencies from `requirements.txt`, follow these steps to run the system:

1. Open Terminal  
2. Activate Virtual Environment  
   - Using **venv**:  
     ```sh
     source .venv\Scripts\activate      # On Windows 
     ```

3. Navigate to the Project Folder
   ```sh
   cd UNI_ADMISSIONS_ASSISTANT/src
   ```
4. Run the Application
   ```sh
   streamlit run main.py
   ```

This will start the University Admission Assistant system, which will be accessible in your browser via the Streamlit interface. 🚀
# Application services 

## RAG (Retrieval-Augmented Generation) 

### System overview


### RAG flow answering



### Evaluate 

The evaluation metrics currently in use are:

- **Recall@k**: Evaluate the accuracy of information retrieval
- **Correctness**:The metric evaluates the answer generated by the system to match a given query reference answer.

The golden dataset I chose for evaluation consists of 1000 samples. Each sample includes 3 fields: query, related_documents, answer


**Recall@k**
|Model               | K=3    | K =5   | K=10    |
|-----------------   |--------|--------|---------|
|BGE-m3              | 55.11% | 63.43% | 72.18%  |
|E5                  | 54.61% | 63.53% | 72.02%  |
|Elasticsearch       | 42.54% | 49.61% | 56.85%  |
|Ensemble            | 68.38% | 74.85% | 80.66%  |
|Ensemble + rerank   | 79.82% | 82,82% | 87.66%  |

**Correctness**



# DEMO       


# References


# Contact 
If you want to support or get API and URL QDRANT ask us:
- Member 1: 
  Hoang Dinh Quy Vu
  0868245465
  hoangdinhquyvu.snape.22@gmail.com
- Memeber 2:
  Tran Quoc An
  0383474552
  quocan1203it@gmail.com