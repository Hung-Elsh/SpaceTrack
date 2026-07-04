import { Router, Request, Response } from 'express';
import {
  fetchObjects,
  fetchObjectDetail,
  fetchSnapshotDates,
  pullObjects,
  pullSnapshots,
  fetchBackfillStatus,
} from '../services/apiService';

const router = Router();

// Proxy routes to Flask API — returns 503 until Phase 2 backend is live.

router.get('/objects', async (req: Request, res: Response) => {
  try {
    const data = await fetchObjects(req.query as Record<string, string>);
    res.json(data);
  } catch {
    res.status(503).json({ error: 'Flask API not available', hint: 'Start the backend on FLASK_API_URL' });
  }
});

router.get('/objects/:noradId', async (req: Request, res: Response) => {
  try {
    const data = await fetchObjectDetail(req.params.noradId);
    res.json(data);
  } catch {
    res.status(503).json({ error: 'Flask API not available' });
  }
});

router.get('/snapshot/dates', async (req: Request, res: Response) => {
  try {
    const data = await fetchSnapshotDates();
    res.json(data);
  } catch {
    res.status(503).json({ error: 'Flask API not available' });
  }
});

// Proactive pull APIs — relay the Flask status code as-is (200 on success, 429 on cooldown)

router.post('/objects', async (req: Request, res: Response) => {
  try {
    const { status, body } = await pullObjects();
    res.status(status).json(body);
  } catch {
    res.status(503).json({ error: 'Flask API not available', hint: 'Start the backend on FLASK_API_URL' });
  }
});

router.post('/snapshot', async (req: Request, res: Response) => {
  try {
    const { status, body } = await pullSnapshots();
    res.status(status).json(body);
  } catch {
    res.status(503).json({ error: 'Flask API not available', hint: 'Start the backend on FLASK_API_URL' });
  }
});

router.get('/backfill/status', async (req: Request, res: Response) => {
  try {
    const { status, body } = await fetchBackfillStatus();
    res.status(status).json(body);
  } catch {
    res.status(503).json({ error: 'Flask API not available' });
  }
});

export default router;
