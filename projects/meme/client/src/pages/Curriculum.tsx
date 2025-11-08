import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Module {
  id: string;
  title: string;
  description: string;
  lessons: Lesson[];
  timeEstimate: string;
  difficulty: string;
}

interface Lesson {
  id: string;
  title: string;
  summary: string;
}

const Curriculum: React.FC = () => {
  const [modules, setModules] = useState<Module[]>([]);

  useEffect(() => {
    const fetchModules = async () => {
      try {
        const res = await axios.get(`${process.env.REACT_APP_API_URL}/api/content/modules`);
        setModules(res.data);
      } catch (err) {
        console.error('Failed to fetch modules', err);
      }
    };
    fetchModules();
  }, []);

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold mb-6">Course Curriculum</h1>
      <div className="space-y-6">
        {modules.map(module => (
          <div key={module.id} className="border rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-2">{module.title}</h2>
            <p className="text-gray-600 mb-4">{module.description}</p>
            <div className="mb-2">
              <span className="font-medium">Time:</span> {module.timeEstimate} | 
              <span className="font-medium">Difficulty:</span> {module.difficulty}
            </div>
            <ul className="list-disc pl-5 space-y-2">
              {module.lessons.map(lesson => (
                <li key={lesson.id}>
                  <strong>{lesson.title}:</strong> {lesson.summary}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Curriculum;