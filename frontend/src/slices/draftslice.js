import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
 
import { apiservice } from '../services/apiservice';


const initialState = {
  board: [],
  teams: {},
  availableplayers: [],
  currentpickindex: 0,
  totalpicks: 0,
  selectedplayerdetails: null,
  status: 'idle', // 'idle' | 'loading' | 'succeeded' | 'failed'
  error: null,
};


// async thunk to fetch the complete initial state from the api
export const fetchinitialstate = createAsyncThunk('draft/fetchinitialstate', async () => {
  const response = await apiservice.fetchdraftstate();
  return response;
});


// async thunk to fetch detailed history for a selected player
export const fetchplayerhistory = createAsyncThunk('draft/fetchplayerhistory', async (playerid, { rejectwithvalue }) => {
    try {
        const response = await apiservice.fetchplayerhistory(playerid);
        return response;
    } catch (error) {
        return rejectwithvalue(error.response.data);
    }
});


const draftslice = createSlice({
  name: 'draft',
  initialstate,
  reducers: {
    // reducer for handling live pick updates from the websocket
    processpick: (state, action) => {
      const { pick_number, player } = action.payload;


      // 1. update the pick on the board
      const pickindexonboard = state.board.findindex(p => p.pick_number === pick_number);
      if (pickindexonboard !== -1) {
        state.board[pickindexonboard].player = player;
      }


      // 2. remove the player from the available pool
      state.availableplayers = state.availableplayers.filter(p => p.player_id !== player.player_id);


      // 3. add player to the correct team's roster
      const teamid = state.board[pickindexonboard].team_id;
      const team = state.teams[teamid];
      if (team) {
        if (!team.roster[player.position]) {
          team.roster[player.position] = [];
        }
        team.roster[player.position].push(player);
      }
      
      // 4. update the current pick index
      state.currentpickindex = pick_number;
    },
    clearselectedplayer: (state) => {
      state.selectedplayerdetails = null;
    }
  },
  extrareducers: (builder) => {
    builder
      // handling fetchinitialstate
      .addcase(fetchinitialstate.pending, (state) => {
        state.status = 'loading';
      })
      .addcase(fetchinitialstate.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.board = action.payload.board;
        state.teams = action.payload.teams;
        state.availableplayers = action.payload.available_players;
        state.currentpickindex = action.payload.current_pick_index;
        state.totalpicks = action.payload.total_picks;
      })
      .addcase(fetchinitialstate.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      })
      // handling fetchplayerhistory
      .addcase(fetchplayerhistory.pending, (state, action) => {
          // find player from availableplayers to show basic info while loading details
          const playerfrompool = state.availableplayers.find(p => p.player_id === action.meta.arg);
          state.selectedplayerdetails = { player: playerfrompool, history: null, loading: true };
      })
      .addcase(fetchplayerhistory.fulfilled, (state, action) => {
        if (state.selectedplayerdetails) {
            state.selectedplayerdetails.history = action.payload;
            state.selectedplayerdetails.loading = false;
        }
      })
      .addcase(fetchplayerhistory.rejected, (state, action) => {
        if (state.selectedplayerdetails) {
            state.selectedplayerdetails.loading = false;
            state.selectedplayerdetails.error = action.payload;
        }
      });
  },
});


export const { processpick, clearselectedplayer } = draftslice.actions;
export default draftslice.reducer;
