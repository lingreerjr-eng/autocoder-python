import React from 'react';
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
  return (
    <div className="container mx-auto p-6">
      <section className="hero text-center py-12">
        <h1 className="text-4xl font-bold mb-4">Learn Day Trading the Right Way</h1>
        <p className="text-lg mb-6">Master the fundamentals, manage risk, and build discipline with our structured course.</p>
        <Link to="/course" className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded">
          Get Started
        </Link>
      </section>
      <section className="modules mt-12">
        <h2 className="text-2xl font-semibold mb-4">Course Modules</h2>
        <ul className="list-disc pl-6 space-y-2">
          <li>Foundations of Day Trading</li>
          <li>Regulations & PDT Rules</li>
          <li>Risk Management</li>
          <li>Day Trading Strategies</li>
          <li>Tools & Platforms</li>
          <li>Trading Psychology</li>
          <li>Small Account Path</li>
          <li>Ethics & Disclaimers</li>
        </ul>
      </section>
    </div>
  );
};

export default Home;