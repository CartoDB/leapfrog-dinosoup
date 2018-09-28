<template>
  <div id="app">
    <div v-if="showNewAppDialog" class="fullscreen">
      <AppDialog />
    </div>
    <Header />
    <MainContent />
  </div>
</template>

<script>
import Header from "./components/Header.vue";
import MainContent from "./components/MainContent.vue";
import AppDialog from "./components/AppDialog.vue";

export default {
  name: "app",

  components: {
    Header,
    MainContent,
    AppDialog
  },

  computed: {
    showNewAppDialog() {
      return this.$store.state.appDialogVisible;
    }
  },

  created() {
    this.$store.dispatch('initialLoad');
  }

};
</script>

<style lang="scss">
@import "./styles/_variables";
@import "./styles/_typography";
@import "./styles/_colors";
@import "./styles/_reset";
@import "./styles/text";
@import "./styles/buttons";

#app {
  font: $font-body;
  height: 100%;
}

body {
  background-color: $color-ui-02;
}

.fullscreen {
  position: fixed;
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
  z-index: 10;
}
</style>
