<template>
  <div class="dialog">
    <div class="overlay"></div>
    <div class="box">
      <div class="close" v-on:click="closeDialog">
        <img class="close-icon" src="../assets/close.svg" />
      </div>
      <h2 class="text-title text-bold">{{ formattedAppName }}</h2>
      <div v-if="!activeApp.name">
        <div class="form">
          <div class="input-field">
            <label>Application name</label>
            <input v-model="name">
          </div>
          <div class="input-field">
            <label>Description</label>
            <input v-model="description">
          </div>
        </div>
        <button class="button" v-on:click="createApp">Create application</button>
      </div>
      <div v-else class="info">
        <div class="description">{{ activeApp.description }}</div>
        <div class="block">
          <div class="label">Deploy instructions</div>
          <ul class="instructions">
            <li v-for="(instruction, index) in activeApp.deploy_instructions" :key="index">
              <div class="instruction mono">{{ instruction }}</div>
            </li>
          </ul>
        </div>
        <div class="block">
          <div class="label">Your application URL</div>
          <div class="app-url"><a :href="activeApp.url">{{activeApp.url}}</a></div>
        </div>
        <div class="block">
          <div class="label">Stack</div>
          <StackLogo :tech="activeApp.stack" />
        </div>
        <div class="block deploys">
          <div class="label">Deploys</div>
          <div class="deploy" v-for="(deploy, index) in activeApp.deploys_list" :key="index">
            <div class="hash"><a href="#">{{ deploy.commit_hash_abbreviated }}</a></div>
            <div class="created_at">{{ deploy.created_at }}</div>
            <StatusTag :status="deploy.status" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import StackLogo from "./StackLogo.vue";
import StatusTag from "./StatusTag.vue";

export default {
  components: {
    StackLogo,
    StatusTag
  },

  data: function () {
    return {
      name: '',
      description: ''
    }
  },

  computed: {
    formattedAppName () {
      const activeApp = this.$store.getters.activeApp;
      return activeApp.name
        ? activeApp.name
        : 'Create new LI application';
    },

    activeApp () {
      return this.$store.getters.activeApp;
    },
  },

  mounted() {
    this.intervalId = setInterval(() => {
      if (this.$store.state.appDialogId) {
        // this.$store.dispatch("updateCommitList", this.$store.state.appDialogId);
        this.$store.dispatch("updateApp", this.$store.state.appDialogId);
      }
    }, 2000);
  },

  beforeDestroy() {
    clearInterval(this.intervalId);
  },
  methods: {
    closeDialog() {
      this.$store.commit("closeAppDialog");
    },

    createApp() {
      this.$store.dispatch("createApp", {
        name: this.name,
        description: this.description
      });
    }
  }
}

</script>

<style scoped lang="scss">
@import "../styles/_typography";
@import "../styles/_colors";

.dialog {
  position: relative;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;

  h2 {
    margin: 0 0 32px 0;
  }
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  background-color: rgba(79, 185, 159, 0.8);
  z-index: 20;
}

.close {
  position: absolute;
  top: 0;
  right: 0;
  width: 64px;
  height: 64px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

.close-icon {
  width: 24px;
  height: 24px;
}

.box {
  position: relative;
  padding: 96px;
  background-color: #FFF;
  z-index: 21;
  max-width: 920px;  
}

.form {
  margin-bottom: 48px;
}

.input-field {
  input {
    margin-bottom: 32px;
    padding: 8px 0;
    border: none;
    border-bottom: 1px solid $color-ui-03;
    width: 100%;
    outline: none;
    font-size: 16px;
  }

  input:focus {
    border-bottom: 1px solid $color-ok;
    box-shadow: 0 1px 0 0 $color-ok;
  }
}

.description {
  margin-top: 16px;
  margin-bottom: 48px !important; 
  font: 16px/24px $font-family-body;
}

.block {
  margin-bottom: 32px;
}

.label {
  font: 16px/16px "Open Sans", sans-serif;
  margin-bottom: 8px !important;
}

.mono {
  font: 16px "Overpass Mono", sans-serif;
}

.repo_path {
  background-color: #000000;
  color: #00EE00;
  padding: 8px;
}

.instructions {
  list-style: none;
  background-color: #000000;
  color: #00EE00;
  padding: 16px;

  & > li {
    padding: 0;
    margin-bottom: 8px;
  }

  & > li:last-child {
    margin-bottom: 0;
  }
}

.app-url {
  font: 16px/24px $font-family-body;

  a:link {
    text-decoration: none;
    color: $color-ok;
  }
}

.deploy {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;

  .hash {
    font: 12px "Overpass Mono", sans-serif;

    a:link {
      text-decoration: none;
      color: $color-ok;
    }

  }
}
</style>

// hash

// created_at

// 
