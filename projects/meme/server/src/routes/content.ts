import express from 'express';
import { getModules } from '../controllers/contentController';

const router = express.Router();

router.get('/modules', getModules);

export default router;