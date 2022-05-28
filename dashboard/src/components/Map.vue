<template>
  <l-map style="height: 100%" :zoom="zoom" :center="center">
    <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
    <l-marker :lat-lng="markerLatLng"></l-marker>
  </l-map>
</template>

<script>
import { latLng } from "leaflet";
import { LMap, LTileLayer, LMarker } from "vue2-leaflet";
import { getJSON } from "../helpers/Request";

export default {
  name: "Map",
  components: {
    LMap,
    LTileLayer,
    LMarker,
  },
  mounted() {
    // Get events
    getJSON("/events", null, false)
      .then((res) => {
        console.log(res);
      })
      .catch((err) => {
        console.log(err);
      });
  },
  data() {
    return {
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 16,
      center: [5.0569, -75.50356],
      markerLatLng: [5.0569, -75.50356],
    };
  },
};
</script>

