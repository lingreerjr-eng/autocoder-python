import express from 'express';
import { createCheckoutSession, webhook } from '../controllers/paymentController';

const router = express.Router();

router.post('/create-checkout-session', createCheckoutSession);
router.post('/webhook', express.raw({ type: 'application/json' }), webhook);

export default router;