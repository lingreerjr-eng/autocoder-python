import { Request, Response } from 'express';
import Module from '../models/Module';

export const getModules = async (req: Request, res: Response) => {
  try {
    const modules = await Module.find();
    res.json(modules);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching modules' });
  }
};