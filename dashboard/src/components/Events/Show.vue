<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" max-width="280px" >
      <v-card>
        <v-carousel hide-delimiters height="100">
          <v-carousel-item
            v-for="(item, i) in items"
            :key="i"
            :src="item.src"
          ></v-carousel-item>
        </v-carousel>

        <v-card-title>
          {{ this.model.name }}
        </v-card-title>

        <v-card-text>
          <v-row align="center" class="mx-0">
            <v-rating
              :value="Number(this.model.score)"
              color="amber"
              dense
              half-increments
              readonly
              size="14"
            ></v-rating>

            <div class="grey--text ms-4">
              {{ this.model.score }} ({{ this.model.total_comments }})
            </div>
          </v-row>

          <div class="my-4 text-subtitle-1">$ • {{ this.model.price }}</div>

          <div>{{ this.model.description }}</div>
        </v-card-text>

        <v-divider class="mx-4"></v-divider>

        <v-card-text>
          <div>
            <span style="font-weight: bold"> Inicia </span> :
            {{ formatDateAndTime(this.model.date_start) }}
          </div>
          <div>
            <span style="font-weight: bold"> Termina </span> :
            {{ formatDateAndTime(this.model.date_end) }}
          </div>
          <div>
            <span style="font-weight: bold"> Aforo Máximo </span> :
            {{ this.model.max }}
          </div>
          <div>
            <span style="font-weight: bold"> Cupos disponibles</span> :
            {{ this.model.slots }}
          </div>
          <div>
            <span style="font-weight: bold"> Rango de edad </span> :
            {{ this.model.range_age[0] }} - {{ this.model.range_age[1] }} años
          </div>
          <div>
            <span style="font-weight: bold"> Categoría </span> :
            {{ this.model.category_name }}
          </div>
        </v-card-text>

        <v-divider class="mx-4"></v-divider>

        <v-card-actions class="justify-center">
          <v-btn color="deep-purple lighten-2" text @click="reserve">
            Reservar
          </v-btn>
          <v-btn color="red lighten-2" text @click="hide"> Cerrar </v-btn>
        </v-card-actions>

        <v-row justify="center">
          <v-dialog v-model="commentDialog" width="300px">
            <template v-slot:activator="{ on, attrs }">
              <div class="my-2">
                <v-btn
                  rounded
                  outlined
                  large
                  v-bind="attrs"
                  v-on="on"
                  color="deep-purple lighten-2"
                  dark
                >
                  Ver comentarios
                </v-btn>
              </div>
            </template>
            <v-card scrollable="300px">
              <v-card-title>
                <span class="text-h5">Comentarios</span>
              </v-card-title>
              <v-col v-for="(comment, i) in this.model.comments" :key="i">
                <v-card-text>
                  <h4>{{ comment["full_name"] }}</h4>
                  {{ comment["comment"] }}
                  <v-rating
                    :value="Number(comment['score'])"
                    color="amber"
                    dense
                    half-increments
                    readonly
                    size="14"
                  ></v-rating>
                </v-card-text>
              </v-col>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  color="green darken-1"
                  text
                  @click="commentDialog = false"
                >
                  Salir
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-row>

        <v-row justify="center">
          <Comment
            ref="Comment"
            :composite_key="composite_key"
            route="/events/comments"
          ></Comment>
        </v-row>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { getJSON } from "@/helpers/Request";
import { formatDateAndTime } from "@/helpers/Date";
import { notification } from "@/helpers/Notifications";
import Comment from "@/components/Comment";


export default {
  components: {
    Comment
  },

  data: () => ({
    dialog: false,
    commentDialog: false,
    showModal: false,

    model: {
      event_id: "",
      category_name: "",
      name: "",
      description: "",
      date_end: "",
      date_start: "",
      max: "",
      name: "",
      price: "",
      range_age: "",
      slots: "",
      score: "",
      total_comments: "",
      comments: "",
    },
    composite_key: "",

    items: [
      {
        src: "https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg",
      },
      {
        src: "https://cdn.vuetifyjs.com/images/carousel/sky.jpg",
      },
      {
        src: "https://cdn.vuetifyjs.com/images/carousel/bird.jpg",
      },
      {
        src: "https://cdn.vuetifyjs.com/images/carousel/planet.jpg",
      },
    ],
  }),

  methods: {
    formatDateAndTime,
    show(params) {
      this.getItem(params);
      this.composite_key = params;
    },
    hide() {
      this.dialog = false;
    },
    reserve() {
      /// not implemented yet
    },
    openDialog() {
      if (this.showModal) {
        this.showModal = !this.showModal;
      }
    },

    getItem(params) {
      getJSON("/events/find", params, false)
        .then((res) => {
          if (res.error) {
            notification({
              message: res.message,
            });
          } else {
            this.model = res.data;
            this.dialog = true;
          }
        })
        .catch((err) => {
          notification({
            message: "Ocurrió un error al hacer la petición",
          });
        });
    },
  },
};
</script>

<style>
</style>