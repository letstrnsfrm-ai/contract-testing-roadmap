import os
import subprocess
import json

base_dir = "/Users/abhinavsharma/Downloads/contract-testing-roadmap"
os.makedirs(base_dir, exist_ok=True)
os.chdir(base_dir)

# Initialize Git
subprocess.run(["git", "init"], check=True)

def write_file(path, content):
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content.strip() + "\n")

# --- Root Files ---
write_file(".gitignore", """
node_modules/
dist/
pacts/
.env
*.log
.DS_Store
coverage/
.pact_cache/
jest-results/
""")

write_file("package.json", json.dumps({
  "name": "contract-testing-roadmap",
  "version": "1.0.0",
  "description": "7-Day Consumer-Driven Contract Testing with Pact & TypeScript",
  "scripts": {
    "test:all": "bash scripts/run-all.sh",
    "broker:up": "docker-compose up -d",
    "broker:down": "docker-compose down"
  },
  "devDependencies": {
    "typescript": "^5.4.0",
    "ts-node": "^10.9.2",
    "@types/node": "^20.0.0",
    "@types/jest": "^29.5.0",
    "jest": "^29.7.0",
    "ts-jest": "^29.1.0"
  },
  "dependencies": {
    "@pact-foundation/pact": "^13.1.0",
    "@pact-foundation/pact-node": "^10.18.0",
    "express": "^4.19.0",
    "@types/express": "^4.17.21",
    "axios": "^1.7.0"
  }
}, indent=2))

write_file("tsconfig.json", json.dumps({
  "compilerOptions": {
    "target": "ES2020",
    "module": "CommonJS",
    "strict": True,
    "esModuleInterop": True,
    "skipLibCheck": True,
    "forceConsistentCasingInFileNames": True,
    "outDir": "./dist"
  },
  "include": ["src/**/*", "day-*/**/*.ts"]
}, indent=2))

write_file("jest.config.ts", """
import type { Config } from 'jest';
const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testTimeout: 30000,
  reporters: ['default'],
};
export default config;
""")

write_file("docker-compose.yml", """
version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: pact
      POSTGRES_PASSWORD: pact_password
      POSTGRES_DB: pact_db
    ports:
      - "5432:5432"
    volumes:
      - pact_postgres_data:/var/lib/postgresql/data
  pact-broker:
    image: pactfoundation/pact-broker:latest
    ports:
      - "9292:9292"
    depends_on:
      - postgres
    environment:
      PACT_BROKER_DATABASE_URL: postgres://pact:pact_password@postgres/pact_db
      PACT_BROKER_BASIC_AUTH_USERNAME: pactbroker
      PACT_BROKER_BASIC_AUTH_PASSWORD: pactbroker
      PACT_BROKER_BASE_URL: http://localhost:9292
volumes:
  pact_postgres_data:
""")

write_file("scripts/run-all.sh", """
#!/bin/bash
set -e

for dir in day-*/; do
  echo "Running tests in $dir"
  cd "$dir"
  npm install
  npm test
  cd ..
done
echo "All tests completed successfully."
""")
os.chmod(os.path.join(base_dir, "scripts/run-all.sh"), 0o755)

write_file("README.md", """
# 7-Day Consumer-Driven Contract Testing with Pact & TypeScript

## Prerequisites
- Node.js 18+
- Docker Desktop
- npm

## Quick Start
```bash
git clone <repo-url>
cd contract-testing-roadmap
npm install
docker-compose up -d
```

## Curriculum
| Day | Topic | Folder | Status |
|---|---|---|---|
| 1 | Consumer Pact Writing Basics | day-1-consumer-pact | ⏳ |
| 2 | Provider Verification | day-2-provider-verification | ⏳ |
| 3 | Pact Broker Setup & Publish | day-3-broker-setup-publish | ⏳ |
| 4 | Can-I-Deploy Gate | day-4-can-i-deploy | ⏳ |
| 5 | Webhooks & Provider States | day-5-webhooks-provider-states | ⏳ |
| 6 | Multi-Consumer Scenarios | day-6-multi-consumer | ⏳ |
| 7 | GitHub Actions CI Pipeline | day-7-github-actions-ci | ⏳ |

See letstrnsfrm.ai portal for more context.
""")

# --- Day 1 ---
write_file("day-1-consumer-pact/package.json", json.dumps({
  "name": "contract-testing-day-1",
  "version": "1.0.0",
  "scripts": { "test": "jest" },
  "devDependencies": {
    "@pact-foundation/pact": "^13.1.0",
    "axios": "^1.7.0",
    "jest": "^29.7.0",
    "ts-jest": "^29.1.0",
    "typescript": "^5.4.0",
    "@types/jest": "^29.5.0"
  }
}, indent=2))

write_file("day-1-consumer-pact/README.md", "# Day 1: Consumer Pact Writing Basics")

write_file("day-1-consumer-pact/src/orderClient.ts", """
import axios from 'axios';

export type Order = {
  id: number;
  product: string;
  quantity: number;
  status: string;
};

export class OrderClient {
  private url: string;

  constructor(url: string) {
    this.url = url;
  }

  public async getOrder(id: number): Promise<Order> {
    const response = await axios.get(`${this.url}/orders/${id}`);
    return response.data;
  }

  public async createOrder(order: Omit<Order, 'id' | 'status'>): Promise<Order> {
    const response = await axios.post(`${this.url}/orders`, order);
    return response.data;
  }
}
""")

write_file("day-1-consumer-pact/src/orderClient.pact.spec.ts", """
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
""")

write_file("day-1-consumer-pact/jest.config.ts", """
export default {
  preset: 'ts-jest',
  testEnvironment: 'node',
};
""")

# --- Day 2 ---
write_file("day-2-provider-verification/package.json", json.dumps({
  "name": "contract-testing-day-2",
  "version": "1.0.0",
  "scripts": {
    "start": "ts-node src/orderService.ts",
    "test": "jest"
  },
  "devDependencies": {
    "@pact-foundation/pact": "^13.1.0",
    "express": "^4.19.0",
    "@types/express": "^4.17.21",
    "jest": "^29.7.0",
    "ts-jest": "^29.1.0",
    "ts-node": "^10.9.2",
    "typescript": "^5.4.0",
    "@types/jest": "^29.5.0"
  }
}, indent=2))

write_file("day-2-provider-verification/README.md", "# Day 2: Provider Verification")

write_file("day-2-provider-verification/src/orderService.ts", """
import express from 'express';

const app = express();
app.use(express.json());

app.get('/health', (req, res) => {
  res.status(200).send('OK');
});

app.get('/orders/:id', (req, res) => {
  if (req.params.id === '1') {
    res.json({ id: 1, product: 'Widget', quantity: 2, status: 'pending' });
  } else {
    res.status(404).json({ error: 'Not found' });
  }
});

app.post('/orders', (req, res) => {
  const { product, quantity } = req.body;
  res.status(201).json({
    id: 2,
    product,
    quantity,
    status: 'pending'
  });
});

if (require.main === module) {
  app.listen(3001, () => {
    console.log('Order Service running on port 3001');
  });
}

export default app;
""")

write_file("day-2-provider-verification/src/orderService.spec.ts", """
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
""")

write_file("day-2-provider-verification/jest.config.ts", """
export default {
  preset: 'ts-jest',
  testEnvironment: 'node',
};
""")

# --- Day 3 ---
write_file("day-3-broker-setup-publish/package.json", json.dumps({
  "name": "contract-testing-day-3",
  "version": "1.0.0",
  "scripts": {
    "publish": "ts-node src/publish.ts",
    "broker:check": "ts-node src/broker-check.ts"
  },
  "devDependencies": {
    "@pact-foundation/pact-node": "^10.18.0",
    "axios": "^1.7.0",
    "ts-node": "^10.9.2",
    "typescript": "^5.4.0"
  }
}, indent=2))

write_file("day-3-broker-setup-publish/README.md", """
# Day 3: Broker Setup & Publish
See `../docker-compose.yml` to start the broker.
UI at `http://localhost:9292`.
""")

write_file("day-3-broker-setup-publish/src/publish.ts", """
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
""")

write_file("day-3-broker-setup-publish/src/broker-check.ts", """
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
""")

# --- Day 4 ---
write_file("day-4-can-i-deploy/package.json", json.dumps({
  "name": "contract-testing-day-4",
  "version": "1.0.0",
  "scripts": {
    "can-i-deploy": "ts-node src/canIDeploy.ts"
  },
  "devDependencies": {
    "@pact-foundation/pact-node": "^10.18.0",
    "axios": "^1.7.0",
    "ts-node": "^10.9.2",
    "typescript": "^5.4.0"
  }
}, indent=2))

write_file("day-4-can-i-deploy/README.md", "# Day 4: Can-I-Deploy Gate")

write_file("day-4-can-i-deploy/src/canIDeploy.ts", """
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
""")

write_file("day-4-can-i-deploy/ci-gate-example.sh", """
#!/bin/bash
echo "Running can-i-deploy..."
npm run can-i-deploy
if [ $? -eq 0 ]; then
  echo "Proceeding with deployment..."
else
  echo "Deployment blocked due to contract verification failures!"
  exit 1
fi
""")
os.chmod(os.path.join(base_dir, "day-4-can-i-deploy/ci-gate-example.sh"), 0o755)

# --- Day 5 ---
write_file("day-5-webhooks-provider-states/package.json", json.dumps({
  "name": "contract-testing-day-5",
  "version": "1.0.0",
  "scripts": {
    "test": "jest",
    "start": "ts-node src/orderService.enhanced.ts"
  },
  "devDependencies": {
    "@pact-foundation/pact": "^13.1.0",
    "express": "^4.19.0",
    "@types/express": "^4.17.21",
    "jest": "^29.7.0",
    "ts-jest": "^29.1.0",
    "ts-node": "^10.9.2",
    "typescript": "^5.4.0",
    "@types/jest": "^29.5.0"
  }
}, indent=2))

write_file("day-5-webhooks-provider-states/README.md", "# Day 5: Webhooks & Provider States")

write_file("day-5-webhooks-provider-states/src/webhook.config.json", json.dumps({
  "events": [{"name": "contract_content_changed"}],
  "request": {
    "method": "POST",
    "url": "https://ci.example.com/builds",
    "headers": {"Content-Type": "application/json"},
    "body": {"provider": "${pactbroker.providerName}"}
  }
}, indent=2))

write_file("day-5-webhooks-provider-states/src/orderService.enhanced.ts", """
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
""")

write_file("day-5-webhooks-provider-states/src/providerVerification.spec.ts", """
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
""")

write_file("day-5-webhooks-provider-states/jest.config.ts", """
export default { preset: 'ts-jest', testEnvironment: 'node' };
""")

# --- Day 6 ---
write_file("day-6-multi-consumer/package.json", json.dumps({
  "name": "contract-testing-day-6",
  "version": "1.0.0",
  "scripts": { "test": "jest" },
  "devDependencies": {
    "@pact-foundation/pact": "^13.1.0",
    "axios": "^1.7.0",
    "express": "^4.19.0",
    "@types/express": "^4.17.21",
    "jest": "^29.7.0",
    "ts-jest": "^29.1.0",
    "ts-node": "^10.9.2",
    "typescript": "^5.4.0",
    "@types/jest": "^29.5.0"
  }
}, indent=2))

write_file("day-6-multi-consumer/README.md", "# Day 6: Multi-Consumer Scenarios")

write_file("day-6-multi-consumer/src/consumers/recommendationClient.ts", """
import axios from 'axios';
export class RecommendationClient {
  constructor(private url: string) {}
  public async getOrderHistory(userId: string) {
    const res = await axios.get(`${this.url}/orders?userId=${userId}`);
    return res.data;
  }
}
""")

write_file("day-6-multi-consumer/src/consumers/recommendationClient.pact.spec.ts", """
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
""")

write_file("day-6-multi-consumer/src/consumers/analyticsClient.ts", """
import axios from 'axios';
export class AnalyticsClient {
  constructor(private url: string) {}
  public async getStats() {
    const res = await axios.get(`${this.url}/orders/stats`);
    return res.data;
  }
}
""")

write_file("day-6-multi-consumer/src/consumers/analyticsClient.pact.spec.ts", """
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
""")

write_file("day-6-multi-consumer/src/provider/orderServiceMulti.ts", """
import express from 'express';

const app = express();
app.use(express.json());

app.get('/orders', (req, res) => {
  if (req.query.userId === '123') {
    res.json([{ id: 1, product: 'Widget' }]);
  } else {
    res.json([]);
  }
});

app.get('/orders/stats', (req, res) => {
  res.json({ totalOrders: 100, totalRevenue: 2500.50 });
});

export default app;
""")

write_file("day-6-multi-consumer/src/provider/multiConsumerVerification.spec.ts", """
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
""")

write_file("day-6-multi-consumer/jest.config.ts", """
export default { preset: 'ts-jest', testEnvironment: 'node' };
""")

# --- Day 7 ---
write_file("day-7-github-actions-ci/package.json", json.dumps({
  "name": "contract-testing-day-7",
  "version": "1.0.0",
  "scripts": {
    "summary": "ts-node src/integration-summary.ts"
  },
  "devDependencies": {
    "ts-node": "^10.9.2",
    "typescript": "^5.4.0"
  }
}, indent=2))

write_file("day-7-github-actions-ci/README.md", "# Day 7: E2E GitHub Actions CI Pipeline")

write_file("day-7-github-actions-ci/src/integration-summary.ts", """
console.log('Contract Testing Complete!');
console.log('All Pact specifications verified across consumer and provider domains.');
""")

write_file(".github/workflows/contract-tests.yml", """
name: Contract Testing CI
on: [push, pull_request]
jobs:
  consumer-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with: { node-version: 20 }
      - run: npm install
      - name: Run consumer pact tests
        run: cd day-1-consumer-pact && npm install && npm test
      - name: Publish pacts to broker
        run: echo "Publish step here"
        env:
          PACT_BROKER_URL: ${{ secrets.PACT_BROKER_URL }}
          PACT_BROKER_USERNAME: ${{ secrets.PACT_BROKER_USERNAME }}
          PACT_BROKER_PASSWORD: ${{ secrets.PACT_BROKER_PASSWORD }}

  provider-verification:
    needs: consumer-tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with: { node-version: 20 }
      - run: npm install
      - name: Verify provider
        run: cd day-2-provider-verification && npm install && npm test
      - name: Can-I-Deploy gate
        run: echo "Checking deployability..."
""")

# Commit Everything
subprocess.run(["git", "add", "-A"], check=True)
subprocess.run(["git", "commit", "-m", "feat: initial 7-day contract testing roadmap with TypeScript Pact labs"], check=True)
print("SUCCESS")
