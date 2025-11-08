import { Request, Response } from 'express';

export const getProgress = (req: Request, res: Response) => {
  // Mock data - in real app, fetch from DB
  const progress = [
    { moduleId: '1', completedLessons: ['1-1'] },
    { moduleId: '2', completedLessons: [] }
  ];
  res.json(progress);
};