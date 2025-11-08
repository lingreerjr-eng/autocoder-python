import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Module {
  id: string;
  title: string;
  description: string;
  duration: string;
  difficulty: string;
  lessons: Lesson[];
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
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/modules`);
        setModules(response.data);
      } catch (error) {
        console.error('Error fetching modules:', error);
      }
    };

    fetchModules();
  }, []);

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Course Curriculum</h1>
      <div className="space-y-6">
        {modules.map((module) => (
          <div key={module.id} className="border p-4 rounded shadow">
            <h2 className="text-xl font-semibold">{module.title}</h2>
            <p className="text-gray-600">{module.description}</p>
            <p><strong>Duration:</strong> {module.duration} | <strong>Difficulty:</strong> {module.difficulty}</p>
            <ul className="mt-2 list-disc pl-5 space-y-1">
              {module.lessons.map((lesson) => (
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