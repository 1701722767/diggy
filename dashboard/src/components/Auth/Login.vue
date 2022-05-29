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
                      :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                      :type="showPassword ? 'text' : 'password'"
                      name="input-10-1"
                      label="Contraseña"
                      counter
                      @click:append="showPassword = !showPassword"
                      :rules="[rules.required]"
                    ></v-text-field>
                  </v-col>

                  <v-row>
                    <br />
                    <v-col class="d-flex" align-left>
                      <v-btn x-large block color="primary" @click="$router.push({ path: '/register' });">
                        Registrarse
                      </v-btn>
                    </v-col>
                    <v-col class="d-flex" align-right>
                      <v-btn
                        x-large
                        block
                        color="success"
                        @click="doLoginRequest"
                        :loading="loading"
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
import { logIn } from "@/services/Auth.js";
import Emitter from "@/services/Emitter.js";
import { notification } from "@/helpers/Notifications.js";

export default {
  name: "Login",
  data: () => ({
    dialog: true,
    loading: false,
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
  }),
  methods: {
    doLoginRequest() {
      if (!this.$refs.loginForm.validate()) {
        notification({
          message: "Debe ingresar todos los campos",
        });
        return;
      }

      this.loading = true;

      logIn(this.model.username, this.model.password)
        .then((res) => {
          notification({
            icon: "mdi-account",
            message: `Bienvenido ${res.attributes.name}`,
          });

          Emitter.emit("reload-navbar-items");
          setTimeout(() => {
            this.$router.push({ path: "/directory/map" });
          }, 2000);
        })
        .catch((err) => {
          this.loading = false;
          if (err.code == "NotAuthorizedException") {
            notification({
              message: "Credenciales incorrectas",
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
