# AI-Powered Search Tool

##  Project Overview
This AI-powered search tool enhances traditional search by integrating **AI-driven query expansion** using an **Ollama server** and fetching results from **Google and YouTube** using external APIs. The system ranks results based on **relevance and popularity**, ensuring high-quality search outcomes.

## Tech Stack
- **Frontend:** React.js, Bootstrap
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL/MySQL
- **Process Manager:** PM2 (for backend deployment)
- **APIs Used:**
  - **Google Custom Search API** – Fetches search results from Google.
  - **YouTube API** – Retrieves video results from YouTube.
  - **Ollama Server (Cloud Deployed)** – Expands user queries using AI-powered alternatives.

##  Features
1.**AI-powered query expansion** – Enhances user queries for better search results using a cloud-hosted Ollama server.  
2. **Google & YouTube search integration** – Fetches results from trusted sources.  
3. **Ranking mechanism** – Sorts results based on relevance and popularity.  

##  Installation & Setup

### 1️ Clone the Repository
```bash
git clone https://github.com/your-repo/ai-search-tool.git
cd ai-search-tool
```

### 2 Frontend Setup (React.js)
- Navigate to the frontend folder:
  ```bash
  cd frontend
  ```
- Install dependencies & start React app locally:
  ```bash
  npm install
  npm start
  ```
> **Note:** The frontend is not deployed because Vercel/Netlify enforce HTTPS requests, while the backend requires HTTP. To run the project, start the frontend locally.

##  APIs Used
- **Google Custom Search API** – Fetches search results from Google.
- **YouTube API** – Retrieves video search results.
- **Ollama Server (Cloud Deployed)** – Expands user queries using AI-powered alternatives.

##  Steps Implemented

###  Step 1: Setup Project Structure
- Created GitHub repository.
- Initialized **React.js** frontend & **FastAPI backend**.

###  Step 2: Build User Input UI
- Designed a **search box** in React.js.
- Connected frontend to backend via API.

###  Step 3: AI-Powered Query Expansion
- Integrated **Ollama server (cloud-hosted)** to generate alternative queries.
- Tested API calls using Postman & console logs.

###  Step 4: Fetch Data from Google & YouTube
- Used **Google Custom Search API** to fetch search results.
- Integrated **YouTube API** to retrieve video-based search results.
- Processed and structured API responses before sending them to frontend.

###  Step 5: Process & Rank Results
- Stored search results in **PostgreSQL/MySQL database**.
- Implemented **basic ranking logic** (relevance & popularity).

###  Step 6: Display Search Results in UI
- Designed UI to **show search results** as cards/lists.
- Added **sorting & filtering options** (optional).

##  Challenges & Solutions
| Challenge | Solution |
|-----------|---------|
| **HTTPS frontend (Vercel/Netlify) vs HTTP backend** | Ran frontend locally (`npm start`) instead of deploying |
| **Backend stopping when terminal closes** | Used PM2 to keep FastAPI running persistently |
| **API rate limits** | Implemented caching & optimized API calls |
| **Query expansion errors** | Adjusted prompt engineering for Ollama queries |
| **UI responsiveness** | Used Bootstrap & optimized CSS |

##  Future Improvements
- **Enable HTTPS for backend** to deploy the frontend properly.
- **Personalized ranking** based on user preferences.
- **Enhanced UI/UX** with better search filtering.
- **Support for more data sources** (news, blogs, etc.).

##  How to Use
1️. **Enter a search query** in the input box.  
2️. **AI expands your query** using the Ollama server.  
3. **View ranked search results** from Google & YouTube.  

##  Sample Outputs
1. ![1](https://github.com/user-attachments/assets/40f7574e-639f-471e-8c1b-1df9fcb7fa7f)
2. ![2](https://github.com/user-attachments/assets/e4d2ce01-91c0-4faa-a141-1deaa9fea050)
3. ![3](https://github.com/user-attachments/assets/5f4fd6bf-9c5d-4c77-8d86-1fea5605b877)
4. ![4](https://github.com/user-attachments/assets/7c8932dd-9825-47e9-8c24-5c75fa21d6c8)








