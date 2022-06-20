<template>
  <v-card-action class="justify-end">
    <v-btn color="primary" text @click="showModal = true">Comentar</v-btn>
    <transition name="fade" appear>
      <div
        class="modal-overlay"
        v-if="showModal"
        @click="showModal = false"
      ></div>
    </transition> 
    <transition name="slide" appear>
      <div ref="commentForm" slot="" class="modal" v-if="showModal">
        <v-col>
          <h3>Realice el comentario</h3>
          <v-textarea
            v-model="postModel.comment"
            append-icon="mdi-comment"
            class="mx-2"
            label="Comentario"
            rows="1"
          ></v-textarea>
          <v-rating
            :value="5.0"
            color="amber"
            v-model="postModel.score"
            dense
            half-increments
            size="23"
          ></v-rating>
          <br />
          <v-card-actions>
            <v-btn color="red" text @click="showModal = false"> Salir </v-btn>
            <v-btn color="primary" text @click="register"> Guardar </v-btn>
          </v-card-actions>
        </v-col>
      </div>
    </transition>
  </v-card-action>
</template>

<script>

import Map from "../components/Directory/Map";
import { postJSON } from "../helpers/Request.js";
import { notification } from "@/helpers/Notifications";

export default {

  components:{
    Map
  },
  props:{
    composite_key: String,
    route: String
  },
  data: () => ({

    showModal: false,
    postModel: {
      comment: "",
      score: 5.0,
    },
    parametros:""
  }),
  methods: {
    register() {
      this.loading = true;
      postJSON(this.route, this.postModel, true, this.composite_key)
        .then((res) => {
          this.loading = false;
          if (res.error) {
            notification({
              message: res.message,
              icon: "mdi-alert-circle",
            });
            return;
          }
          notification({
            message: "Comentario guardado con éxito",
          });
          this.postModel.comment="";
          this.postModel.score=5.0;

          this.showModal = false;
        })
        .catch((err) => {
          this.loading = false;
          notification({
            message: "Ocurrió un error al hacer la petición",
          });
        });
    },


  },
};
</script>