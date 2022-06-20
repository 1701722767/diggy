<template>
  <h3>{{ toCurrency(amount) }}</h3>
</template>

<script>
import { getJSON } from "../../helpers/Request";
import { toCurrency } from "../../helpers/Money";
export default {
  name: "Amount",
  data() {
    return {
      amount: 0,
    };
  },
  mounted() {
    this.getBalance();
  },
  methods: {
    toCurrency,
    getBalance() {
      getJSON("/users", null, true)
        .then((res) => {
          if (res.error) {
            notification({
              message: res.message,
            });

            return;
          }

          this.amount = res.data.amount;
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

<style scoped></style>
