import Vue from 'vue';
import Router from 'vue-router';
import Login from './components/Auth/Login.vue';
import Register from './components/Auth/Register.vue'
import Confirm from './components/Auth/Confirm.vue'
import EventRegister from './components/Events/Register.vue'
import PlaceRegister from './components/Places/Register.vue'
import Container from './components/Directory/Container.vue'
import Map from './components/Directory/Map.vue'
import EventsList from './components/Events/List.vue'
import PlacesPublicList from './components/Places/List.vue'
import MyEvents from './views/MyEvents.vue'
import MyPlaces from './views/MyPlaces.vue'
import MyBalance from './views/MyBalance.vue'



Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,

    routes: [
        {
            path: '/directory/',
            name: 'home',
            name: 'Directory',
            component: Container,
            children: [
              {
                path: 'map',
                component: Map
              },
              {
                path: 'events',
                component: EventsList
              },
              {
                path: 'places',
                component: PlacesPublicList
              }
            ]
        },
        {
            path: '/login',
            name: 'login',
            component: Login,
        },
        {
          path: '/register',
          name: 'register',
          component: Register
        },
        {
          path: '/confirm',
          name: 'confirm',
          component: Confirm
        },
        {
          path: '/event-register',
          name: 'Eventregister',
          component: EventRegister
        },
        {
          path: '/my-events',
          name: 'MyEvents',
          component: MyEvents
        },
        {
          path: '/my-balance',
          name: 'MyBalance',
          component: MyBalance
        },
        {
          path: '/place-register',
          name: 'Placeregister',
          component: PlaceRegister
        },
        {
          path: '/my-places',
          name: 'MyPlaces',
          component: MyPlaces
        },
        {
          path: '*',
          redirect: "/directory/map"
        }
    ],
});
