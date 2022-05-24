<template>
  <div>
    <v-snackbar v-model="showAlert" color="deep-purple accent-4">
      {{ alertMessage }}

      <template v-slot:action="{ attrs }">
        <v-btn color="grey" text v-bind="attrs" @click="showAlert = false">
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
    <v-app-bar color="deep-purple accent-4" dense dark>
      <template v-if="width > 800">
        <v-toolbar-title>Diggy</v-toolbar-title>
        <v-spacer></v-spacer>
        <div class="navbar_options">
          <v-btn
            class="option"
            color="deep-purple accent-4"
            dense
            dark
            v-for="item in items"
            :key="item.title"
            @click="doAction(item)"
          >
            <v-icon>{{ item.icon }}</v-icon>
            {{ item.title }}
          </v-btn>
        </div>
      </template>
      <template v-else>
        <v-bottom-sheet style="z-index: 1000 !important" v-model="sheet">
          <template v-slot:activator="{ on, attrs }">
            <v-app-bar-nav-icon
              dark
              v-bind="attrs"
              v-on="on"
            ></v-app-bar-nav-icon>
            <v-toolbar-title>
              <v-icon>fas fa-lock</v-icon>
              Diggy</v-toolbar-title
            >
          </template>
          <v-list>
            <v-subheader>Menú</v-subheader>
            <template v-for="item in items">
              <v-list-item
                class="mobil_menu"
                :key="item.title"
                @click="doAction(item)"
              >
                <v-list-item-avatar>
                  <v-avatar size="32px" tile>
                    <v-icon>{{ item.icon }}</v-icon>
                  </v-avatar>
                </v-list-item-avatar>
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item>
            </template>
          </v-list>
        </v-bottom-sheet>
      </template>
    </v-app-bar>
  </div>
</template>

<script>
import { isAuthenticate, logOut } from "../services/Auth";
import Emitter from "../services/Emitter.js";

export default {
  name: "NavBar",
  setup() {
    return {
      Emitter,
    };
  },
  data() {
    return {
      drawer: false,
      group: null,
      width: 0,
      sheet: false,
      items: [
        { icon: "mdi-map-search-outline", 
          title: "Ver mapa", 
          path: "/" 
        },
        {
          icon: "mdi-account-plus-outline",
          title: "Registrarme",
          path: "register",
        },
        {
          icon: "mdi-account-key-outline",
          title: "Iniciar sesión",
          path: "login",
        },
      ],

      alertMessage: "",
      showAlert: false,
    };
  },
  mounted() {
    this.width = window.innerWidth;
    this.setItems();

    Emitter.off("reload-navbar-items");
    Emitter.on("reload-navbar-items", () => {
      this.setItems();
    });
  },
  created() {
    window.addEventListener("resize", this.onResize);
  },
  destroyed() {
    window.removeEventListener("resize", this.onResize);
  },
  methods: {
    async setItems() {
      let isAuth = await isAuthenticate();
      if (!isAuth) {
        this.items = [
          { icon: "mdi-map-search-outline", 
            title: "Ver mapa", 
            path: "/" 
          },
          {
            icon: "mdi-account-plus-outline",
            title: "Registrarme",
            path: "register",
          },
          {
            icon: "mdi-account-key-outline",
            title: "Iniciar sesión",
            path: "login",
          },
        ];
        return;
      }

      this.items = [
        { icon: "mdi-map-search-outline", 
          title: "Ver mapa", 
          path: "/" 
        },
        { icon: "mdi-calendar-star", 
          title: "Mis eventos", 
          path: "/my-events",
        },
        {
          icon: "mdi-map-marker-outline",
          title: "Mis sitios",
          path: "/my-places",
        },
        { icon: "mdi-currency-usd",
          title: "Balance", 
          path: "/my-balance" },
        {
          icon: "mdi-logout",
          title: "Cerrar sesión",
          action: () => {
            logOut()
              .then((res) => {
                this.setItems();
                this.alertMessage = "Sesión cerrada con exito";
                this.showAlert = true;
              })
              .catch(() => {
                this.alertMessage = "Ocurrió un error al cerrar sesión";
                this.showAlert = true;
              });
          },
        },
      ];
    },
    onResize(e) {
      this.width = window.innerWidth;
    },
    doAction(item) {
      this.sheet = false;
      if (item.path) {
        this.$router.push({ path: item.path });
        return;
      }

      if (item.action) {
        item.action();
        return;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.v-dialog__content--active {
  z-index: 10000;
}

.option {
  display: inline;
  margin: 5px;
}

.option .v-icon {
  margin-right: 5px;
}
</style>
