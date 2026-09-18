import axios from 'axios';
export class RecommendationClient {
  constructor(private url: string) {}
  public async getOrderHistory(userId: string) {
    const res = await axios.get(`${this.url}/orders?userId=${userId}`);
    return res.data;
  }
}
