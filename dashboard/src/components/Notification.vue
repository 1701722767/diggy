<template>
  <v-snackbar v-model="show" color="deep-purple accent-4">
    <v-icon>{{ icon }}</v-icon>
    {{ message }}

    <template v-slot:action="{ attrs }">
      <v-btn color="grey" text v-bind="attrs" @click="show = false">
        Cerrar
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
import Emitter from "../services/Emitter.js";

export default {
  name: "Notification",
  data() {
    return {
      show: false,
      icon: '',
      message: "",
    };
  },
  mounted() {
    Emitter.off("show-notification");
    Emitter.on("show-notification", (payload) => {
      this.show = true;
      this.icon = payload.icon;
      this.message = payload.message;
    });
  },
};
</script>
