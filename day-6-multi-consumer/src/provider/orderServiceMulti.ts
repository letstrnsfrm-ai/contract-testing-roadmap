import express from 'express';

const app = express();
app.use(express.json());

app.get('/orders', (req, res) => {
  if (req.query.userId === '123') {
    res.json([{ id: 1, product: 'Widget' }]);
  } else {
    res.json([]);
  }
});

app.get('/orders/stats', (req, res) => {
  res.json({ totalOrders: 100, totalRevenue: 2500.50 });
});

export default app;
