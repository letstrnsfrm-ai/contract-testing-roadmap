import express from 'express';

const app = express();
app.use(express.json());

let orders: any[] = [];

app.post('/_pact/provider_states', (req, res) => {
  const state = req.body.state;
  if (state === 'order 1 exists') {
    orders = [{ id: 1, product: 'Widget', quantity: 2, status: 'pending' }];
  } else if (state === 'no orders exist') {
    orders = [];
  } else if (state === 'multiple orders exist') {
    orders = [
      { id: 1, product: 'Widget', quantity: 2, status: 'pending' },
      { id: 2, product: 'Gadget', quantity: 1, status: 'shipped' }
    ];
  }
  res.sendStatus(200);
});

app.get('/orders/:id', (req, res) => {
  const order = orders.find(o => o.id === parseInt(req.params.id));
  if (order) res.json(order);
  else res.status(404).json({ error: 'Not found' });
});

app.post('/orders', (req, res) => {
  const { product, quantity } = req.body;
  const newOrder = { id: 2, product, quantity, status: 'pending' };
  orders.push(newOrder);
  res.status(201).json(newOrder);
});

if (require.main === module) {
  app.listen(3002, () => console.log('Enhanced Order Service on 3002'));
}
export default app;
