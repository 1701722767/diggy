<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <v-toolbar-title>
        <v-btn href="/map" width="60px" icon> 
        DIGGY
        </v-btn>
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn href="/map" icon>
        <v-icon>mdi-map-marker</v-icon>
      </v-btn>

      <v-btn href="/list" icon>
        <v-icon>mdi-playlist-star</v-icon>
      </v-btn>

      <v-btn  icon>
        <v-icon >mdi-magnify</v-icon>
      </v-btn>

      <v-menu
        left
        bottom
      >
        <span class="mr-2">Latest Release</span>
        <v-icon>mdi-open-in-new</v-icon>
    </v-app-bar>

    
  
      <!-- Provides the application the proper gutter -->
      <v-container fluid>
        <!-- If using vue-router -->
        <router-view></router-view>
      </v-container>

    <v-main>
      <HelloWorld/>
    </v-main>
  </v-app>
</template>

<script>
import HelloWorld from './components/HelloWorld';

export default {
  name: 'App',
  data(){
    return {
      switch1: false,
      appTitle: 'DIGGY',
      sidebar: false,
      menuItems: [
          { title: 'Home', path: '/home'},
          { title: 'Sign Out', path: '/Login' }
     ]
    }
  },
  methods: {
    toggleViews(){
      if (switch1==false) {
        this.$router.push('dashboard/login')
      }else{
        this.$router.push('dashboard/register')
      }
    }
  },
  };
</script>
