<template>
  <v-dialog v-model="dialog" max-width="500px" min-width="360px">
    <v-tabs
      show-arrows
      background-color="deep-purple accent-4"
      icons-and-text
      dark
      grow
    >
      <v-tabs-slider color="purple darken-4"></v-tabs-slider>
      <v-tab>
        <div class="caption py-1">Recargar</div>
      </v-tab>
      <v-tab-item>
        <v-container>
          <form
            ref="rechargeForm"
            @submit.prevent="rechargeValidate()"
            method="POST"
            action="https://sandbox.checkout.payulatam.com/ppp-web-gateway-payu/"
          >
            <input name="merchantId" type="hidden" value="508029" />
            <input name="accountId" type="hidden" value="512321" />
            <input name="description" type="hidden" value="Compra por Payu" />
            <input
              name="referenceCode"
              type="hidden"
              :value="`${user.id}#${user.user_name}#${reference_id}`"
            />
            <input name="tax" type="hidden" value="0" />
            <!-- <input name="taxReturnBase" type="hidden" value="16806" /> -->
            <input name="currency" type="hidden" value="COP" />
            <input
              name="signature"
              type="hidden"
              :value="
                md5(
                  `4Vj8eK4rloUd272L48hsrarnUA~508029~${user.id}#${user.user_name}#${reference_id}~${amount}~COP`
                )
              "
            />
            <input name="test" type="hidden" value="0" />
            <input name="buyerEmail" type="hidden" :value="user.email" />
            <input
              name="responseUrl"
              type="hidden"
              :value="`${APP_HOST}/my-balance`"
            />
            <input
              name="confirmationUrl"
              type="hidden"
              :value="`${API_URL}/payments/webhook`"
            />
            <v-row>
              <v-col cols="24">
                <v-text-field
                  name="amount"
                  v-model="amount"
                  :rules="amountRules"
                  label="Valor"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
            <v-col cols="24" align="center">
              <v-btn dark color="deep-purple accent-4" type="submit">Recargar</v-btn>
              <v-btn @click="dialog = false">Cancelar</v-btn>
            </v-col>
          </form>
        </v-container>
      </v-tab-item>
    </v-tabs>
  </v-dialog>
</template>

<script>
import { notification } from "@/helpers/Notifications.js";
import { APP_HOST,API_URL } from "@/config/Constants.js"
import md5 from "md5";

export default {
  props: {
    user: Object,
  },
  data: () => ({
    APP_HOST,
    API_URL,
    valid: false,
    amount: "",
    lastname: "",
    amountRules: [
      (v) => !!v || "Ingrese un valor valido a recargar",
      (v) => v > 1000 || "Solo se puede recargar un valor mayor a 1000",
    ],
    dialog: false,
    reference_id: Date.now(),
  }),
  methods: {
    md5,
    openDialog() {
      this.dialog = true;
    },
    rechargeValidate() {
      if (this.amount == "" || this.amount < 1000) {
        notification({
          message: "Ingrese un valor valido a recargar.",
        });
        return;
      }

      this.$refs.rechargeForm.submit();
    },
  },
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: "montserrat", sans-serif;
}

#app {
  position: relative;

  display: flex;
  justify-content: center;
  align-items: center;

  width: 100vw;
  min-height: 100vh;
  overflow-x: hidden;
}

.button {
  transition: 0.4s ease-out;
}

.modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 98;
  background-color: rgba(0, 0, 0, 0.3);
}

.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 99;

  width: 100%;
  max-width: 600px;
  background-color: #fff;
  border-radius: 16px;

  padding: 25px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.5s;
}

.slide-enter,
.slide-leave-to {
  transform: translateY(-50%) translateX(100vw);
}
</style>
