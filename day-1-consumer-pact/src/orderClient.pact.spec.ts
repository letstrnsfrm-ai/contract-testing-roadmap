import { PactV3, MatchersV3 } from '@pact-foundation/pact';
import { OrderClient } from './orderClient';
import * as path from 'path';

const { like, integer } = MatchersV3;

const provider = new PactV3({
  consumer: 'ShoppingCartConsumer',
  provider: 'OrderServiceProvider',
  dir: path.resolve(process.cwd(), 'pacts'),
});

describe('OrderClient API Contract', () => {
  describe('GET /orders/:id', () => {
    it('returns an order', () => {
      provider
        .given('order 1 exists')
        .uponReceiving('a request for order 1')
        .withRequest({
          method: 'GET',
          path: '/orders/1',
        })
        .willRespondWith({
          status: 200,
          body: {
            id: integer(1),
            product: like('Widget'),
            quantity: integer(2),
            status: like('pending'),
          },
        });

      return provider.executeTest(async (mockserver) => {
        const client = new OrderClient(mockserver.url);
        const order = await client.getOrder(1);
        expect(order.id).toEqual(1);
        expect(order.product).toEqual('Widget');
      });
    });
  });

  describe('POST /orders', () => {
    it('creates an order', () => {
      provider
        .given('no orders exist')
        .uponReceiving('a request to create an order')
        .withRequest({
          method: 'POST',
          path: '/orders',
          headers: { 'Content-Type': 'application/json' },
          body: {
            product: like('Gadget'),
            quantity: integer(5),
          },
        })
        .willRespondWith({
          status: 201,
          body: {
            id: integer(2),
            product: like('Gadget'),
            quantity: integer(5),
            status: like('pending'),
          },
        });

      return provider.executeTest(async (mockserver) => {
        const client = new OrderClient(mockserver.url);
        const order = await client.createOrder({ product: 'Gadget', quantity: 5 });
        expect(order.id).toBeDefined();
        expect(order.status).toEqual('pending');
      });
    });
  });
});
