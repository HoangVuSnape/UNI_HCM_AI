# Introduction
The University Admission Assistant is an AI-powered system designed to support admission inquiries for 15 universities in Ho Chi Minh City. The system leverages Retrieval-Augmented Generation (RAG) techniques to enhance query responses by integrating structured data retrieval with generative AI models. This ensures accurate and context-aware answers to users' admission-related questions.


# Table of contents
    # Introduction
    # Link
    # Structure code
    # Gettting started
        ## Prepare enviroment
        ## Environment variables
    # Note
    # Run local
    # Contact

###-----------------------LINK------------------------------###
# Link:

- Github: https://github.com/HoangVuSnape/UNI_HCM_AI
- Web deploy: https://huggingface.co/spaces/HoangVuSnape/TuyenSinh_v2
- Link data: https://drive.google.com/drive/folders/1iPG2Sw53wbe7uVmyQZwGQtZeMc4Q4YmF

###-----------------------Structure Code------------------------------###
# Structure Code

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


###-----------------------GETTING STARTED------------------------------###
# Getting started

To get starte with this project, we need to do the following

###-----------------------.ENV------------------------------###

## Environment variables (`.env`)

```env example
# LangChain configuration for enabling tracing, setting API endpoint, authentication, and project management(Lang Smith)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="lsv2_pt_3cf1cc72f325452391c67fc38da4b958dssdsd_7222b87d24"
LANGCHAIN_PROJECT="pr-pertinent-pseudoscience-63"

# API key for Qdrant, a vector database for storing and querying embeddings(using recursive chunking)
QDRANT_API = "đasdsds-UpHXNGsR70W9PuWng"
QDRANT_URL = "https://4bf0a3b6-33c5-4488-b0f3-aabddd6fed6dbf3.eu-west-2-0.aws.cloud.qdrant.io:6333/"

# API key for Groq, a platform that enables fast inference for AI models (LLMs)
GROQ_API_KEY = "gsk_bhFXOpycyjnjTMmgKFY8WGdyb3FYr8CcX0GadsdsdsdsdsaujEdo3Ad42dEqn5"

# API key for Google, a platform that enables fast inference for AI models (LLMs)
GOOGLE_API_KEY = "AIzaSyDzJQ_ILXcd2tBzcwd8Kf_-sdsdsdsd"

# API key for Tavily, a service that assists with web search and data retrieval
TAVILY_API_KEY = "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"

# API key 2 for Qdrant, a vector database for storing and querying embeddings(using semantic chunking)
QDRANT_URL_2 = "https://1390ac05-4421-4fc6-8798-05032e7abad2.us-east4-0.gcp.cloud.qdrant.io/"
QDRANT_API_2 = "02n1zyvj8zLx0xaAPk-_pbVSVIq4sFdsdsdsadaXVUbfMWzl3mCHJdkpTHMn3Cw"

````

After installing the required dependencies, you need to create a `.env` file to configure the necessary API keys. Follow these steps to obtain them:

#### 1. **LangChain API Keys**
- Go to [LangChain Smith](https://smith.langchain.com/) and log in.
- Create a project, then navigate to the **API Keys** section to get your `LANGCHAIN_API_KEY`.
- Set up the following environment variables:
  ```env
  LANGCHAIN_TRACING_V2=true  
  LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"  
  LANGCHAIN_API_KEY="your_langchain_api_key"  
  LANGCHAIN_PROJECT="your_project_name"
  ```

#### 2. **Qdrant API Keys**
- Sign up at [Qdrant Cloud](https://cloud.qdrant.io/).
- Create a new cluster, then go to the **API Keys** section to obtain `QDRANT_API` and `QDRANT_URL`.
- If you have multiple clusters, you can add `QDRANT_URL_2` and `QDRANT_API_2`.
  ```env
  QDRANT_API="your_qdrant_api_key"  
  QDRANT_URL="your_qdrant_url"  
  QDRANT_API_2="your_second_qdrant_api_key"  
  QDRANT_URL_2="your_second_qdrant_url"
  ```

#### 3. **GROQ API Key**
- Register at [GROQ](https://groq.com/) and obtain your API key from the dashboard.
  ```env
  GROQ_API_KEY="your_groq_api_key"
  ```

#### 4. **Google API Key**
- Go to [Google Cloud Console](https://console.cloud.google.com/) and create a new project.
- Enable **Google AI Services** and generate an API key under the **Credentials** section.
  ```env
  GOOGLE_API_KEY="your_google_api_key"
  ```

#### 5. **Tavily API Key**
- Sign up at [Tavily](https://tavily.com/) and retrieve your API key from the dashboard.
  ```env
  TAVILY_API_KEY="your_tavily_api_key"
  ```

After setting up the `.env` file, you can load these environment variables in your project using a library like `dotenv` in Python.

###-----------------------NOTE------------------------------###
# Note:  

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
- Rename file json in 2 files python gemi_agent_v1.py, gemi_agent_v2.py correctively.   

###-----------------------RUN LOCAL------------------------------###
# Run local 

## Prepare enviroment 
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

###-----------------------CONTACT------------------------------###
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