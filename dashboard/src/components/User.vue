<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" max-width="300px">
        <v-card
            max-width="300px"
        >
            <v-card-title>{{ this.model.full_name }}</v-card-title>

            <v-card-text>
            <v-row
                align="center"
                class="mx-0"
            >

            </v-row>

            </v-card-text>

            <v-divider class="mx-4"></v-divider>

            <v-card-title>Mi Información Personal</v-card-title>

            <v-card-text>
                <div>
                    <span style= "font-weight: bold"> Nombre de usuario </span> : {{ this.model.user_name }}
                </div>
                <div>
                    <span style= "font-weight: bold"> Email  </span> :{{ this.model.email }}
                </div>
                 <div>
                    <span style= "font-weight: bold"> Teléfono  </span> : {{ this.model.phone_number }}
                </div>
                <div>
                    <span style= "font-weight: bold"> Fecha de nacimiento </span> : {{ this.model.birthdate }}
                </div>
                <div>
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
                </div>
                <div>
                    <span style= "font-weight: bold"> Saldo </span> : {{ this.model.amount }}
                </div>
            </v-card-text>

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

import { getJSON } from "@/helpers/Request";
import { notification } from "@/helpers/Notifications.js";

  export default {
    data: () => ({
      dialog: false,
      model :{
        full_name : "",
        birthdate : "",
        categories: "",
        amount: "",
        phone_number: "",
        email : ""

      },

      categories : []

    }),

    methods: {
        show() {
            this.getItem();
            this.getCategories();

            let user_cats = [];

            this.categories.forEach((category)=>{
                if(this.model.categories.includes(category.id)){
                    user_cats.push(category)
                }
            })

            this.categories = user_cats;
        },
        hide() {
            this.dialog = false;
        },
        getItem() {
            getJSON("/users",null,true)
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
        getCategories() {
            getJSON("/categories", this.params, false)
                .then((res) => {
                    this.categories = res.data.items;
                })
                .catch((err) => {
                    notification({
                        message: err
                    });
                });
        }
    }
  }
</script>