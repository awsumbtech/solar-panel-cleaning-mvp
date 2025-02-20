import { useEffect } from 'react';
import { AppNavigator } from './src/navigation/AppNavigator';
import ApiService from './src/services/api';

export default function App() {
  useEffect(() => {
    // Initialize the API service
    ApiService.init();
  }, []);

  return <AppNavigator />;
} 