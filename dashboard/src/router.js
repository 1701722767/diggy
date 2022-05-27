import Vue from 'vue';
import Router from 'vue-router';
import Login from './components/Auth/Login.vue';
import Register from './components/Auth/Register.vue'
import Confirm from './components/Auth/Confirm.vue'
import EventRegister from './components/Events/Register.vue'
import Container from './components/Directory/Container.vue'
import Map from './components/Directory/Map.vue'
import EventsPublicList from './components/Directory/Events.vue'
import PlacesPublicList from './components/Directory/Places.vue'
import EventList from './components/Events/List.vue'



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
                component: EventsPublicList
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
          path: '/events-list',
          name: 'list',
          component: EventList
        },
    ],
});
