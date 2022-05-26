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
<style scoped>
.container {
  padding: 0;
  height: 100vh;
}
</style>
