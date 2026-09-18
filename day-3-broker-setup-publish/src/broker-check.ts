import axios from 'axios';

async function check() {
  try {
    const res = await axios.get('http://localhost:9292/diag', {
      auth: { username: 'pactbroker', password: 'pactbroker' }
    });
    console.log('Broker status:', res.status, res.data);
  } catch (err) {
    console.error('Broker is unreachable', err);
    process.exit(1);
  }
}
check();
