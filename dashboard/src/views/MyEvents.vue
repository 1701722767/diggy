<template>
  <div class="content">
    <v-col cols="12" sm="6" md="6">
      <v-btn x-large color="success" :to="{ path: '/event-register' }"
        >Crear evento
      </v-btn>
    </v-col>
  </div>
</template>

<script>
export default {
  name: "MyEvents",
  data: function() {
return {};
},
  methods: {},
};
</script>

<style>
.content {
  height: 100%;
  padding-bottom: 56px;
}
</style>

