<template>
  <div class="content">
    <h2>Mi balance</h2>
    <amount />
    <br><br>
    <transactions />
  </div>
</template>

<script>
import Amount from '../components/Balance/Amount.vue';
import Transactions from '../components/Balance/Transactions.vue';
export default {
  name: "MyBalance",
  components: { Amount, Transactions },
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
