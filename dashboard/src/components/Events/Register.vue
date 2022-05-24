<template>
  <v-app>
    <v-dialog v-model="dialog" persistent max-width="1000px" min-width="360px">
      <div>
        <v-tabs
          v-model="tab"
          show-arrows
          background-color="deep-purple accent-4"
          icons-and-text
          dark
          grow
        >
          <v-tabs-slider color="purple darken-4"></v-tabs-slider>
          <v-tab v-for="i in tabs" :key="i">
            <v-icon large>{{ i.icon }}</v-icon>
            <div class="caption py-1">{{ i.name }}</div>
          </v-tab>
          <v-tab-item>
            <v-card class="px-4">
              <v-card-text>
                <v-form ref="registerForm" v-model="valid" lazy-validation>
                  <v-row>
                    <v-col cols="12">
                      <v-text-field
                        v-model="nombre"
                        label="Nombre del evento"
                        maxlength="40"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        v-model="descripcion"
                        :rules="[rules.required]"
                        label="Descripción del evento"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="6">
                      <v-select
                        v-model="select"
                        :hint="`${select.category}`"
                        :items="items"
                        item-text="category"
                        item-value="category"
                        label="Seleccione categoría"
                        persistent-hint
                        return-object
                        single-line
                      ></v-select>
                    </v-col>
                    <v-col cols="12" sm="6" md="6">
                      <v-text-field
                        v-model="valor"
                        type="number"
                        label="Valor de ingreso"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="6">
                      <v-menu
                        ref="menu"
                        v-model="menu"
                        :rules="[rules.required]"
                        :close-on-content-click="false"
                        transition="scale-transition"
                        offset-y
                        min-width="auto"
                      >
                        <template v-slot:activator="{ on, attrs }">
                          <v-text-field
                            v-model="date"
                            label="Fecha del evento"
                            prepend-icon="mdi-calendar"
                            readonly
                            v-bind="attrs"
                            v-on="on"
                          ></v-text-field>
                        </template>
                        <v-date-picker
                          v-model="date"
                          :active-picker.sync="activePicker"
                          :min="
                            new Date(
                              Date.now() -
                                new Date().getTimezoneOffset() * 60000
                            )
                              .toISOString()
                              .substr(0, 10)
                          "
                          max="2024-03-20"
                          @change="save"
                        ></v-date-picker>
                      </v-menu>
                    </v-col>
                    <v-col cols="12" sm="6" md="6">
                      <v-text-field
                        v-model="aforo"
                        :rules="[rules.required]"
                        type="number"
                        label="Aforo máximo"
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="6">
                      <v-file-input
                        v-model="imagen"
                        :rules="rules"
                        accept="image/png, image/jpeg, image/bmp"
                        placeholder="Pick an avatar"
                        prepend-icon="mdi-camera"
                        label="Inserte imagen del evento"
                      ></v-file-input>
                    </v-col>
                    <v-button> </v-button>
                    <v-col> </v-col>
                    <v-spacer></v-spacer>
                    <v-col class="d-flex ml-auto" cols="15" sm="5" xsm="20">
                      <v-btn
                        x-large
                        block
                        :disabled="!valid"
                        color="success"
                        @click="validate"
                        >Crear evento</v-btn
                      >
                    </v-col>
                  </v-row>
                </v-form>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs>
      </div>
      <div></div>
    </v-dialog>
  </v-app>
</template>

<script>
import { LMap, LTileLayer, LMarker } from "vue2-leaflet";

export default {
  name: "EventRegister",
  methods: {
    validate() {
      if (this.$refs.loginForm.validate()) {
        // submit form to server/API here...
      }
    },
    reset() {
      this.$refs.form.reset();
    },
    resetValidation() {
      this.$refs.form.resetValidation();
    },
    save(date) {
      this.$refs.menu.save(date);
    },
  },
  data: () => ({
    menu: false,
    dialog: true,
    tab: 0,
    tabs: [{ name: "Registro de evento", icon: "mdi-calendar-edit" }],
    valid: true,

    nombre: "",
    descripcion: "",
    valor: "",
    imagen: null,
    fecha_nacimiento: null,
    aforo: "",
    select: { category: "" },
    items: [
      { category: "Fiesta" },
      { category: "Deporte" },
      { category: "Cultura" },
      { category: "Musica" },
      { category: "Educacion" },
    ],

    show1: false,
    rules: {
      required: (value) => !!value || "Campo requerido",
      min: (v) => (v && v.length >= 8) || "Debe contener al menos 8 caracteres",
    },
  }),
};
</script>

<style></style>
