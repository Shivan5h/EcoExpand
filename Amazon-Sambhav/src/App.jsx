import React from 'react';
import './index.css';

function App() {
  return (
    <div className="app">
      <header className="header">
        <h1>EcoDrive</h1>
        <p>Transforming E-commerce with Sustainable Solutions</p>
      </header>

      <nav className="navbar">
        <ul>
          <li><a href="#carbon-calculator">Carbon Calculator</a></li>
          <li><a href="#packaging-optimizer">Packaging Optimizer</a></li>
          <li><a href="#logistics-optimizer">Logistics Optimizer</a></li>
          <li><a href="#recyclability-tool">Recyclability Tool</a></li>
          <li><a href="#supplier-network">Supplier Network</a></li>
          <li><a href="#eco-dashboard">EcoDashboard</a></li>
        </ul>
      </nav>

      <main className="main-content">
        <section id="carbon-calculator">
          <h2>Carbon Footprint Calculator</h2>
          <p>
            Assess carbon emissions for your products and track environmental impact.
          </p>
        </section>

        <section id="packaging-optimizer">
          <h2>Eco-Friendly Packaging Optimizer</h2>
          <p>
            Find and switch to sustainable packaging options effortlessly.
          </p>
        </section>

        <section id="logistics-optimizer">
          <h2>Smart Logistics Optimizer</h2>
          <p>
            Optimize delivery routes and minimize carbon emissions with AI-powered tools.
          </p>
        </section>

        <section id="recyclability-tool">
          <h2>Product Recyclability Tool</h2>
          <p>
            Learn how recyclable your products are and display EcoBadges to customers.
          </p>
        </section>

        <section id="supplier-network">
          <h2>Sustainable Supplier Network</h2>
          <p>
            Connect with verified suppliers offering eco-friendly products and materials.
          </p>
        </section>

        <section id="eco-dashboard">
          <h2>Customer-Facing EcoDashboard</h2>
          <p>
            Showcase your sustainability achievements to eco-conscious customers.
          </p>
        </section>
      </main>

      <footer className="footer">
        <p>&copy; 2024 EcoDrive. Empowering SMBs for a sustainable future.</p>
      </footer>
    </div>
  );
}

export default App;
