import axios from 'axios';

const instance = axios.create({
  baseURL: '/////', // Change this to  API base URL
});

export default instance;