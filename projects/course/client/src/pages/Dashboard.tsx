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
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/user/progress`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        setProgress(response.data);
      } catch (error) {
        console.error('Error fetching progress:', error);
      }
    };

    fetchProgress();
  }, []);

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Your Dashboard</h1>
      <div className="space-y-4">
        {progress.map((p) => (
          <div key={p.moduleId} className="border p-4 rounded shadow">
            <h2 className="text-xl font-semibold">Module ID: {p.moduleId}</h2>
            <p>Completed Lessons: {p.completedLessons.length}</p>
            <a href={`/downloads/module-${p.moduleId}.pdf`} className="text-blue-500 hover:underline">Download Resources</a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;