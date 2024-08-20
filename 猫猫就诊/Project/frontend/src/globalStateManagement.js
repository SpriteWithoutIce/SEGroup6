import { GlobalState } from './global.js';

export default {
  updateIdentityNum(newVal) {
    GlobalState.identityNum = newVal; 
  },
};