<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" max-width="300px">
        <v-card
            max-width="300px"
        >
            <v-card-title>Nicolas Cardona</v-card-title>

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
                    <span style= "font-weight: bold"> Nombre de usuario </span> : nicolascr181
                </div>
                <div>
                    <span style= "font-weight: bold"> Email  </span> : nicolascr181@gmail.com
                </div>
                 <div>
                    <span style= "font-weight: bold"> Teléfono  </span> : +57 323-444-0587
                </div>
                <div>
                    <span style= "font-weight: bold"> Fecha de nacimiento </span> : 1998-09-04
                </div>
                <div>
                    <span style= "font-weight: bold"> Categorías de interés </span> : Música,Social
                </div>
                <div>
                    <span style= "font-weight: bold"> Saldo </span> : $ 20.000
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
  export default {
    data: () => ({
      dialog: false,
    }),

    methods: {
        show() {
            this.dialog = true;
        },
        hide() {
            this.dialog = false;
        }
    }
  }
</script>