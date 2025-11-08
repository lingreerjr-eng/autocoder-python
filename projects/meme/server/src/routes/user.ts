import express from 'express';
import { getProgress } from '../controllers/userController';

const router = express.Router();

router.get('/progress', getProgress);

export default router;