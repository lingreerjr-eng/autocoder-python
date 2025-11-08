import express from 'express';
import { getProgress } from '../controllers/progressController';
import auth from '../middleware/auth';

const router = express.Router();

router.get('/progress', auth, getProgress);

export default router;