<template>
  <div>
    <h4>Transacciones</h4>
    <div class="paginator">
      <v-btn
        @click="beforePage()"
        small
        dark
        color="deep-purple accent-4"
        :disabled="page <= 0"
      >
        <v-icon small> mdi-arrow-left </v-icon>
      </v-btn>
      <v-btn
        @click="nextPage()"
        small
        dark
        :disabled="nextStartkey == '' && page == maxPage - 1"
        class="mx-2"
        color="deep-purple accent-4 "
      >
        <v-icon small> mdi-arrow-right </v-icon>
      </v-btn>
    </div>
    <v-simple-table>
      <template v-slot:default>
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Referencia</th>
            <th>Descripción</th>
            <th>Valor</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="transaction in transactions.slice(page * registerPerPage, page + registerPerPage)"
            :key="transaction.reference_id"
          >
            <td>{{ transaction.date }}</td>
            <td>{{ transaction.reference_id }}</td>
            <td>{{ transaction.description }}</td>
            <td>{{ toCurrency(transaction.amount) }}</td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
  </div>
</template>

<script>
import { toCurrency } from "../../helpers/Money";
import { getJSON } from "../../helpers/Request";

export default {
  name: "Transactions",
  data() {
    return {
      transactions: [],
      nextStartkey: "",
      registerPerPage: 15,
      page: 0,
      maxPage: 1,
    };
  },
  mounted() {
    this.getTransactions("");
  },
  methods: {
    toCurrency,
    getTransactions(startKey) {
      getJSON(
        "/payments/list-transactions",
        {
          start_key: startKey,
        },
        true
      )
        .then((res) => {
          if (res.error) {
            notification({
              message: res.message,
            });

            return;
          }

          this.transactions.push(...res.data.items);
          if (res.data.start_key != undefined) {
            this.nextStartkey = res.data.start_key;
            this.maxPage++;

            return;
          }

          this.nextStartkey = "";
        })
        .catch(() => {
          notification({
            message: "Ocurrió un error al obtener el saldo",
          });
        });
    },
    beforePage() {
      if (this.page > 0) {
        this.page--;
      }
    },
    nextPage() {
      this.page++;
      if (this.page == this.maxPage - 1 && this.nextStartkey != "") {
        this.getTransactions(this.nextStartkey);
      }
    },
  },
};
</script>

<style scoped>
.paginator {
  text-align: end;
}
</style>
