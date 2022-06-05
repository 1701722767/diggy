<template>
  <div class="content">
    <h2>Mis eventos</h2>
    <list />
    <register ref="addEvent" />
    <v-btn
      class="btn-add"
      fab
      color="deep-purple accent-4"
      bottom
      right
      absolute
      @click="openAddModal"
    >
      <v-icon>mdi-plus</v-icon>
    </v-btn>
  </div>
</template>

<script>
import List from "../components/Events/List.vue";
import Register from "../components/Events/Register.vue";
export default {
  components: { Register, List },
  name: "MyEvents",
  methods: {
    openAddModal() {
      this.$refs.addEvent.openDialog();
    },
  },
};
</script>

<style lang="scss" scoped>
.content {
  height: 100vh;
  padding: 10px;
}

.btn-add {
  bottom: 10px !important;
}

.mdi-plus {
  color: white !important;
}

.container {
  overflow: auto;
  height: 80vh;
}
</style>
