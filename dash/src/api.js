const BASE_URL = "http://carto.ku:8000";
const user = "wadus";
const apps = "apps";

export default {
  getApp(appId) {
    const url = `${BASE_URL}/${user}/${apps}/${appId}`;
    return fetch(url, {
      mode: "cors"
    })
      .then(response => response.json())
      .then(json => {
        console.log(json.deploys_list.length);
        return json;
      })
      .catch(error => {
        console.error(error);
      });
  },

  getApps() {
    const url = `${BASE_URL}/${user}/${apps}`;
    return fetch(url, {
      mode: "cors"
    })
      .then(response => response.json())
      .then(json => {
        return json.apps.reverse();
      })
      .catch(error => {
        console.error(error);
      });
  },

  createApp(name, description) {
    const url = `${BASE_URL}/${user}/${apps}`;
    const data = new FormData();
    data.append("name", name);
    data.append("description", description);

    return fetch(url, {
      method: "POST",
      body: data
    })
      .then(response => response.json())
      .then(json => {
        return json;
      });
  }
};
