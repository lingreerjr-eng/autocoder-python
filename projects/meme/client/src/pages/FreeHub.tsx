import React, { useState } from 'react';

const FreeHub: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const articles = [
    {
      id: '1',
      title: 'Pattern Day Trader Rule Explained',
      content: 'The Pattern Day Trader (PDT) rule requires day trading accounts to maintain a minimum equity of ,000. This article breaks down the rule and its implications.'
    },
    {
      id: '2',
      title: 'Risk Management Fundamentals',
      content: 'Learn about position sizing, stop-losses, and how to protect your capital while day trading.'
    },
    {
      id: '3',
      title: 'Common Beginner Mistakes',
      content: 'Avoid these pitfalls that new traders often fall into, including overtrading and ignoring risk.'
    }
  ];

  const filteredArticles = articles.filter(article =>
    article.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    article.content.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold mb-6">Free Learning Hub</h1>
      <input
        type="text"
        placeholder="Search articles..."
        className="w-full p-3 mb-6 border rounded"
        value={searchTerm}
        onChange={e => setSearchTerm(e.target.value)}
      />
      <div className="space-y-6">
        {filteredArticles.map(article => (
          <div key={article.id} className="border rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-2">{article.title}</h2>
            <p className="text-gray-700">{article.content}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default FreeHub;