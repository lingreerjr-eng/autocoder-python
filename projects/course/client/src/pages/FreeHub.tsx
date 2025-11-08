import React, { useState } from 'react';

const FreeHub: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const articles = [
    {
      id: '1',
      title: 'Pattern Day Trader Rule Explained',
      content: 'Learn about the PDT rule, its requirements, and implications for active traders.'
    },
    {
      id: '2',
      title: 'Risk Management Fundamentals',
      content: 'Essential techniques to protect your capital and manage exposure.'
    },
    {
      id: '3',
      title: 'Common Beginner Mistakes',
      content: 'Avoid these pitfalls that new traders often fall into.'
    }
  ];

  const filteredArticles = articles.filter(article =>
    article.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    article.content.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Free Learning Hub</h1>
      <input
        type="text"
        placeholder="Search articles..."
        className="w-full p-2 border rounded mb-4"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <div className="space-y-4">
        {filteredArticles.map(article => (
          <div key={article.id} className="border p-4 rounded shadow">
            <h2 className="text-xl font-semibold">{article.title}</h2>
            <p>{article.content}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default FreeHub;