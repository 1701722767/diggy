<template>
  <h3>{{ toCurrency(amount) }}</h3>
</template>

<script>
import { toCurrency } from "../../helpers/Money";
export default {
  name: "Amount",
  props: {
    amount: String,
  },
  methods: {
    toCurrency,
  },
};
</script>

<style scoped></style>
