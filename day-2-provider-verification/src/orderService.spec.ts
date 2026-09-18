import { Verifier } from '@pact-foundation/pact';
import app from './orderService';
import * as path from 'path';

describe('Pact Verification', () => {
  let server: any;

  beforeAll(() => {
    server = app.listen(8081, () => {
      console.log('Test provider running on port 8081');
    });
  });

  afterAll(() => {
    if (server) {
      server.close();
    }
  });

  it('validates the expectations of ShoppingCartConsumer', async () => {
    const pactFile = path.resolve(
      __dirname,
      '../../day-1-consumer-pact/pacts/ShoppingCartConsumer-OrderServiceProvider.json'
    );

    const verifier = new Verifier({
      providerBaseUrl: 'http://localhost:8081',
      pactUrls: [pactFile],
      stateHandlers: {
        'order 1 exists': async () => {
          console.log('Setting up state: order 1 exists');
        },
        'no orders exist': async () => {
          console.log('Setting up state: no orders exist');
        }
      }
    });

    await verifier.verifyProvider();
  });
});
