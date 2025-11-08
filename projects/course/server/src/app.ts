import express from 'express';
import mongoose from 'mongoose';
import cors from 'cors';
import dotenv from 'dotenv';
import moduleRoutes from './routes/moduleRoutes';
import authRoutes from './routes/authRoutes';
import checkoutRoutes from './routes/checkoutRoutes';
import contactRoutes from './routes/contactRoutes';
import progressRoutes from './routes/progressRoutes';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

mongoose.connect(process.env.MONGO_URI || 'mongodb://localhost:27017/daytrading')
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.error('MongoDB connection error:', err));

app.use('/api/modules', moduleRoutes);
app.use('/api/auth', authRoutes);
app.use('/api/checkout', checkoutRoutes);
app.use('/api/contact', contactRoutes);
app.use('/api/user', progressRoutes);

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});