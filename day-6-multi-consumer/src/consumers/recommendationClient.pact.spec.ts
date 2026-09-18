import { PactV3, MatchersV3 } from '@pact-foundation/pact';
import { RecommendationClient } from './recommendationClient';
import * as path from 'path';

const { eachLike, like, integer } = MatchersV3;
const provider = new PactV3({
  consumer: 'RecommendationConsumer',
  provider: 'OrderServiceProvider',
  dir: path.resolve(process.cwd(), 'pacts'),
});

describe('Recommendation Client Pact', () => {
  it('returns order history', () => {
    provider
      .given('user 123 has orders')
      .uponReceiving('a request for order history')
      .withRequest({ method: 'GET', path: '/orders', query: { userId: '123' } })
      .willRespondWith({
        status: 200,
        body: eachLike({ id: integer(1), product: like('Widget') })
      });
    return provider.executeTest(async (mock) => {
      const client = new RecommendationClient(mock.url);
      const data = await client.getOrderHistory('123');
      expect(data).toHaveLength(1);
    });
  });
});
