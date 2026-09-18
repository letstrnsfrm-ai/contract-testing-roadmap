import express from 'express';

const app = express();
app.use(express.json());

app.get('/health', (req, res) => {
  res.status(200).send('OK');
});

app.get('/orders/:id', (req, res) => {
  if (req.params.id === '1') {
    res.json({ id: 1, product: 'Widget', quantity: 2, status: 'pending' });
  } else {
    res.status(404).json({ error: 'Not found' });
  }
});

app.post('/orders', (req, res) => {
  const { product, quantity } = req.body;
  res.status(201).json({
    id: 2,
    product,
    quantity,
    status: 'pending'
  });
});

if (require.main === module) {
  app.listen(3001, () => {
    console.log('Order Service running on port 3001');
  });
}

export default app;
