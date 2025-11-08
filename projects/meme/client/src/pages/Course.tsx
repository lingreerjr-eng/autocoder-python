import React from 'react';
import { loadStripe } from '@stripe/stripe-js';
import axios from 'axios';

const stripePromise = loadStripe(process.env.REACT_APP_STRIPE_PUBLISHABLE_KEY!);

const Course: React.FC = () => {
  const handleCheckout = async () => {
    const stripe = await stripePromise;
    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/api/payments/create-checkout-session`);
      const session = response.data;
      const result = await stripe?.redirectToCheckout({ sessionId: session.id });
      if (result?.error) {
        console.error(result.error.message);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold mb-6">Premium Day Trading Course</h1>
      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-2">What's Included</h2>
        <ul className="list-disc pl-5 space-y-1">
          <li>7 comprehensive modules</li>
          <li>Downloadable checklists & templates</li>
          <li>Video walkthroughs (coming soon)</li>
          <li>Progress tracking dashboard</li>
        </ul>
      </div>
      <button
        onClick={handleCheckout}
        className="bg-green-600 text-white px-6 py-3 rounded hover:bg-green-700"
      >
        Buy Now - .99
      </button>
    </div>
  );
};

export default Course;