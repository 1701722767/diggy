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
                <v-form ref="registerForm" :v-model="true" lazy-validation>
                  <v-row>
                    <!-- NOMBRE DEL EVENTO -->
                    <v-col cols="12">
                      <v-text-field
                        v-model="model.name"
                        label="Nombre del lugar"
                        maxlength="40"
                        :rules="[rules.required]"
                      ></v-text-field>
                    </v-col>
                    <!-- FIN NOMBRE EVENTO -->
                    <!-- DESCRIPCION EVENTO  -->
                    <v-col cols="12">
                      <v-textarea
                        :rules="[rules.required]"
                        label="Descripción del lugar"
                        v-model="model.description"
                      ></v-textarea>
                    </v-col>
                    <!-- FIN DESCRIPCION EVENTO -->
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
                          <h1>Seleccione la ubicación del lugar</h1>
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
                            <l-marker :lat-lng="markerLatLng"></l-marker>
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
                        >Crear lugar</v-btn
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
      <div></div>
    </v-dialog>
  </v-app>
</template>

<script>
import { LMap, LTileLayer, LMarker } from "vue2-leaflet";
import { Icon } from "leaflet";
import { postJSON } from "../../helpers/Request.js";
import { getJSON } from "../../helpers/Request.js";
import { notification } from "@/helpers/Notifications.js";

delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
});

export default {
  name: "PlaceRegister",
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
      postJSON("/places", this.model, true)
        .then((res) => {
          this.loading = false;
          notification({
            message: "Evento creado con éxito",
          });

          if (res.error) {
            notification({
              message: res.message,
              icon: "mdi-alert-circle",
            });
            return;
          }

          this.$router.push({ path: "/my-places" });
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
      if (this.showModal) {
        this.showModal = !this.showModal;
      }
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
  },
  data() {
    return {
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 16,
      center: [5.0569, -75.50356],
      markers: [L.latLng(5.0569, -75.50356)],
      dialog: true,
      tab: 0,
      tabs: [{ name: "Registro de lugar", icon: "mdi-map-marker" }],
      valid: true,
      model: {
        name: "",
        description: "",
        category_id: "",
        max: "",
        calificacion:0.0,
        coordinates: {},
      },
      categories: "",
      select: { category: "" },
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
