import { Request, Response } from 'express';

export const submitContactForm = (req: Request, res: Response) => {
  const { name, email, message } = req.body;
  console.log(`Contact Form Submission:\nName: ${name}\nEmail: ${email}\nMessage: ${message}`);
  res.status(200).json({ message: 'Message received' });
};