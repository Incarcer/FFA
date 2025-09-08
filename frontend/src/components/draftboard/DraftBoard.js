import react from 'react';
import { useSelector } from 'react-redux';


const draftboard = () => {
  const { board, currentpickindex, status } = useSelector((state) => state.draft);
  // ...
  return (
    <div classname="panel draft-board-container">
      {/* ... */}
      <div classname="draft-board-grid">
        {board.map((pick) => (
          <div
            key={pick.pick_number}
            classname={`draft-pick-cell ${pick.pick_number === currentpickindex + 1 ? 'current-pick' : ''}`}
          >
            <div classname="pick-number">{pick.pick_number}</div>
            {pick.player ? (
              <>
                <div classname="player-name">{pick.player.player_name}</div>
                <div classname="player-info">{pick.player.position}</div>
              </>
            ) : null}
          </div>
        ))}
      </div>
    </div>
  );
};
