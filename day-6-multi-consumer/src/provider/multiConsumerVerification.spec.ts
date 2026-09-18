import { Verifier } from '@pact-foundation/pact';
import app from './orderServiceMulti';
import * as path from 'path';

describe('Multi-Consumer Verification', () => {
  let server: any;
  beforeAll(() => {
    server = app.listen(8083, () => console.log('Multi-provider running on 8083'));
  });
  afterAll(() => {
    if (server) server.close();
  });

  it('validates against multiple consumers', async () => {
    const pactsDir = path.resolve(__dirname, '../../pacts');
    const verifier = new Verifier({
      providerBaseUrl: 'http://localhost:8083',
      pactUrls: [
        path.resolve(pactsDir, 'RecommendationConsumer-OrderServiceProvider.json'),
        path.resolve(pactsDir, 'AnalyticsConsumer-OrderServiceProvider.json')
      ],
      stateHandlers: {
        'user 123 has orders': async () => {},
        'orders exist for stats': async () => {}
      }
    });
    await verifier.verifyProvider();
  });
});
