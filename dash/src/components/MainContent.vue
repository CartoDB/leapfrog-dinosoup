<template>
  <main class="main-content">
    <ApplicationList />

  </main>
</template>

<script>
import ApplicationList from "./ApplicationList.vue";

export default {
  name: "main-content",
  components: {
    ApplicationList
  }
};
</script>

<style scoped lang="scss">
@import "../styles/_variables";
@import "../styles/_colors";

.main-content {
  margin: 48px auto 0 auto;
  padding: 0 48px;
  max-width: 240 * $su;
  width: auto;

  min-height: 64px;
  height: 100%;
}
</style>
