import pact from '@pact-foundation/pact-node';

async function checkDeploy() {
  try {
    await pact.canDeploy({
      pactBroker: 'http://localhost:9292',
      pactBrokerUsername: 'pactbroker',
      pactBrokerPassword: 'pactbroker',
      pacticipants: [
        { name: 'ShoppingCartConsumer', version: '1.0.0' },
        { name: 'OrderServiceProvider', latest: true }
      ],
      toEnvironment: 'production'
    });
    console.log('PASS: Can deploy!');
  } catch (e) {
    console.error('FAIL: Cannot deploy', e);
    process.exit(1);
  }
}
checkDeploy();
