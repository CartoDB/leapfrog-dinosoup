<template>
  <div class="application-card" v-on:click="handleClick">
    <div class="application-content">
      <img class="image" src="../assets/app-01.png"/>
      <div class="name">{{ app.name }}</div>
      <div class="description">{{ app.description}}</div>
      <div class="info">
        <div class="url">
          <a href="#">{{ app.domain }}</a>
        </div>
        <div>Last deploy <span class="text-bold">{{ lastDeployText }}</span></div>
        <div>{{ app.size }}</div>
      </div>
      <div class="logo-container">
        <StackLogo :tech="app.stack" />
      </div>
    </div>
    <div class="state">
      <p>{{ stateText }}</p>
    </div>
  </div>
</template>

<script>
import { format } from "date-fns/esm";
import StackLogo from "./StackLogo.vue";

export default {
  name: "application-card",

  components: {
    StackLogo
  },

  props: {
    app: Object
  },

  computed: {
    lastDeployText() {
      return format(new Date(this.app.lastDeploy), "MM/dd/yyyy");
    },

    stateText() {
      return this.app.state ? this.app.state : "No info about state";
    }
  },

  methods: {
    handleClick() {
      this.$store.dispatch("loadAddAndOpenDialog", this.app.name);
    }
  }
};
</script>

<style scoped lang="scss">
@import "../styles/_typography";
@import "../styles/_colors";

.application-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  cursor: pointer;
}

.application-content {
  padding: 16px;
  background-color: $color-ui-01;
  flex: 1;
  position: relative;
}

.image {
  height: 128px;
  width: 100%;
  object-fit: cover;
}

.name {
  margin-top: 24px;
  font: 16px/24px $font-family-body;
  font-weight: bold;
}

.url {
  font: 16px/24px $font-family-body;

  a:link {
    color: orange;
    text-decoration: none;
    color: $color-ok;
  }
}

.info {
  margin-top: 32px;

  font: 12px/18px $font-family-body;

  div {
    margin: 8px 0;
  }
}

.description {
  margin-top: 16px;
  font: 16px/24px $font-family-body;
}

.state {
  background-color: $color-ok;
  padding: 8px 16px;
}

.state p {
  position: relative;
  color: $color-ui-01;
}

.logo-container {
  background-color: $color-ui-01;
  padding: 8px;
  position: absolute;
  bottom: -24px;
  right: 12px;
  border-radius: 999px;
}
</style>
