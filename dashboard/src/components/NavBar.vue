<template>
  <div>
    <v-app-bar color="deep-purple accent-4" dense dark>
      <template v-if="width > 700">
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
            @click="goToPath(item.path)"
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
                @click="goToPath(item.path)"
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
export default {
  name: "NavBar",
  data() {
    return {
      drawer: false,
      group: null,
      width: 0,
      sheet: false,
      items: [
        { icon: "mdi-map-search-outline", title: "Ver mapa", path: "/" },
        { icon: "mdi-account-plus-outline", title: "Registrarme", path: "register" },
        { icon: "mdi-account-key-outline", title: "Iniciar sesión", path: "login" },
      ],
    };
  },
  mounted() {
    this.width = window.innerWidth;
  },
  created() {
    window.addEventListener("resize", this.onResize);
  },
  destroyed() {
    window.removeEventListener("resize", this.onResize);
  },
  methods: {
    onResize(e) {
      this.width = window.innerWidth;
    },
    goToPath(path){
      this.sheet = false;
      console.log(this.$router);
      this.$router.push({path:path});
    }
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
