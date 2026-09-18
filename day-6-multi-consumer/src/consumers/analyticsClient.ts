import axios from 'axios';
export class AnalyticsClient {
  constructor(private url: string) {}
  public async getStats() {
    const res = await axios.get(`${this.url}/orders/stats`);
    return res.data;
  }
}
