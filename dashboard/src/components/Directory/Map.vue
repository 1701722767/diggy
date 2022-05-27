<template>
  <l-map style="z-index:0; height: 100%" :zoom="zoom" :center="center">

    <PopUp ref="PopUp"></PopUp>

    <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <l-marker 
          :lat-lng="markerLatLng" 
          @click="showPopUp" >
      </l-marker>

  </l-map>
</template>

<script>
import { latLng } from "leaflet";
import { LMap, LTileLayer, LMarker, LPopup} from "vue2-leaflet";
import { getJSON } from "../../helpers/Request";
import { Icon } from 'leaflet';
import PopUp from '../PopUp';

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
    PopUp
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

      params :{
          composite_key: "ew0KICAiZXZlbnRfaWQiIDogIkU0MzAzN2I5ZC0zNGMzLTQ1MmQtYTQzZC1lOGYwNjhjZDQ0N2YiICwNCiAgImNhdGVnb3J5X2lkIiA6ICJDMDEiDQp9"
      },

    };
  },

  methods : {
      showPopUp (){
        this.$refs.PopUp.show('/find', this.params);
      },
    },
  };
</script>

