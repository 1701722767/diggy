<template>
  <v-app>
    <notification/>
    <nav-bar> </nav-bar>
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import NavBar from "./components/NavBar.vue";
import Notification from './components/Notification.vue';

export default {
  components: { NavBar, Notification },
  name: "App",
};
</script>
<style>
html{
  overflow: hidden !important;
}
</style>
<style scoped>
html, body, #app{
  height: 100%;
  padding: 0;
  margin: 0;
  overflow: hidden !important;
}

notification{
  z-index: 1000000000 !important;
}

.v-main {
  height: 100vh;
  padding-bottom: 49px !important;
}
</style>
