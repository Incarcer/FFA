import axios from 'axios';


// configure a base url for all api requests
const apiclient = axios.create({
  baseurl: '/api/v1',
  headers: {
    'content-type': 'application/json',
  },
});


export const apiservice = {
  async startdraft() {
    const response = await apiclient.post('/draft/start');
    return response.data;
  },


  async fetchdraftstate() {
    const response = await apiclient.get('/draft/state');
    return response.data;
  },


  async fetchplayerhistory(playerid) {
    const response = await apiclient.get(`/players/${playerid}/history`);
    return response.data;
  },


  async getrecommendations() {
    const response = await apiclient.get('/draft/recommendations');
    return response.data;
  }
};
