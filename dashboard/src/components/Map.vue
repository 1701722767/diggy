<template>
  <l-map style="height: 100%" :zoom="zoom" :center="center">
    <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
    <l-marker :lat-lng="markerLatLng" @click="getEvent">
      <l-popup> 
          <v-carousel hide-delimiters height=100 >
            <v-carousel-item
              v-for="(item,i) in items"
              :key="i"
              :src="item.src"
            ></v-carousel-item>
          </v-carousel>

          <v-card-title>{{this.model.name}}</v-card-title>

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
              $ • {{this.model.price}}
            </div>

            <div>{{this.model.description}}</div>

        
          </v-card-text>
        <v-divider class="mx-4"></v-divider>

        <v-card-text>
          <div>
             <strong> Inicia </strong> : {{ this.model.datestart}}
          </div>
          <div>
             <strong> Termina </strong> : {{ this.model.dateend}}
          </div>
          <div>
             <strong> Aforo Máximo </strong> : {{ this.model.max}}
          </div>
          <div>
             <strong> Cupos disponibles</strong> : {{ this.model.slots}}
          </div>
          <div>
             <strong> Rango de edad </strong> : {{this.model.range_age[0]}} - {{this.model.range_age[1]}} años
          </div>
        
        </v-card-text>


        <v-divider class="mx-4"></v-divider>


        <!--This info can be used for a place info>

        <!--<v-card-title>24 de Mayo del 2022</v-card-title>-->

        <!--<v-card-text>
          <v-chip-group
            v-model="selection"
            active-class="deep-purple accent-4 white--text"
            column
          >
          <v-chip>5:30PM</v-chip>

          <v-chip>7:30PM</v-chip>

          <v-chip>8:00PM</v-chip>

         
          </v-chip-group>
        </v-card-text> -->

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

      model: {
        
        event_id : "",
        name: "",
        description: "",
        dateend: "",
        datestart: "",
        max: "",
        name: "",
        price: "",
        range_age: "",
        slots: "",
      },

      params :{
        composite_key: "ewogICJldmVudF9pZCI6ICJFYjMyZTMyZmUtZGRlNi00YjNjLTkxNjAtZjAxYTY3ZDYwYWIxIiwKICAiY2F0ZWdvcnlfaWQiOiAiQzAxIgp9"
      },

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

      getEvent (){
        getJSON("/find", this.params, false)
          .then((res) => {
            this.model = res.data;
            console.log(res);

          })
          .catch((err) => {
            console.log(err);
          });
      }

    },
  };
</script>

<style>

.leaflet-popup-content{
  width:400px;
}

</style>

