<template>
  <l-map
    style="z-index: 0; height: 100%"
    :zoom="zoom"
    :center="center"
    @ready="onReady"
    ref="map"
    @locationfound="onLocationFound"
    @moveend="onMouseMove"
  >
    <ShowEvent ref="ShowEvent"></ShowEvent>
    <ShowPlace ref="ShowPlace"></ShowPlace>
    <ShowUser ref="ShowUser"></ShowUser>

    <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>

    <l-marker
      v-for="(event) in events"
      :key="event.event_id"
      :lat-lng="[event.coordinates.latitude, event.coordinates.longitude]"
      @click="showInfoEvent(event.event_id, event.category_id)"
    >
      <l-tooltip :options="optionsTooltip">{{ event.name }}</l-tooltip>

      <l-icon
        :tooltipAnchor="[20, -10]"
        :icon-size="[45, 45]"
        icon-url="https://cdn-icons-png.flaticon.com/512/6554/6554348.png"
      >
      </l-icon>
    </l-marker>

    <l-marker
      v-for="(place) in places"
      :key="place.id"
      :lat-lng="[place.coordinates.latitude, place.coordinates.longitude]"
      @click="showInfoPlace(place.id, place.category_id)"
    >
      <l-tooltip :options="optionsTooltip">{{ place.name }}</l-tooltip>

      <l-icon
        :tooltipAnchor="[20, -10]"
        :icon-size="[45, 45]"
        icon-url="https://cdn1.iconfinder.com/data/icons/vibrancie-map/30/map_026-location-marker-favorite-pin-star-256.png"
      >
      </l-icon>
    </l-marker>

    <template v-if="location">
      <l-marker :lat-lng="location.latlng" @click="showInfoUser">
        <l-icon
          :tooltipAnchor="[20, -10]"
          :icon-size="[45, 45]"
          icon-url="https://cdn-icons-png.flaticon.com/512/1949/1949165.png"
        >
        </l-icon>
      </l-marker>
    </template>
  </l-map>
</template>

<script>
import { LMap, LTileLayer, LMarker, LTooltip, LIcon } from "vue2-leaflet";
import { getJSON } from "../../helpers/Request";
import ShowEvent from "../Events/Show";
import ShowPlace from "../Places/Show";
import ShowUser from "@/components/User";
import { notification } from "@/helpers/Notifications";

export default {
  name: "Map",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LTooltip,
    LIcon,
    ShowEvent,
    ShowPlace,
    ShowUser
  },
  mounted() {
    this.getEvents(this.center);
    this.getPlaces();
  },
  data() {
    return {
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 16,
      center: [5.0569, -75.50356],

      currentCenter: null,
      map: null,
      location: null,

      optionsTooltip: {
        permanent: true,
      },

      events: [],
      places: [],

    };
  },

  methods: {
    showInfoEvent(event_id, category_id) {
      const keys = btoa(
        `{
            "event_id" : "${event_id}" ,
            "category_id" : "${category_id}"
            }`
      );

      const param = { composite_key: keys };
      this.$refs.ShowEvent.show(param);
    },

    showInfoPlace(place_id, category_id) {
      const keys = btoa(
        `{
            "id" : "${place_id}" ,
            "category_id" : "${category_id}"
            }`
      );

      const param = { composite_key: keys };
      this.$refs.ShowPlace.show(param);
    },

    showInfoUser(){
      this.$refs.ShowUser.show();
    },

    onReady() {
      this.map = this.$refs['map'].mapObject;
      this.map.locate();
    },

    onLocationFound(currentLocation) {
      this.location = currentLocation;
      this.recenterMap(this.location.latlng);
    },

    onMouseMove(){
        const currentCenter = this.$refs['map'].mapObject.getCenter();
        this.getEvents([currentCenter.lat,currentCenter.lng])
    },

    recenterMap(currentLocation) {
      this.$refs["map"].mapObject.panTo(currentLocation);
    },

    getEvents(center) {
      const centerCoordinates = btoa(
        `{
          "latitude": ${center[0]},
          "longitude": ${center[1]}
        }`)
      
      const params = { center_coordinates : centerCoordinates}

      getJSON("/events/closest",params,false)
        .then((res) => {
          if (res.error) {
            notification({
              message: res.message,
            });
          } else {
            this.events = res.data.items;
          }
        })
        .catch((err) => {
          notification({
            message: "Error al realizar la petición",
          });
        });
    },

    getPlaces() {
      getJSON(
        "/places",
        {
          type: "default",
        },
        false
      )
        .then((res) => {
          if (res.error) {
            notification({
              message: res.message,
            });
          } else {
            this.places = res.data.items;
          }
        })
        .catch((err) => {
          notification({
            message: "Ocurrió un error al hacer la petición",
          });
        });
    },
  },
};
</script>
