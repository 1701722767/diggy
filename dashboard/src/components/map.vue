<template>
    <div class="row map">
    <l-map :zoom="zoom" :center="center">
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <l-marker :lat-lng="marker"></l-marker>
    </l-map>
    </div>
</template>

<script>
    import L from 'leaflet';
    import { LMap, LTileLayer, LMarker } from 'vue2-leaflet';
  export default {
    name: 'HelloWorld',
    components: {
    LMap,
    LTileLayer,
    LMarker,
    },
    data: function() {
      return{
        zoom:13,
        center: L.latLng(47.413220, -1.219482),
        url:'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
        marker: L.latLng(47.413220, -1.219482),
      }
    },
  }
</script>

<style scoped>
    .map{
        height: 50%;
        margin: 0;
    }
</style>