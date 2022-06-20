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
          <div class="caption py-1">Registro</div>
          <v-icon large>mdi-account-outline</v-icon>
        </v-tab>
        <v-tab-item>
          <v-card class="px-4">
            <v-card-text>
              <v-form ref="registerForm" :v-model="true">
                <v-row>
                  <v-col cols="12">
                    <v-text-field
                      v-model="model.full_name"
                      label="Nombre completo"
                      :rules="nameRules"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field
                      v-model="model.user_name"
                      label="Nombre de usuario"
                      :rules="userNameRules"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field
                      v-model="model.phone_number"
                      type="text"
                      label="Número telefónico"
                      :rules="phoneRules"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field
                      v-model="model.email"
                      label="Correo electrónico"
                      :rules="emailRules"
                    ></v-text-field>
                  </v-col>
                  <!-- BIRTHDAY -->
                  <v-col cols="12">
                    <v-menu
                      ref="menu"
                      v-model="menu"
                      :close-on-content-click="false"
                      transition="scale-transition"
                      offset-y
                      min-width="auto"
                    >
                      <template v-slot:activator="{ on, attrs }">
                        <v-text-field
                          v-model="model.birthdate"
                          :rules="dateRules"
                          label="Fecha de nacimiento"
                          prepend-icon="mdi-calendar"
                          readonly
                          v-bind="attrs"
                          v-on="on"
                        ></v-text-field>
                      </template>
                      <v-date-picker
                        v-model="model.birthdate"
                        :active-picker.sync="activePicker"
                        :max="
                          new Date(
                            Date.now() - new Date().getTimezoneOffset() * 60000
                          )
                            .toISOString()
                            .substr(0, 10)
                        "
                        min="1950-01-01"
                        @change="saveBirthDate"
                      ></v-date-picker>
                    </v-menu>
                  </v-col>
                  <!-- END BIRTHDAY -->

                  <!-- SELECCION DE CATEGORIA -->
                  <v-col cols="12">
                    <v-select
                      v-model="model.categories"
                      :items="categories"
                      item-text="name"
                      item-value="id"
                      label="Categorias de interés"
                      attach
                      chips
                      multiple
                    ></v-select>
                  </v-col>
                  <!-- FIN SELECCION CATEGORIA -->

                  <v-col cols="12">
                    <v-text-field
                      v-model="model.password"
                      :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                      :type="showPassword ? 'text' : 'password'"
                      name="input-10-1"
                      label="Contraseña"
                      hint="At least 8 characters"
                      counter
                      @click:append="showPassword = !showPassword"
                      :rules="passwordRules"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field
                      block
                      v-model="confirmPassword"
                      :append-icon="
                        showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'
                      "
                      :type="showConfirmPassword ? 'text' : 'password'"
                      name="input-10-1"
                      label="Confirme la contraseña"
                      counter
                      @click:append="showConfirmPassword = !showConfirmPassword"
                      :rules="passwordRules"
                    ></v-text-field>
                  </v-col>
                  <v-col class="d-flex ml-auto">
                    <v-btn
                      x-large
                      block
                      color="success"
                      @click="register"
                      :loading="loading"
                      >Registrarme</v-btn
                    >
                  </v-col>
                </v-row>
              </v-form>
            </v-card-text>
          </v-card>
        </v-tab-item>
      </v-tabs>
    </div>
  </v-dialog>
</template>

<script>
import { postJSON, getJSON } from "@/helpers/Request.js";
import { notification } from "@/helpers/Notifications.js";

export default {
  name: "Register",
  computed: {
    passwordMatch() {
      return () =>
        this.password === this.verify || "Las contraseñas deben coincidir";
    },
  },
  mounted() {
    this.getCategories();
  },
  data() {
    return {
      dialog: true,
      loading: false,

      categories: [],

      model: {
        user_name: "",
        password: "",
        email: "",
        phone_number: "",
        birthdate: "",
        full_name: "",
        categories: [],
      },
      confirmPassword: "",
      showPassword: false,
      showConfirmPassword: false,

      activePicker: null,
      date: null,
      menu: false,

      nameRules: [(v) => !!v || "Debe ingresar su nombre completo"],
      userNameRules: [
        (v) => !!v || "Debe ingresar su nombre de usuario",
        (v) =>
          /^[a-z|A-Z]*$/.test(v) ||
          "Ingrese un nombre de usuario válido (solo letras)",
      ],
      emailRules: [
        (v) => !!v || "Debe ingresar su correo electrónico",
        (v) => /.+@.+\..+/.test(v) || "Ingrese un correo válido",
      ],
      phoneRules: [
        (v) => !!v || "Debe ingresar su número telefónico",
        (v) =>
          /^\+\d{12}$/.test(v) ||
          "Ingrese un número telefónico válido (+573214567890)",
      ],
      dateRules: [(v) => !!v || "Debe ingresar su fecha de nacimiento"],
      passwordRules: [
        (v) => !!v || "Debe ingresar la contraseña",
        (v) =>
          this.model.password === this.confirmPassword ||
          "Las contraseñas no coinciden",
        (v) => v.length >= 8 || "La contraseña debe tener almenos 8 caracter",
        (v) =>
          /\d+/.test(v) || "La contraseña debe contener al menos un número",
        (v) =>
          /[a-z]+/.test(v) ||
          "La contraseña debe contener al menos una letra minuscula",
        (v) =>
          /[A-Z]+/.test(v) ||
          "La contraseña debe contener al menos una letra mayuscula",
        (v) =>
          /[#$%&/()=]+/.test(v) ||
          "La contraseña debe contener al menos una caracter especial",
      ],
    };
  },
  watch: {
    menu(val) {
      val && setTimeout(() => (this.activePicker = "YEAR"));
    },
  },
  methods: {
    register() {
      if (!this.$refs.registerForm.validate()) {
        notification({
          message: "Verifique los datos ingresados",
        });

        return;
      }

      this.loading = true;
      postJSON("/users", this.model, false)
        .then((res) => {
          this.loading = false;

          notification({
            message: res.message,
          });

          if (!res.error) {
            this.$router.push({ path: "/confirm" });
          }
        })
        .catch(() => {
          this.loading = false;
          notification({
            message: "Ocurrió un error al hacer la petición",
          });
        });
    },
    saveBirthDate(date) {
      this.$refs.menu.save(date);
    },
    getCategories() {
      getJSON("/categories", this.params, false)
        .then((res) => {
          this.categories = res.data.items;
        })
        .catch((err) => {
          notification({
            message: "Error al obtener las categorias",
          });
        });
    },
  },
};
</script>
