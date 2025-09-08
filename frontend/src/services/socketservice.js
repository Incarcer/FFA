import { io } from 'socket.io-client';
import { updateRecommendations } from '../slices/recommendationslice';
import { addPick } from '../slices/draftslice';

// Use Vite's environment variable handling, as specified in your summary.
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class SocketService {
  socket;

  connect(dispatch) {
    console.log(`Connecting socket to ${API_URL}`);
    this.socket = io(API_URL, {
      path: '/socket.io/',
      transports: ['websocket'],
    });

    this.socket.on('connect', () => {
      console.log('Socket connected:', this.socket.id);
    });

    this.socket.on('connect_error', (error) => {
        console.error('Socket connection error:', error.message);
        console.error(`Failed to connect to backend at ${API_URL}. Ensure the backend container is running and there are no network issues.`);
    });

    this.socket.on('draft_update', (data) => {
      console.log('Received draft_update:', data);
      // Dispatch an action to update Redux store with new pick data
      dispatch(addPick(data));
    });

    this.socket.on('recommendation_update', (data) => {
      console.log('Received recommendation_update:', data);
      // Dispatch an action to update recommendations
      dispatch(updateRecommendations(data.recommendations));
    });
    
    this.socket.on('error', (error) => {
      console.error('Socket server-side error:', error.message);
    });
  }

  disconnect() {
    if (this.socket) {
      console.log('Disconnecting socket.');
      this.socket.disconnect();
    }
  }
}

export const socketService = new SocketService();
