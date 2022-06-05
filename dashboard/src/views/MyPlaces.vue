<template>
  <div class="content">
    <h2>Mis lugares</h2>
    <list />
    <register ref="addPlaceModal" />

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
import List from "../components/Places/List.vue";
import Register from "../components/Places/Register.vue";
export default {
  name: "MyPlaces",
  components: { Register, List },
  methods: {
    openAddModal() {
      this.$refs.addPlaceModal.openDialog();
    }
  },
};
</script>

<style scoped>
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
