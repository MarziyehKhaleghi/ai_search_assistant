import { useState } from "react";
import { Search, Loader, ArrowRight } from "lucide-react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [expandedItems, setExpandedItems] = useState({});

  
  const toggleExpand = (index) => {
    setExpandedItems((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };
  
  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: query }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setAnswer(data.answer);
      setResults(data.sources);
      setQuery("");
    } catch (error) {
      console.error("Feil:", error);
    } finally {
      setLoading(false);
    }


  };

  return (
    <div className="container">
      <h1 className="title">AI Search Assistant</h1>

      <form className="search-form" onSubmit={handleSearch}>
        <div className="search-box">

          <Search size={18} className="search-icon" />
          
          <input
            type="text"
            placeholder="Enter your search here..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="search-input"
          />

          <button type="submit"  disabled={loading} className="icon-button">
            
             <ArrowRight  size={22}/>
            
          </button>

        </div>
      </form>

      {loading && (
        <div className="spinner-container">
          <Loader className="spin" size={30} />
        </div>
      )}

      {answer && (
        <div className="answer-box">
          <h3>AI Answer:</h3>
          <p>{answer}</p>
        </div>
      )}

      {results.length > 0 &&(
        <div className="sources">
          <h3>Sources:</h3>
          {results.map((item, index) => (
            <div key={index} className="source-item">

              <p><strong>File:</strong> {item.metadata.source}</p>
              <p><strong>Score:</strong> {item.score}</p>
              <p>
                <strong>Snippet:</strong>{" "}
                {expandedItems[index]
                  ? item.text
                  : `${item.text.slice(0, 100)}...`}
              </p>

              
              <div className="read-more-container">
                <button
                  className="read-more-button"
                  onClick={() => toggleExpand(index)}
                >
                  {expandedItems[index] ? "Show less" : "Read more"}
                </button>

              </div>

            </div>
          ))}
        </div>
      )}  
    </div>
  );
}

export default App;