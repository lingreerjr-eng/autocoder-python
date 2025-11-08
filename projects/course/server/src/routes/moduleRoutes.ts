import express from 'express';
import { getModules } from '../controllers/moduleController';

const router = express.Router();

router.get('/', getModules);

export default router;