import { Request, Response } from 'express';

export const getModules = (req: Request, res: Response) => {
  const modules = [
    {
      id: '1',
      title: 'Foundations of Day Trading',
      description: 'Learn what day trading is, market mechanics, and order types.',
      timeEstimate: '2 hours',
      difficulty: 'Beginner',
      lessons: [
        { id: '1-1', title: 'What is Day Trading?', summary: 'Introduction to day trading and how it differs from investing.' },
        { id: '1-2', title: 'Market Structure', summary: 'Understanding how markets operate and liquidity.' }
      ]
    },
    {
      id: '2',
      title: 'Regulations & PDT Rules',
      description: 'Explore Pattern Day Trader rules and margin requirements.',
      timeEstimate: '1.5 hours',
      difficulty: 'Beginner',
      lessons: [
        { id: '2-1', title: 'PDT Rule Overview', summary: 'Minimum equity requirements and rule implications.' },
        { id: '2-2', title: 'Margin Basics', summary: 'Intraday margin and buying power.' }
      ]
    }
  ];
  res.json(modules);
};