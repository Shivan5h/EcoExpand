import React, { useState, useEffect } from "react";
import "./index.css";
// import axios from 'axios';

// const fetchData = async () => {
//     try {
//         const response = await axios.post('http://localhost:5173/your-endpoint', { key: 'value' });
//         console.log(response.data);
//     } catch (error) {
//         console.error(error);
//     }
// };

// fetchData();

// const apiUrl = process.env.REACT_APP_API_URL;

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
  const [apiData, setApiData] = useState({}); // Store data from FastAPI

  const [input, setInput] = useState('');
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
      try {
          const response = await axios.post(`${process.env.REACT_APP_API_URL}/predict`, { data: input });
          setResult(response.data);
      } catch (error) {
          console.error('Error:', error);
      }
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      setAppVisible(true);
      setIsLoading(false);
    }, 2500); 
    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/data");
      const result = await response.json();
      setApiData(result); // Save data from FastAPI
    } catch (error) {
      console.error("Error fetching data:", error);
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
        <footer className="footer">
          <p>&copy; 2024 EcoDrive. Empowering SMBs for a sustainable future.</p>
        </footer>
        {activeSection && (
          <div className={`popup ${isPopupClosing ? "closing" : ""}`}>
            <div className="popup-content animate-popup">
              <button className="close-btn" onClick={handlePopupClose}>
                ✕
              </button>
              <div className="popup-emoji">{activeSection.emoji}</div>
              <h2>{activeSection.title}</h2>
              <p>{activeSection.description}</p>
              <p className="about-section">{activeSection.about}</p>
              
              {/* <button
                className="get-started-btn"
                style={{ backgroundColor: activeSection.color }}
              >
                Get Started
              </button> */}
              <div>
                <input
                  type="text"
                   value={input}
                  onChange={(e) => setInput(e.target.value)}
                 placeholder="Enter data"
               />
                 <button onClick={handleSubmit}>Submit</button>
                 {result && <div>Result: {result}</div>}
             </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
