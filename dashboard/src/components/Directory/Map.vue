<template>
  <l-map style="z-index:0; height: 100%" :zoom="zoom" :center="center">

    <ShowEvent ref="ShowEvent"></ShowEvent>

    <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <l-marker 
          :lat-lng="markerLatLng" 
          @click="showInfoEvent('E43037b9d-34c3-452d-a43d-e8f068cd447f','C01')" >
      </l-marker>

  </l-map>
</template>

<script>
import { latLng } from "leaflet";
import { LMap, LTileLayer, LMarker, LPopup} from "vue2-leaflet";
import { getJSON } from "../../helpers/Request";
import { Icon } from 'leaflet';
import ShowEvent from '../ShowEvent';

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
    ShowEvent
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
    },
  };
</script>

