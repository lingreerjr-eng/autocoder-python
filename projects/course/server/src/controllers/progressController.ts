import { Request, Response } from 'express';
import User from '../models/User';

export const getProgress = async (req: Request, res: Response) => {
  try {
    const user = await User.findById((req as any).user.id);
    if (!user) return res.status(404).json({ message: 'User not found' });
    res.json(user.progress);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching progress' });
  }
};