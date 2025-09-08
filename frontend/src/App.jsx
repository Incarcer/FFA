import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchInitialState } from './slices/draftslice';
import { socketService } from './services/socketservice';

// It's convention to keep imports clean - you can organize these as you see fit
import Header from './components/layout/Header';
import StatusBar from './components/layout/StatusBar';
import DraftBoard from './components/draftboard/DraftBoard';
import TeamRosters from './components/teamrosters/TeamRosters';
import RecommendationPanel from './components/recommendationpanel/RecommendationPanel';
import PlayerDetails from './components/playerdetails/PlayerDetails';
import PlayerPool from './components/playerpool/PlayerPool';

function App() {
  const dispatch = useDispatch();
  const draftStatus = useSelector((state) => state.draft.status);
  const selectedPlayer = useSelector((state) => state.draft.selectedPlayerDetails);

  useEffect(() => {
    socketService.connect(dispatch);

    if (draftStatus === 'idle') {
      dispatch(fetchInitialState());
    }

    return () => {
      socketService.disconnect();
    };
  }, [dispatch, draftStatus]);

  return (
    <div className="app-container">
      <Header />
      <StatusBar />
      <main className="main-content">
        <DraftBoard />
        <div className="sidebar">
            <PlayerPool />
            <RecommendationPanel />
        </div>
      </main>
      <TeamRosters />
      
      {/* Conditionally render PlayerDetails based on selectedPlayer state */}
      {selectedPlayer && (
        <PlayerDetails 
          player={selectedPlayer} 
        />
      )}
    </div>
  );
}

export default App;
