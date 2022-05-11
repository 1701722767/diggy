<template>
  <v-app>
    <!-- Sizes your content based upon application components -->
    <v-main> 
      <v-app-bar
      color="deep-purple accent-4"
      dense
      dark
    >
      <v-toolbar-title>DIGGY</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn icon>
        <v-icon>mdi-home</v-icon>
      </v-btn>

      <v-btn icon>
        <v-icon >mdi-magnify</v-icon>
      </v-btn>

      <v-menu
        left
        bottom
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            icon
            v-bind="attrs"
            v-on="on"
          >
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-item
            v-for="n in menuItems"
            :key="n"
            @click="() => {}"
          >
            <v-list-item-title> {{ n.title}}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
  
      <!-- Provides the application the proper gutter -->
      <v-container fluid>
        <!-- If using vue-router -->
        <router-view></router-view>
      </v-container>
    </v-main>

    <v-footer app>
      <!-- -->
    </v-footer>
  </v-app>
</template>

<script>
//import HelloWorld from './components/HelloWorld.vue';

 export default { 
  name: 'App',
  data(){
    return {
      appTitle: 'DIGGY',
      sidebar: false,
      menuItems: [
          { title: 'Home', path: '/home'},
          { title: 'Sign Out', path: '/Login' }
     ]
    }
  }
  };
</script>
