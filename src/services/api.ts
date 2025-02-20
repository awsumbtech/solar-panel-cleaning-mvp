import AsyncStorage from '@react-native-async-storage/async-storage';
import { AuthResponse, LoginCredentials } from '../types/auth';

const API_URL = 'http://localhost:5000/api';

class ApiService {
  private static token: string | null = null;

  static async init() {
    this.token = await AsyncStorage.getItem('token');
  }

  private static async request(endpoint: string, options: RequestInit = {}) {
    const headers = {
      'Content-Type': 'application/json',
      ...(this.token ? { Authorization: `Bearer ${this.token}` } : {}),
      ...options.headers,
    };

    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'An error occurred');
    }

    return response.json();
  }

  static async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });

    this.token = response.token;
    await AsyncStorage.setItem('token', response.token);
    return response;
  }

  static async logout() {
    this.token = null;
    await AsyncStorage.removeItem('token');
  }

  // Add more API methods here as needed
}

export default ApiService; 