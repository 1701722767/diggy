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
                    <v-col class="d-flex ml-auto" cols="15" sm="5" xsm="25">
                      <v-btn
                        x-large
                        block
                        color="secondary"
                        @click="showModal=true"> Inserte dirección                 
                      </v-btn>
                      <transition name="fade" appear>
                        <div class="modal-overlay" v-if="showModal" @click="showModal=false"></div>
                      </transition>  
                      <transition name="slide" appear>
                        <div class="modal" v-if="showModal">
                            <h1>Seleccione la ubicación del evento</h1>
                            <l-map style="height: 250px" :zoom="zoom" :center="center">
                              <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
                              <l-marker :lat-lng="markerLatLng"></l-marker>
                            </l-map>
                        </div>
                      </transition> 
                    </v-col>
                    <v-spacer></v-spacer>
                    <v-col>
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
  components:{
    LMap,
    LTileLayer,
    LMarker,
  },
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
    openDialog() {
      if (this.showModal) {
        this.showModal=!this.showModal
      }
    },
  },
  data(){
    return {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
          '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 16,
      center: [5.05690, -75.50356],
      markerLatLng:[5.05690, -75.50356],
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
      showModal:false,
      rules: {
        required: (value) => !!value || "Campo requerido",
        min: (v) => (v && v.length >= 8) || "Debe contener al menos 8 caracteres",
      }
    };
  }
};
</script>

<style>
  * {
 margin: 0;
 padding: 0;
 box-sizing: border-box;
}

body {
 font-family: 'montserrat', sans-serif;
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
 background-color: #FFF;
 border-radius: 16px;
 
 padding: 25px;
}

.fade-enter-active,
.fade-leave-active {
 transition: opacity .5s;
}

.fade-enter,
.fade-leave-to {
 opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
 transition: transform .5s;
}

.slide-enter,
.slide-leave-to {
 transform: translateY(-50%) translateX(100vw);
}
</style>
