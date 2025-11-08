import React from 'react';

const About: React.FC = () => {
  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold mb-6">About This Course</h1>
      <div className="prose max-w-none">
        <p>This course is designed for educational purposes only. It is not financial advice.</p>
        <p>Trading involves substantial risk of loss and is not suitable for every investor.</p>
        <p>Past performance is not indicative of future results. You are responsible for complying with all applicable laws and regulations.</p>
        <p>We recommend consulting with a licensed financial professional before making any investment decisions.</p>
      </div>
    </div>
  );
};

export default About;