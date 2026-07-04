import express from 'express';
import path from 'path';
import dotenv from 'dotenv';
import indexRouter from './routes/index';
import apiRouter from './routes/api';
import pagesRouter from './routes/pages';

dotenv.config();

const app = express();
const PORT = process.env.PORT ?? 3000;

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/', pagesRouter);
app.use('/api', apiRouter);

app.listen(PORT, () => {
  console.log(`SpaceTrack running → http://localhost:${PORT}`);
});
