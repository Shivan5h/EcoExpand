import React, { useState } from "react";
import "./index.css";

const modules = [
  {
    id: 1,
    icon: "📦",
    title: "Eco-Friendly Packaging",
    about: "Discover sustainable packaging options tailored to your business needs.",
    image: "https://via.placeholder.com/400x200",
    details: "Connect with certified suppliers to source biodegradable or recyclable packaging that lowers your carbon footprint."
  },
  {
    id: 2,
    icon: "🚚",
    title: "Smart Logistics Optimizer",
    about: "Optimize shipping routes to minimize emissions and save costs.",
    image: "https://via.placeholder.com/400x200",
    details: "Leverage real-time logistics data to choose carbon-saving routes and green shipping partners."
  },
  {
    id: 3,
    icon: "🌍",
    title: "Carbon Footprint Calculator",
    about: "Track and analyze emissions across your operations.",
    image: "https://via.placeholder.com/400x200",
    details: "Assess lifecycle emissions, including raw materials, shipping, and disposal, to identify areas for improvement."
  },
  {
    id: 4,
    icon: "♻️",
    title: "Product Recyclability",
    about: "Help customers and businesses manage end-of-life product recycling.",
    image: "https://via.placeholder.com/400x200",
    details: "Provide recyclability insights, badges, and disposal recommendations for every product."
  },
  {
    id: 5,
    icon: "⭐",
    title: "Sustainability Rewards",
    about: "Earn rewards for sustainable actions.",
    image: "https://via.placeholder.com/400x200",
    details: "Redeem points for discounts, carbon credits, or premium features by implementing green initiatives."
  }
];

const App = () => {
  const [activeModule, setActiveModule] = useState(null);

  const openModule = (module) => {
    setActiveModule(module);
  };

  const closeModule = () => {
    setActiveModule(null);
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>EcoDrive - Transforming <br/> E-commerce</h1>
        <p>Empowering SMBs with sustainable solutions for a greener future.</p>
      </header>

      <div className="modules-container">
        {modules.map((module) => (
          <div key={module.id} className="module-card animated-card" onClick={() => openModule(module)}>
            <div className="module-icon">{module.icon}</div>
            <h2 className="module-title">{module.title}</h2>
          </div>
        ))}
      </div>

      {activeModule && (
        <div className="modal-overlay" onClick={closeModule}>
          <div className="modal animated-modal" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={closeModule}>
              ✖
            </button>
            <img className="modal-img" src={activeModule.image} alt={activeModule.title} />
            <h2 className="modal-title">{activeModule.title}</h2>
            <p className="modal-details">{activeModule.details}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
