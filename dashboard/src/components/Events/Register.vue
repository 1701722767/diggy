<template>
    <v-dialog v-model="dialog" max-width="1000px" min-width="360px">
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
          <v-tab v-for="i in tabs" :key="i.name">
            <v-icon large>{{ i.icon }}</v-icon>
            <div class="caption py-1">{{ i.name }}</div>
          </v-tab>
          <v-tab-item>
            <v-card class="px-4">
              <v-card-text>
                <v-form ref="registerForm" :v-model="true" lazy-validation>
                  <v-row>
                    <!-- NOMBRE DEL EVENTO -->
                    <v-col cols="12">
                      <v-text-field
                        v-model="model.name"
                        label="Nombre del evento"
                        maxlength="40"
                        required
                      ></v-text-field>
                    </v-col>
                    <!-- FIN NOMBRE EVENTO -->
                    <!-- DESCRIPCION EVENTO  -->
                    <v-col cols="12">
                      <v-textarea
                        :rules="[rules.required]"
                        label="Descripción del evento"
                        v-model="model.description"
                      ></v-textarea>
                    </v-col>
                    <!-- FIN DESCRIPCION EVENTO -->
                    <!--RANGO EDAD-->
                    <v-col cols="12">
                      <h3>Seleccione el rango de edad:</h3>
                      <v-range-slider
                        color="purple darken-4"

                        :tick-labels="edades"
                        v-model="model.range_age"
                        min="0"
                        max="80"
                        step="10"
                        ticks="always"
                        tick-size="1"
                        >
                        <template v-slot:thumb-label="props">
                          <v-icon dark>
                            {{ season(props.value) }}
                          </v-icon>
                        </template>
                      </v-range-slider>
                    </v-col>
                    <!--FIN RANGO EDAD-->
                    <!--FECHA DE INICIO-->
                    <v-col cols="12" sm="6" md="6">
                      <v-datetime-picker
                        v-model="picker_start"
                        color="purple darken-4"
                        label="Fecha y hora de inicio"
                        max="2024-03-20"
                        >
                        <template slot="dateIcon">
                            <v-icon>mdi-calendar</v-icon>
                            </template>
                            <template slot="timeIcon">
                              <v-icon>mdi-clock</v-icon>
                        </template>
                      </v-datetime-picker>
                    </v-col>
                    <!--FIN FECHA DE INICIO-->
                    <!--FECHA DE FIN-->
                    <v-col cols="12" sm="6" md="6">
                      <v-datetime-picker
                            color="purple darken-4"
                            label="Fecha y hora de fin"
                            v-model="picker_end"
                            max="2024-03-20"
                            >
                            <template slot="dateIcon">
                              <v-icon>mdi-calendar</v-icon>
                            </template>
                            <template slot="timeIcon">
                              <v-icon>mdi-clock</v-icon>
                            </template>
                      </v-datetime-picker>
                    </v-col>
                    <!--FIN FECHA DE FIN-->
                    <!-- SELECCION DE CATEGORIA -->
                    <v-col cols="12" sm="6" md="6">
                      <v-select
                        v-model="model.category_id"
                        :items="categories"
                        item-text="name"
                        item-value="id"
                        label="Seleccione categoría"
                        persistent-hint
                        single-line
                      ></v-select>
                    </v-col>
                    <!-- FIN SELECCION CATEGORIA -->
                    <!-- VALOR DE INGRESO -->
                    <v-col cols="12" sm="6" md="6">
                      <v-text-field
                        v-model="model.price"
                        type="number"
                        label="Valor de ingreso"
                        required
                      ></v-text-field>
                    </v-col>
                    <!-- FIN VALOR DE INGRESO -->
                    <!-- AFORO -->
                    <v-col cols="12" sm="6" md="6">
                      <v-text-field
                        v-model="model.max"
                        :rules="[rules.required]"
                        type="number"
                        label="Aforo máximo"
                        required
                      ></v-text-field>
                    </v-col>
                     <v-col cols="12" sm="6" md="6">
                      <v-text-field
                        v-model="model.slots"
                        :rules="[rules.required]"
                        type="number"
                        label="Espacios disponible"
                        required

                      ></v-text-field>
                    </v-col>
                    <!-- FIN AFORO -->
                    <!-- IMAGEN -->
                    <!--
                    <v-col cols="12" sm="6" md="6">
                      <v-file-input
                        v-model="model.imagen"
                        :rules="rules"
                        accept="image/png, image/jpeg, image/bmp"
                        placeholder="Pick an avatar"
                        prepend-icon="mdi-camera"
                        label="Inserte imagen del evento"
                      ></v-file-input>
                    </v-col>-->
                  <!-- FIN IMAGEN -->
                  <!-- COORDENADAS -->
                  <v-col class="d-flex ml-auto" cols="15" sm="5" xsm="25">
                    <v-btn
                      x-large
                      block
                      color="secondary"
                      @click="showModal = true"
                    >
                      Inserte dirección
                    </v-btn>
                    <transition name="fade" appear>
                      <div
                        class="modal-overlay"
                        v-if="showModal"
                        @click="showModal = false"
                      ></div>
                    </transition>
                    <transition name="slide" appear>
                      <div class="modal" v-if="showModal">
                        <h1>Seleccione la ubicación del evento</h1>
                        <br />
                        <l-map
                          style="height: 250px"
                          :zoom="zoom"
                          :center="center"
                          @click="addMarker($event)"
                        >
                          <l-tile-layer
                            :url="url"
                            :attribution="attribution"
                          ></l-tile-layer>
                        </l-map>
                        <v-col>
                          <h1>Coordenadas seleccionadas:</h1>
                          <h3>{{ model.coordinates }}</h3>
                          <br />
                          <v-btn
                            x-large
                            block
                            :disabled="!valid"
                            color="success"
                            @click="showModal = false"
                            >Guardar dirección</v-btn
                          >
                        </v-col>
                      </div>
                    </transition>
                  </v-col>
                  <v-spacer></v-spacer>
                  <v-col cols="12" sm="6" md="6">
                    <v-btn
                      x-large
                      block
                      :disabled="!valid"
                      color="success"
                      @click="register"
                      :loading="loading"
                      >Crear evento</v-btn
                    >
                  </v-col>
                  <!-- FIN COORDENADA -->
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
import { LMap, LTileLayer, LMarker } from "vue2-leaflet";
import { postJSON, getJSON } from "@/helpers/Request.js";
import { notification } from "@/helpers/Notifications.js";
import { transformDate } from "@/helpers/Date.js";

export default {
  name: "EventRegister",
  components: {
    LMap,
    LTileLayer,
    LMarker,
  },
  mounted() {
    this.getCategories();
  },
  methods: {
    register() {
      if (!this.$refs.registerForm.validate()) {
        notification({
          message: "Complete todos los campos.",
        });
        return;
      }

      this.loading = true;

      this.model.date_start = transformDate(this.picker_start);
      this.model.date_end = transformDate(this.picker_end);
    

      postJSON("/events", this.model, true)
        .then((res) => {
          this.loading = false;

          if (res.error) {
            notification({
              message: res.message,
              icon: "mdi-alert-circle",
            });
            return;
          }

          if (!res.error) {
            notification({
            message: "Evento creado con éxito",
          });
            this.closeDialog();
          }

          
        })
        .catch((err) => {
          this.loading = false;
          notification({
            message: "Ocurrió un error al hacer la petición",
          });
        });
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
    reset() {
      this.$refs.form.reset();
    },
    resetValidation() {
      this.$refs.form.resetValidation();
    },
    openDialog() {
      this.dialog = true;
    },
    closeDialog(){
      this.dialog=false;
    },
    addMarker(event) {
      let latitude = event.latlng.lat;
      let longitude = event.latlng.lng;
      this.model.coordinates = {
        latitude,
        longitude,
      };
    },
    season(val) {
      return this.icons[val];
    },
    setSlot(aforo) {
      return (this.slots = this.max);
    },
  },
  data() {
    return {
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 16,
      center: [5.0569, -75.50356],
      markers: [L.latLng(5.0569, -75.50356)],
      dialog: false,
      loading: false,
      tab: 0,
      tabs: [{ name: "Registro de evento", icon: "mdi-calendar-edit" }],
      valid: true,
      model: {
        name: "",
        description: "",
        price: "",
        slots: "",
        max: "",
        range_age: [0, 1],
        //images: null,
        date_start: "",
        date_end: "",
        category_id:"",
        coordinates:{}
      },
      tpdate_start:"",
      tpdate_end:"",
      categories: "",
      select: { category: "" },
      edades: ["0", "10", "20", "30", "40", "50", "60", "70", "80"],
      icons: [
        "mdi-teddy-bear",
        "mdi-football",
        "mdi-football",
        "mdi-football",
        "mdi-football",
        "mdi-human-male",
        "mdi-human-male",
        "mdi-human-male",
        "mdi-human-male",
      ],
      show1: false,
      showModal: false,
      rules: {
        required: (value) => !!value || "Campo requerido",
      },
    };
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
