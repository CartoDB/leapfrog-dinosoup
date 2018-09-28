<template>
  <div class="application-list">
    <svg class="apps-icon">xmlns="http://www.w3.org/2000/svg" width="24" height="24"><path d="M 0 0 L 24 0 L 24 24.001 L 0 24.001 Z" fill="transparent"></path><path d="M 20.555 17.832 C 20.833 17.646 21 17.334 21 17 L 21 3 C 21.001 2.631 20.799 2.291 20.473 2.117 C 20.148 1.943 19.753 1.962 19.446 2.168 L 14.054 5.763 L 9.625 2.219 C 9.454 2.092 9.248 2.018 9.035 2.008 C 8.827 2.002 8.622 2.058 8.445 2.168 L 2.445 6.168 C 2.167 6.354 2 6.666 2 7 L 2 21 C 2 21.369 2.203 21.708 2.528 21.882 C 2.853 22.056 3.248 22.037 3.555 21.832 L 8.947 18.238 L 13.376 21.781 C 13.556 21.926 13.777 22 14 22 C 14.198 22.007 14.392 21.944 14.549 21.824 Z M 4 7.535 L 8 4.869 L 8 16.465 L 4 19.132 Z M 13 18.92 L 10 16.52 L 10 5.082 L 13 7.481 Z M 19 16.465 L 15 19.132 L 15 7.535 L 19 4.869 Z" fill="#2E3C43"></path></svg>
    <h2 class="text-title text-bold">Your applications</h2>
    <ul class="cards">
      <li>
        <AddAppCard />
      </li>
      <li v-for="app in apps" :key="app.name">
        <ApplicationCard v-bind:app="app"/>
      </li>
    </ul>
  </div>
</template>

<script>
import ApplicationCard from "./ApplicationCard.vue";
import AddAppCard from "./AddAppCard.vue";

export default {
  name: "application-list",

  components: {
    ApplicationCard,
    AddAppCard
  },

  computed: {
    apps() {
      return this.$store.state.apps;
    }
  }
};
</script>

<style scoped lang="scss">
h2 {
  display: inline;
}

.cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  align-self: stretch;
  list-style: none;
  margin: 24px 0 0 0;
  padding: 0;
}

.cards > li {
  width: 30%;
  margin: 0 24px 24px 0;
}

.application-list {
  position: relative;
}

.apps-icon {
  position: absolute;
  top: 4px;
  left: -32px;
  width: 24px;
  height: 24px;
}
</style>
