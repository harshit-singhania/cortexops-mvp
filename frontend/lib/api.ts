import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const endpoints = {
  chat: (query: string) => api.post('/query/chat', { query }),
  rootCause: (logData: string, context?: string) => 
    api.post('/query/rootcause', { log_data: logData, context }),
  generateDocs: (serviceName: string, description: string, metadata: any) => 
    api.post('/query/docs/generate', { service_name: serviceName, description, metadata }),
};
