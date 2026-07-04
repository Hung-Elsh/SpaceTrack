import { Router, Request, Response } from 'express';

const router = Router();

router.get('/data', (req: Request, res: Response) => {
  res.render('data', { page: 'data' });
});

router.get('/objects', (req: Request, res: Response) => {
  res.render('objects', { page: 'objects' });
});

export default router;
