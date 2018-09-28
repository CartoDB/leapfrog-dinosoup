import Vue from "vue";
import Vuex from "vuex";
import api from "./api";

Vue.use(Vuex);

const state = {
  appDialogVisible: false,
  appDialogId: null,
  apps: []
};

const getters = {
  activeApp(state) {
    console.log("BOOM!");
    if (!state.appDialogId) {
      return {};
    }

    let index = -1;
    state.apps.forEach((app, idx) => {
      if (app.name === state.appDialogId && index === -1) {
        index = idx;
      }
    });
    if (index > -1) {
      if (state.apps[index].deploys_list.length > 0) {
        console.log("mierda");
      }
      return state.apps[index];
    } else {
      return {};
    }
  },

  getVisible(state) {
    return state.appDialogVisible;
  }
};

const mutations = {
  setActiveApp(state, id) {
    state.appDialogId = id;
  },

  closeAppDialog(state) {
    state.appDialogVisible = false;
  },

  loadApps(state, apps) {
    state.apps = apps;
  },

  updateAppInfo(state, appInfo) {
    let index = -1;
    state.apps.forEach((app, idx) => {
      if (app.name === appInfo.name && index === -1) {
        index = idx;
      }
    });
    if (index > -1) {
      state.apps[index] = { ...state.apps[index], ...appInfo };
    } else {
      state.apps.push(appInfo);
    }
  },

  updateCommitList(state, appInfo) {
    let index = -1;
    state.apps.forEach((app, idx) => {
      if (app.name === appInfo.name && index === -1) {
        index = idx;
      }
    });
    if (index > -1) {
      state.apps[index].deploys_list = appInfo.deploys_list;
      state.appDialogId = "";
      state.appDialogId = appInfo.name;
    }
  },

  openDialog(state, name) {
    state.appDialogId = name;
    state.appDialogVisible = true;
  }
};

const actions = {
  initialLoad({ commit }) {
    api.getApps().then(apps => {
      commit("loadApps", apps);
    });
  },

  createApp({ commit, dispatch }, payload) {
    api.createApp(payload.name, payload.description).then(newApp => {
      commit("setActiveApp", newApp.name);
      dispatch("initialLoad");
    });
  },

  loadAddAndOpenDialog({ commit }, name) {
    api.getApp(name).then(app => {
      commit("updateAppInfo", app);
      commit("openDialog", app.name);
    });
  },

  updateApp({ commit }, name) {
    api.getApp(name).then(app => {
      commit("updateAppInfo", app);
    });
  },

  updateCommitList({ commit }, name) {
    api.getApp(name).then(app => {
      commit("updateCommitList", app);
    });
  }
};

export default new Vuex.Store({
  state,
  getters,
  mutations,
  actions
});
