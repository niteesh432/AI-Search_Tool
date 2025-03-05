import React, { useState } from "react";
import axios from "axios";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";

const API_BASE_URL = "http://144.24.149.254:8000"; // Update this with your FastAPI server IP

function App() {
  const [query, setQuery] = useState("");
  const [alternativeQueries, setAlternativeQueries] = useState([]);
  const [googleResults, setGoogleResults] = useState([]);
  const [youtubeResults, setYoutubeResults] = useState([]);
  const [storedResults, setStoredResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    if (!query.trim()) {
      console.warn("⚠ Query is empty! Please enter a valid query.");
      return;
    }

    setLoading(true);
    setError(null);
    setAlternativeQueries([]);
    setGoogleResults([]);
    setYoutubeResults([]);
    setStoredResults([]);

    try {
      const res = await axios.post(`${API_BASE_URL}/ask-ai/`, { query });

      if (res.data) {
        setAlternativeQueries(res.data.alternative_queries);
        setGoogleResults(res.data.google_results);
        setYoutubeResults(res.data.youtube_results);
      }

      // Fetch ranked results after storing them
      fetchRankedResults(query);
    } catch (err) {
      console.error("❌ API Error:", err.response || err.message);
      setError(err.response?.data?.detail || "An error occurred. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const fetchRankedResults = async (query) => {
    try {
      const res = await axios.get(`${API_BASE_URL}/get_results/`, { params: { query } });
      if (res.data) {
        setStoredResults(res.data);
      }
    } catch (err) {
      console.error("❌ Failed to fetch ranked results:", err.response || err.message);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleSearch();
  };

  return (
    <div className="container text-center p-4 input-container">
      <h2 className="mb-4 heading">AI-Powered Search Tool</h2>

      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control"
          placeholder="Enter your query..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button className="btn btn-primary" onClick={handleSearch} disabled={loading}>
          {loading ? "Searching..." : "Search"}
        </button>
      </div>

      {loading && <div className="spinner-border text-primary" role="status"></div>}

      {error && <p className="text-danger">{error}</p>}

      {/* Alternative Queries */}
      {alternativeQueries.length > 0 && (
        <div className="mt-4 card p-3">
          <h5 className="text-primary text-start">Alternative Queries</h5>
          <ul className="list-unstyled text-start">
            {alternativeQueries.map((altQuery, index) => (
              <li key={index} className="mb-1">{altQuery}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Google Search Results */}
      {googleResults.length > 0 && (
        <div className="mt-4 card p-3">
          <h5 className="text-primary text-start">Google Search Results</h5>
          <ul className="list-unstyled text-start">
            {googleResults.map((result, index) => (
              <li key={index} className="mb-2">
                <a href={result.link} target="_blank" rel="noopener noreferrer">
                  {result.title}
                </a>
                <p className="text-muted small">{result.snippet}</p>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* YouTube Search Results */}
      {youtubeResults.length > 0 && (
        <div className="mt-4 card p-3">
          <h5 className="text-primary text-start">YouTube Search Results</h5>
          <div className="row">
            {youtubeResults.map((video, index) => (
              <div key={index} className="col-md-4 mb-3">
                <div className="card">
                  <img src={video.thumbnail} className="card-img-top" alt={video.title} />
                  <div className="card-body">
                    <h6 className="card-title">{video.title}</h6>
                    <p className="card-text text-muted small">{video.channel}</p>
                    <a href={video.link} target="_blank" rel="noopener noreferrer" className="btn btn-sm btn-danger">
                      Watch on YouTube
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Stored & Ranked Results */}
      {storedResults.length > 0 && (
        <div className="mt-4 card p-3">
          <h5 className="text-success text-start">Ranked Search Results</h5>
          <ul className="list-unstyled text-start">
            {storedResults.map((result, index) => (
              <li key={index} className="mb-2">
                <strong>{result.source}:</strong>{" "}
                <a href={result.link} target="_blank" rel="noopener noreferrer">
                  {result.title}
                </a>{" "}
                <span className="badge bg-info">{result.rank_score.toFixed(2)}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
