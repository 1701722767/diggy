
<template>
    <div class="ma-20 pa-25">
    <v-card>
      <v-navigation-drawer
        permanent
        expand-on-hover
      >
        <v-list>
          <v-list-item class="px-2">
            <v-list-item-avatar>
              <v-img src="https://storage.googleapis.com/media.clinicavisualyauditiva.com/images/2019/11/211fd983-default-user-image.png"></v-img>
            </v-list-item-avatar>
          </v-list-item>

          <v-list-item link>
            <v-list-item-content>
              <v-list-item-title class="text-h6">
                nombre usuario
              </v-list-item-title>
              <v-list-item-subtitle>username</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list
          nav
          dense
        >
        <v-text-field
          v-model="search"
          label="Buscar"
          single-line
          hide-details
        ></v-text-field>
        <v-spacer></v-spacer>
          <v-list-item link>
            <v-list-item-icon>
                
                  <v-btn icon href="/Login" target="_blank"> <v-icon>
                    mdi-calendar
                    </v-icon> </v-btn>
                  
              
            </v-list-item-icon>
            <v-list-item-title>Mis eventos</v-list-item-title>
          </v-list-item>
          <v-list-item link>
            <v-list-item-icon>
              <v-icon>mdi-account-arrow-left</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Ajustes</v-list-item-title>
          </v-list-item>
          <v-list-item link>
            <v-list-item-icon>
              <v-icon>mdi-logout</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Cerrar sesión</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
    </v-card>
  </div>
</template>

<script>
  export default {
    name: 'HelloWorld',

    data: () => ({
    }),
  }
</script>
