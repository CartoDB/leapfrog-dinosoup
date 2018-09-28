<template>
  <div class="logo">
    <img class="logo-img" v-if="tech === 'python'" src="../assets/python-logo.svg" />
    <img class="logo-img" v-if="tech === 'js'" src="../assets/js-logo.svg" />
  </div>
</template>


<script>
export default {
  name: "stack-logo",

  props: {
    tech: String
  }
};
</script>

<style scoped lang="scss">
.logo {
  width: 32px;
  height: 32px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.logo-img {
  height: 100%;
}
</style>
