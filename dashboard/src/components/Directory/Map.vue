<template>
  <l-map 
    style="z-index:0; height: 100%" 
    :zoom="zoom" 
    :center="center"
    @ready="onReady" 
    ref="map" 
    @locationfound="onLocationFound"
  >

    <ShowEvent ref="ShowEvent"></ShowEvent>

    <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>

      <l-marker 
          v-for = "(event,i) in events"
          :key= "i"
          :lat-lng="[event.coordinates.latitude,event.coordinates.longitude]"
          @click="showInfoEvent(event.event_id,event.category_id)" 
      >

        <l-tooltip :options= "optionsTooltip" >{{event.name}}</l-tooltip>

        <l-icon
          :tooltipAnchor="[20,-10]"
          :icon-size="[45, 45]"
          icon-url="https://cdn-icons-png.flaticon.com/512/6554/6554348.png" >
        </l-icon>

      </l-marker>

      <template v-if="location">
        <l-marker :lat-lng="location.latlng">
          <l-icon
            :tooltipAnchor="[20,-10]"
            :icon-size="[45, 45]"
            icon-url="https://cdn-icons-png.flaticon.com/512/1949/1949165.png" 
          >
          </l-icon>
        </l-marker>
      </template>

  
  </l-map>
</template>

<script>
import { latLng } from "leaflet";
import { LMap, LTileLayer, LMarker , LTooltip, LIcon} from "vue2-leaflet";
import { getJSON } from "../../helpers/Request";
import { Icon } from 'leaflet';
import ShowEvent from '../ShowEvent';
import { notification } from "@/helpers/Notifications";

export default {
  name: "Map",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LTooltip,
    LIcon,
    ShowEvent
  },
  mounted() {
    // Get events
    getJSON("/events", null, false)
      .then((res) => {
        if(res.error){
          notification({
            message: res.message,
          });
        }
        else{
          this.events = res.data.items;
        } 
    }).catch((err) => {
         notification({
            message: "Ocurrió un error al hacer la petición",
          }); 
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

      map: null,
      location: null,

      optionsTooltip : {
        permanent : true,
      
      },
      events : []
    };
  },

  methods : {
      showInfoEvent (event_id,category_id){
        const keys = btoa(
          `{
            "event_id" : "${event_id}" ,
            "category_id" : "${category_id}"
            }`);
        
        const param = { composite_key : keys };
        this.$refs.ShowEvent.show(param);
      },

      onReady() {
        this.map = this.$refs["map"].mapObject;
        this.map.locate();
      },

      onLocationFound(currentLocation) {
        this.location = currentLocation;
      },

    },
  };
</script>

