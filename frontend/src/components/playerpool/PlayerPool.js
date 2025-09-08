import react, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchPlayerHistory } from '../../slices/draftslice';


const playerpool = () => {
  const dispatch = useDispatch();
  const availableplayers = useSelector((state) => state.draft.availableplayers);
  const [searchterm, setsearchterm] = useState('');
  //...
  
  const handleplayerclick = (playerid) => {
    dispatch(fetchplayerhistory(playerid));
  };
  
  // ... filtering logic ...


  return (
  <div>Player Pool Table Placeholder</div>
);
};
