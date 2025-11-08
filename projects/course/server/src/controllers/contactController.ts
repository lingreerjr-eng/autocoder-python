import { Request, Response } from 'express';

export const sendMessage = (req: Request, res: Response) => {
  const { name, email, message } = req.body;

  // In a real app, send email or store in DB
  console.log(`Message from ${name} (${email}): ${message}`);
  res.json({ message: 'Message received' });
};