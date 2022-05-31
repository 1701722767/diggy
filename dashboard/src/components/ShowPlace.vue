<template>
  <v-row justify="center">
    <v-dialog
      v-model="dialog"
      max-width="300px"
    >
      <v-card>
        <v-carousel hide-delimiters height=100 >
            <v-carousel-item
            v-for="(item,i) in items"
            :key="i"
            :src="item.src"
            ></v-carousel-item>
        </v-carousel>

        <v-card-title>
          {{this.model.name}}
        </v-card-title>

        <v-card-text>
            <v-row
              align="center"
              class="mx-0"
            >
              <v-rating
                :value="Number(this.model.score)"
                color="amber"
                dense
                half-increments
                readonly
                size="14"
              ></v-rating>

              <div class="grey--text ms-4">
                {{this.model.score}} ({{this.model.comments}})
              </div>

            </v-row>

            <div class="my-3 text-subtitle-2" >{{this.model.description}}</div>

        </v-card-text>

        <v-divider class="mx-4"></v-divider>

        <v-card-text>
          
          <div>
             <span style= "font-weight: bold"> Aforo Máximo </span> : {{ this.model.max}}
          </div>

          <div>
             <span style= "font-weight: bold" > Categoría </span> : {{ this.model.category_name}} 
          </div>

        </v-card-text>

       <v-divider class="mx-4"></v-divider>

        <v-card-actions>
          <v-btn
            color="red lighten-2"
            text
            @click="hide"
          >
            Cerrar
          </v-btn>
        </v-card-actions>

      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { getJSON } from "../helpers/Request";
import { formatDateAndTime } from "@/helpers/Date"
import { notification } from "@/helpers/Notifications";

  export default {

    data: () => ({
        dialog : false,

        model: {
        
            id : "",
            category_id : "",
            category_name : "",
            name: "",
            description: "",
            max: "",
            score: 0,
            comments: 0

        },

        items: [
          {
            src: 'https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg',
          },
          {
            src: 'https://cdn.vuetifyjs.com/images/carousel/sky.jpg',
          },
          {
            src: 'https://cdn.vuetifyjs.com/images/carousel/bird.jpg',
          },
          {
            src: 'https://cdn.vuetifyjs.com/images/carousel/planet.jpg',
          },
        ],
    }),

    methods: {
        formatDateAndTime,
        show(params) {
            this.getItem(params);
        },
        hide(){
            this.dialog = false
        },
        reserve(){
            /// not implemented yet
        },
        getItem(params){
            getJSON("/places/find", params, false)
            .then((res) => {
                if (res.error) {
                    notification({
                        message: res.message,
                    }); 
                }
                else{
                    this.model = res.data;
                    this.dialog = true;
                    
                }
            })
            .catch((err) => {

                notification({
                    message: "Ocurrió un error al hacer la petición",
                });
            });
        }
    }    
  }
</script>