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
