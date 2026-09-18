import { PactV3, MatchersV3 } from '@pact-foundation/pact';
import { AnalyticsClient } from './analyticsClient';
import * as path from 'path';

const provider = new PactV3({
  consumer: 'AnalyticsConsumer',
  provider: 'OrderServiceProvider',
  dir: path.resolve(process.cwd(), 'pacts'),
});

describe('Analytics Client Pact', () => {
  it('returns order stats', () => {
    provider
      .given('orders exist for stats')
      .uponReceiving('a request for order stats')
      .withRequest({ method: 'GET', path: '/orders/stats' })
      .willRespondWith({
        status: 200,
        body: { totalOrders: MatchersV3.integer(100), totalRevenue: MatchersV3.decimal(2500.50) }
      });
    return provider.executeTest(async (mock) => {
      const client = new AnalyticsClient(mock.url);
      const data = await client.getStats();
      expect(data.totalOrders).toEqual(100);
    });
  });
});
