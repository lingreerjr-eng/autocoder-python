import React from 'react';
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
  return (
    <div className="container mx-auto px-4 py-12">
      <section className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4">Learn Day Trading the Right Way</h1>
        <p className="text-lg mb-6 max-w-2xl mx-auto">
          Master the fundamentals of day trading with our structured, regulation-aware course. Start building your skills today.
        </p>
        <Link to="/course" className="bg-blue-600 text-white px-6 py-3 rounded hover:bg-blue-700">
          Get Started
        </Link>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Course Modules Overview</h2>
        <ul className="list-disc pl-6 max-w-2xl mx-auto">
          <li>Foundations of Day Trading</li>
          <li>Regulations & PDT Rules</li>
          <li>Risk Management Essentials</li>
          <li>Day Trading Strategies</li>
          <li>Tools & Platforms</li>
          <li>Trading Psychology</li>
          <li>Small Account Path</li>
        </ul>
      </section>
    </div>
  );
};

export default Home;