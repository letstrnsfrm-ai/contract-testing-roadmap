import { Verifier } from '@pact-foundation/pact';
import app from './orderService.enhanced';
import * as path from 'path';

describe('Pact Verification with States', () => {
  let server: any;
  beforeAll(() => {
    server = app.listen(8082, () => console.log('Test provider running on port 8082'));
  });
  afterAll(() => {
    if (server) server.close();
  });

  it('validates the expectations against the local pact file', async () => {
    const pactFile = path.resolve(
      __dirname,
      '../../day-1-consumer-pact/pacts/ShoppingCartConsumer-OrderServiceProvider.json'
    );
    const verifier = new Verifier({
      providerBaseUrl: 'http://localhost:8082',
      pactUrls: [pactFile],
      providerStatesSetupUrl: 'http://localhost:8082/_pact/provider_states'
    });
    await verifier.verifyProvider();
  });
});
