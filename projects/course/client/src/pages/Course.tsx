import React from 'react';
import axios from 'axios';

const Course: React.FC = () => {
  const handlePurchase = async () => {
    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/api/checkout`);
      window.location.href = response.data.url;
    } catch (error) {
      console.error('Error initiating checkout:', error);
    }
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Premium Day Trading Course</h1>
      <p className="mb-4">This comprehensive course includes:</p>
      <ul className="list-disc pl-6 mb-6 space-y-2">
        <li>8 structured modules with video lessons</li>
        <li>Interactive quizzes and practical exercises</li>
        <li>Downloadable checklists and templates</li>
        <li>Progress tracking and completion certificates</li>
      </ul>
      <button
        onClick={handlePurchase}
        className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"
      >
        Buy Now - $99
      </button>
    </div>
  );
};

export default Course;