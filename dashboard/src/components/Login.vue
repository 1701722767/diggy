<template>
  <v-dialog v-model="dialog" max-width="600px" min-width="360px">
    <v-snackbar v-model="showAlert" color="deep-purple accent-4">
      {{ alertMessage }}

      <template v-slot:action="{ attrs }">
        <v-btn color="grey" text v-bind="attrs" @click="showAlert = false">
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
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
          <div class="caption py-1">Iniciar sesión</div>
          <v-icon large>mdi-account</v-icon>
        </v-tab>
        <v-tab-item>
          <v-card class="px-4">
            <v-card-text>
              <v-form ref="loginForm" :v-model="true" lazy-validation>
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
                      v-model="model.password"
                      :append-icon="showPassword ? 'eye' : 'eye-off'"
                      :rules="[rules.required]"
                      :type="showPassword ? 'text' : 'password'"
                      name="input-10-1"
                      label="Contraseña"
                      counter
                      @click:append="showPassword = !showPassword"
                    ></v-text-field>
                  </v-col>
                  <v-col class="d-flex" cols="12" sm="6" xsm="12"> </v-col>

                  <v-row>
                    <br />
                    <v-col class="d-flex" align-left>
                      <v-btn x-large block color="primary" href="/register">
                        Registrarse
                      </v-btn>
                    </v-col>
                    <v-spacer></v-spacer>
                    <v-col class="d-flex" align-right>
                      <v-btn
                        x-large
                        block
                        color="success"
                        @click="doLoginRequest"
                      >
                        Login
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
import { postJSON } from "../helpers/Request";
export default {
  name: "Login",
  data: () => ({
    dialog: true,
    valid: true,

    model: {
      username: "",
      password: "",
    },

    showPassword: false,
    rules: {
      required: (value) => !!value || "Campo requerido",
      min: (v) => (v && v.length >= 8) || "Debe contener al menos 8 caracteres",
    },

    alertMessage: "",
    showAlert: false,
  }),
  methods: {
    doLoginRequest() {
      if (!this.$refs.loginForm.validate()) {
        this.alertMessage = "Debe ingresar todos los campos";
        this.showAlert = true;
        return;
      }

      postJSON("/log-in", this.model, false)
        .then((res) => {
          console.log(res);
        })
        .then((res) => {
          console.log(err);
        });
    },
  },
};
</script>
