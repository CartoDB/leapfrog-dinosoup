<template>
  <div class="application-card" v-on:click="handleClick">
    <div class="message">
      <p class="plus-sign">+</p>
      <p>Add a new LI APP</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "add-app-card",

  components: {},

  props: {
    app: Object
  },

  computed: {},

  methods: {
    handleClick() {
      this.$store.commit("openDialog");
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
  align-items: center;
  justify-content: center;
  background-color: $color-ui-01;
  cursor: pointer;
}

.message {
  text-align: center;
  color: $color-ok;

  p {
    font-size: 64px;
    font-weight: bold;
    font: $font-title;
  }

  p.plus-sign {
    font: 128px/128px $font-family-display;
    color: $color-ok;
  }
}
</style>
