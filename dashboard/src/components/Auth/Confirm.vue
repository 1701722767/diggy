<template>
  <v-dialog v-model="dialog" max-width="600px" min-width="360px">
    <div>
      <v-tabs
        show-arrows
        background-color="deep-purple accent-4"
        icons-and-text
        dark
        grow
      >
        <v-tabs-slider color="purple darken-4"></v-tabs-slider>
        <v-tab>
          <div class="caption py-1">Confirmar Registro</div>
          <v-icon large>mdi-account</v-icon>
        </v-tab>
        <v-tab-item>
          <v-card class="px-4">
            <v-card-text>
              <v-form ref="confirmForm" :v-model="true" lazy-validation>
                <v-row>
                  <v-col cols="12">
                    <v-text-field
                      v-model="model.username"
                      label="Nombre de usuario"
                      :rules="[rules.required]"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field
                      v-model="model.code"
                      :append-icon="showCode ? 'mdi-eye' : 'mdi-eye-off'"
                      :type="showCode ? 'text' : 'password'"
                      name="input-10-1"
                      label="Código de verificación"
                      counter
                      @click:append="showCode = !showCode"
                      :rules="[rules.required,rules.min]"
                    ></v-text-field>
                  </v-col>

                  <v-row>
                    <v-col class="d-flex" align-right>
                      <v-btn
                        x-large
                        block
                        color="success"
                        @click="doLoginRequest"
                        :loading="loading"
                      >
                        Confirmar registro
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-row>
                <br />
              </v-form>
            </v-card-text>
          </v-card>
        </v-tab-item>
      </v-tabs>
    </div>
  </v-dialog>
</template>

<script>
import { confirm } from "@/services/Auth.js";
import { notification } from "@/helpers/Notifications.js";

export default {
  name: "Confirm",
  data: () => ({
    dialog: true,
    loading: false,
    valid: true,

    model: {
      username: "",
      code: "",
    },

    showCode: false,
    rules: {
      required: (value) => !!value || "Campo requerido",
      min: (v) => (v && v.length == 6) || "Debe ingresar 6 caracteres",
    },
  }),
  methods: {
    doLoginRequest() {
      if (!this.$refs.confirmForm.validate()) {
        notification({
          message: "Debe ingresar todos los campos",
        });
        return;
      }

      this.loading = true;

      confirm(this.model.username, this.model.code)
        .then((res) => {
          this.loading = false;
          if (res == "SUCCESS") {
            notification({
              message: `Registro confirmado con exito`,
            });

            this.$router.push({ path: "/login" });
            return;
          }

          notification({
            message: `No se logro confirmar el registro`,
          });
        })
        .catch((err) => {
          this.loading = false;
          if (err.code == "ExpiredCodeException") {
            notification({
              message: "El código de verificación ha expirado",
            });
            return;
          }

          notification({
            message: "Ocurrió un error al hacer la petición",
          });
        });
    },
  },
};
</script>
