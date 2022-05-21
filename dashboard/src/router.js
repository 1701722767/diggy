import Vue from 'vue';
import Router from 'vue-router';
import Login from './components/Login.vue';
import Register from './components/Register.vue'
import EventRegister from './components/Events/Register.vue'
import Map from './components/Map.vue'
import EventList from './components/Events/List.vue'



Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,

    routes: [
        {
            path: '/',
            name: 'home',
            name: 'dashboard',
            component: Map,
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
