import React from 'react';

const About: React.FC = () => {
  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">About This Course</h1>
      <p className="mb-4">This course is designed to provide educational content about day trading. It is not financial advice.</p>
      <p className="mb-4">Trading involves risk, including the potential loss of principal. Past performance is not indicative of future results.</p>
      <p>Please consult with a licensed financial professional before making any investment decisions.</p>
    </div>
  );
};

export default About;