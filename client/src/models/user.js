import axios from "axios";

const baseURL = "/api/user/";

export default {
  getUserImages(username, params) {
    return axios.get(baseURL + `${username}/images`, {
      params: {
        ...params
      }
    });
  },
};
