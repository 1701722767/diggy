<template>
  <div class="container-directory">
    <div class="content">
      <router-view></router-view>
    </div>
    <v-bottom-navigation color="deep-purple accent-4">

      <v-btn :to="{ path: '/directory/map' }">
        <span>Mapa</span>

        <v-icon>mdi-map-search-outline</v-icon>
      </v-btn>

      <v-btn :to="{ path: '/directory/events' }">
        <span>Eventos</span>

        <v-icon>mdi-calendar</v-icon>
      </v-btn>

      <v-btn :to="{ path: '/directory/places' }">
        <span>Lugares</span>

        <v-icon>mdi-map-marker-outline</v-icon>
      </v-btn>
    </v-bottom-navigation>
  </div>
</template>

<script>
export default {
  name: "Container",

  data() {
    return {
      tab: 1,
    };
  },
};
</script>

<style scoped>
.container-directory {
  height: 100%;
  
}

.content {
  height: 100vh;
  max-height: 100%;
  overflow: auto;
}

.v-bottom-navigation {
  bottom: 0;
  position: absolute;
}
</style>
