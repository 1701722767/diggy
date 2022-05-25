<template>
  <l-map style="height: 100%" :zoom="zoom" :center="center">
    <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
    <l-marker :lat-lng="markerLatLng">
      <l-popup> 

          <v-carousel hide-delimiters height=100 >
            <v-carousel-item
              v-for="(item,i) in items"
              :key="i"
              :src="item.src"
            ></v-carousel-item>
          </v-carousel>

          <v-card-title>Noche Acústica</v-card-title>

          <v-card-text>
            <v-row
              align="center"
              class="mx-0"
            >
              <v-rating
                :value="4.5"
                color="amber"
                dense
                half-increments
                readonly
                size="14"
              ></v-rating>

              <div class="grey--text ms-4">
                4.5 (413)
              </div>
            </v-row>

            <div class="my-4 text-subtitle-1">
              $ • 5000
            </div>

            <div>Small plates, salads & sandwiches - an intimate setting with 12 indoor seats plus patio seating.</div>

        
          </v-card-text>
        <v-divider class="mx-4"></v-divider>

        <v-card-text>
         <strong> Estado </strong> : En curso
        </v-card-text>

        <v-divider class="mx-4"></v-divider>

        <v-card-title>24 de Mayo del 2022</v-card-title>

        <v-card-text>
          <v-chip-group
            v-model="selection"
            active-class="deep-purple accent-4 white--text"
            column
          >
          <v-chip>5:30PM</v-chip>

          <v-chip>7:30PM</v-chip>

          <v-chip>8:00PM</v-chip>

         
          </v-chip-group>
        </v-card-text>

        <v-card-actions>
          <v-btn
            color="deep-purple lighten-2"
            text
            @click="reserve"
          >
            Reservar
          </v-btn>
        </v-card-actions>

      </l-popup>
      <l-tooltip>Noche Acústica</l-tooltip>
    </l-marker>
  </l-map>
</template>

<script>
import { latLng } from "leaflet";
import { LMap, LTileLayer, LMarker, LPopup, LTooltip } from "vue2-leaflet";
import { getJSON } from "../helpers/Request";
import { Icon } from 'leaflet';

// If the marker icons are missing the issue lies in a problem with webpack, 
// a quick fix is to run this snippet:

delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

export default {
  name: "Map",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
    LTooltip
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

      selection: 1,

      items: [
          {
            src: 'https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg',
          },
          {
            src: 'https://cdn.vuetifyjs.com/images/carousel/sky.jpg',
          },
          {
            src: 'https://cdn.vuetifyjs.com/images/carousel/bird.jpg',
          },
          {
            src: 'https://cdn.vuetifyjs.com/images/carousel/planet.jpg',
          },
        ],
    
      
    };
  },

  methods : {
      reserve () {
        console.log('click')
      },
    },
  };
</script>

<style>


</style>

