import pact from '@pact-foundation/pact-node';
import * as path from 'path';

const opts = {
  pactFilesOrDirs: [path.resolve(__dirname, '../../day-1-consumer-pact/pacts')],
  pactBroker: 'http://localhost:9292',
  pactBrokerUsername: 'pactbroker',
  pactBrokerPassword: 'pactbroker',
  consumerVersion: '1.0.0',
  tags: ['dev']
};

pact
  .publishPacts(opts)
  .then(() => {
    console.log('Pacts successfully published to broker!');
  })
  .catch((e) => {
    console.error('Failed to publish pacts:', e);
    process.exit(1);
  });
