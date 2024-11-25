import React, { useState, useEffect } from "react";
import axios from 'axios';
import "./index.css";

const sections = [
  {
    id: "carbon-calculator",
    title: "Carbon Footprint Calculator",
    description: "Assess carbon emissions for your products and track environmental impact.",
    emoji: "🌍",
    about: `
      Our Carbon Footprint Calculator helps you measure the carbon emissions of your products throughout their lifecycle. 
      By understanding your impact, you can identify areas to reduce emissions and adopt more sustainable practices. 
      Key features include real-time data tracking, benchmarking, and actionable insights to reduce your environmental footprint.
    `,
    color: "#2e7d32",
  },
  {
    id: "packaging-optimizer",
    title: "Eco-Friendly Packaging Optimizer",
    description: "Find and switch to sustainable packaging options effortlessly.",
    emoji: "📦",
    about: `
      The Eco-Friendly Packaging Optimizer helps businesses transition to sustainable packaging materials.
      It provides recommendations based on your specific product dimensions, weight, and shipping needs. 
      Reduce waste and appeal to eco-conscious customers with innovative, biodegradable, or recyclable packaging solutions.
    `,
    color: "#4caf50",
  },
  {
    id: "logistics-optimizer",
    title: "Smart Logistics Optimizer",
    description: "Optimize delivery routes and minimize carbon emissions with AI-powered tools.",
    emoji: "🚛",
    about: `
      Our Smart Logistics Optimizer leverages AI and machine learning to optimize your delivery routes.
      By minimizing transportation distances and maximizing vehicle capacity, you save on costs and significantly reduce your emissions. 
      The tool integrates seamlessly with existing logistics software for real-time route adjustments.
    `,
    color: "#ff9800",
  },
  {
    id: "recyclability-tool",
    title: "Product Recyclability Tool",
    description: "Learn how recyclable your products are and display EcoBadges to customers.",
    emoji: "♻️",
    about: `
      With the Product Recyclability Tool, you can analyze your product's recyclability and highlight this to consumers.
      Gain access to detailed reports on recyclable components and suggestions for improving product design to align with circular economy principles. 
      Showcase EcoBadges on your site to build trust with sustainability-focused customers.
    `,
    color: "#3f51b5",
  },
  {
    id: "supplier-network",
    title: "Sustainable Supplier Network",
    description: "Connect with verified suppliers offering eco-friendly products and materials.",
    emoji: "🔗",
    about: `
      The Sustainable Supplier Network connects you with pre-vetted, eco-friendly suppliers worldwide.
      Find suppliers for raw materials, components, or finished goods that align with your sustainability goals. 
      Our platform ensures transparency, helping you create a robust, ethical supply chain.
    `,
    color: "#8e24aa",
  },
  {
    id: "eco-dashboard",
    title: "Customer-Facing EcoDashboard",
    description: "Showcase your sustainability achievements to eco-conscious customers.",
    emoji: "📊",
    about: `
      The EcoDashboard allows you to communicate your sustainability initiatives and achievements directly to your customers. 
      Display metrics like carbon savings, recyclable packaging usage, and sustainable sourcing efforts in a visually engaging way. 
      Strengthen brand loyalty by showing your commitment to a greener future.
    `,
    color: "#00bcd4",
  },
];

function App() {
  const [activeSection, setActiveSection] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isPopupClosing, setIsPopupClosing] = useState(false);
  const [appVisible, setAppVisible] = useState(false);
  
  // State for API data
  const [chatResponse, setChatResponse] = useState('');
  const [userQuery, setUserQuery] = useState('');
  const [countries, setCountries] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState('');
  const [countryAnalysis, setCountryAnalysis] = useState(null);
  const [textInput, setTextInput] = useState('');
  const [keyPhrases, setKeyPhrases] = useState([]);
  const [summary, setSummary] = useState('');

  // Fetch initial data
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const response = await axios.get('/countries');
        setCountries(response.data.countries);
      } catch (error) {
        console.error('Error fetching countries:', error);
      }
    };

    fetchInitialData();
    const timer = setTimeout(() => {
      setAppVisible(true);
      setIsLoading(false);
    }, 2500);
    return () => clearTimeout(timer);
  }, []);

  // API interaction functions
  const handleChat = async () => {
    try {
      const response = await axios.post('/chat', {
        user_query: userQuery
      });
      setChatResponse(response.data.response);
    } catch (error) {
      console.error('Chat error:', error);
    }
  };

  const handleCountryAnalysis = async () => {
    try {
      const response = await axios.post('/analyze', {
        country: selectedCountry
      });
      setCountryAnalysis(response.data);
    } catch (error) {
      console.error('Analysis error:', error);
    }
  };

  const handleTextAnalysis = async () => {
    try {
      const [phrasesResponse, summaryResponse] = await Promise.all([
        axios.post('/extract-key-phrases', { text: textInput }),
        axios.post('/summarize-text', { text: textInput })
      ]);
      
      setKeyPhrases(phrasesResponse.data.key_phrases);
      setSummary(summaryResponse.data.summary);
    } catch (error) {
      console.error('Text analysis error:', error);
    }
  };

  // Render API components based on active section
  const renderApiComponent = () => {
    switch (activeSection?.id) {
      case 'carbon-calculator':
        return (
          <div className="api-section">
            <input
              type="text"
              value={userQuery}
              onChange={(e) => setUserQuery(e.target.value)}
              placeholder="Ask about carbon footprint..."
            />
            <button onClick={handleChat}>Get Answer</button>
            {chatResponse && (
              <div className="response-box">
                <p>{chatResponse}</p>
              </div>
            )}
          </div>
        );

      case 'logistics-optimizer':
        return (
          <div className="api-section">
            <select
              value={selectedCountry}
              onChange={(e) => setSelectedCountry(e.target.value)}
            >
              <option value="">Select a country</option>
              {countries.map(country => (
                <option key={country} value={country}>{country}</option>
              ))}
            </select>
            <button onClick={handleCountryAnalysis}>Analyze Market</button>
            {countryAnalysis && (
              <div className="analysis-box">
                <p>Risk Cluster: {countryAnalysis.risk_cluster}</p>
                <p>Predicted Savings: {countryAnalysis.predicted_cost_savings}</p>
              </div>
            )}
          </div>
        );

      case 'eco-dashboard':
        return (
          <div className="api-section">
            <textarea
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              placeholder="Enter text for analysis..."
            />
            <button onClick={handleTextAnalysis}>Analyze Text</button>
            {keyPhrases.length > 0 && (
              <div className="analysis-box">
                <h4>Key Phrases:</h4>
                <ul>
                  {keyPhrases.map(([phrase, count]) => (
                    <li key={phrase}>{phrase}: {count}</li>
                  ))}
                </ul>
              </div>
            )}
            {summary && (
              <div className="analysis-box">
                <h4>Summary:</h4>
                <p>{summary}</p>
              </div>
            )}
          </div>
        );

      default:
        return null;
    }
  };

  const handleNavClick = (section) => {
    const sectionElement = document.getElementById(section.id);
    sectionElement.scrollIntoView({ behavior: "smooth" });
    setTimeout(() => setActiveSection(section), 500);
  };

  const handlePopupClose = () => {
    setIsPopupClosing(true);
    setTimeout(() => {
      setIsPopupClosing(false);
      setActiveSection(null);
    }, 300); 
  };

  return (
    <div className="app">
      {isLoading && (
        <div className="loading-screen">
          <h1 className="animate-header">EcoDrive</h1>
          <p className="animate-subtitle">Transforming E-commerce with Sustainable Solutions</p>
        </div>
      )}
      <div className={`main-app ${appVisible ? "fade-in" : "hidden"}`}>
        <header className="header">
          <h1>EcoDrive</h1>
          <p>Transforming E-commerce with Sustainable Solutions</p>
        </header>
        <nav className="navbar">
          <ul>
            {sections.map((section) => (
              <li key={section.id}>
                <button onClick={() => handleNavClick(section)}>{section.title}</button>
              </li>
            ))}
          </ul>
        </nav>
        <main className="main-content">
          {sections.map((section) => (
            <div
              key={section.id}
              className="section-box animate"
              id={section.id}
              onClick={() => setActiveSection(section)}
            >
              <div className="emoji">{section.emoji}</div>
              <h2>{section.title}</h2>
              <p>{section.description}</p>
            </div>
          ))}
        </main>
        {activeSection && (
          <div className={`popup ${isPopupClosing ? "closing" : ""}`}>
            <div className="popup-content animate-popup">
              <button className="close-btn" onClick={handlePopupClose}>✕</button>
              <div className="popup-emoji">{activeSection.emoji}</div>
              <h2>{activeSection.title}</h2>
              <p>{activeSection.description}</p>
              <p className="about-section">{activeSection.about}</p>
              {renderApiComponent()}
            </div>
          </div>
        )}
        <footer className="footer">
          <p>&copy; 2024 EcoDrive. Empowering SMBs for a sustainable future.</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
