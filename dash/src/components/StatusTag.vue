<template>
  <div v-bind:class="classObject">
    {{ status }}
  </div>

</template>

<script>
export default {
  props: {
    status: String
  },

  computed: {
    classObject: function () {
      let classes = {};
      classes[this.status] = true;
      return classes;
    }
  }
};
</script>

<style scoped lang="scss">

.pending {
  color: blue;
}

.checking {
  color: orange;
}

.compiling {
  color: brown;
}

.building_image {
  color: pink;
}

.executing {
  color: red;
}

.configuring_nginx {
  color: olive;
}

.success {
  color: green;
}

.failed {
  color: red;
}

</style>