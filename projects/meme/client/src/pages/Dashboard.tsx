import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Progress {
  moduleId: string;
  completedLessons: string[];
}

const Dashboard: React.FC = () => {
  const [progress, setProgress] = useState<Progress[]>([]);

  useEffect(() => {
    const fetchProgress = async () => {
      try {
        const res = await axios.get(`${process.env.REACT_APP_API_URL}/api/user/progress`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        setProgress(res.data);
      } catch (err) {
        console.error('Failed to fetch progress', err);
      }
    };
    fetchProgress();
  }, []);

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold mb-6">Your Dashboard</h1>
      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-4">Progress Tracking</h2>
        {progress.length > 0 ? (
          <ul className="space-y-4">
            {progress.map(p => (
              <li key={p.moduleId} className="border rounded p-4">
                Module {p.moduleId}: {p.completedLessons.length} lessons completed
              </li>
            ))}
          </ul>
        ) : (
          <p>No progress yet. Start learning!</p>
        )}
      </div>
      <div>
        <h2 className="text-xl font-semibold mb-4">Downloads</h2>
        <ul className="list-disc pl-5 space-y-2">
          <li><a href="/downloads/risk-checklist.pdf" className="text-blue-600 hover:underline">Risk Management Checklist</a></li>
          <li><a href="/downloads/trading-plan-template.pdf" className="text-blue-600 hover:underline">Trading Plan Template</a></li>
        </ul>
      </div>
    </div>
  );
};

export default Dashboard;