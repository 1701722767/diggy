<template>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>
        <v-btn href="/" width="60px" icon> DIGGY </v-btn>
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn href="/" icon>
        <v-icon>mdi-map-marker</v-icon>
      </v-btn>
    </v-app-bar>
</template>

<script>
export default {
  name: "NavBar",
  data() {
    return {
      drawer: false,
      group: null,
    };
  },
};
</script>

<style lang="scss" scoped>
.body {
  height: 100%;
  border: 1px solid red;
}

#content {
  height: 100%;
}
</style>
