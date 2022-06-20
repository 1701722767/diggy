<template>
  <div class="content">
    <recharge :user="user" ref="rechargeModal" />
    <h2>Mi balance</h2>
    <amount :amount="user.amount" />
    <br /><br />
    <transactions />
    <v-btn
      class="btn-add"
      fab
      color="deep-purple accent-4"
      bottom
      right
      dark
      absolute
      @click="openRechargeModal"
    >
      <v-icon>mdi-plus</v-icon>
    </v-btn>
  </div>
</template>

<script>
import Amount from "../components/Balance/Amount.vue";
import Recharge from "../components/Balance/Recharge.vue";
import Transactions from "../components/Balance/Transactions.vue";
import { getJSON } from "../helpers/Request";

export default {
  name: "MyBalance",
  components: { Amount, Transactions, Recharge },
  mounted() {
    this.getUser();
  },
  data() {
    return {
      user: {},
    };
  },
  methods: {
    openRechargeModal() {
      this.$refs.rechargeModal.openDialog();
    },
    getUser() {
      getJSON("/users", null, true)
        .then((res) => {
          if (res.error) {
            notification({
              message: res.message,
            });

            return;
          }

          this.user = res.data;
        })
        .catch(() => {
          notification({
            message: "Ocurrió un error al obtener el saldo",
          });
        });
    },
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
