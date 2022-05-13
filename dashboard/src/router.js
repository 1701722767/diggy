import Vue from 'vue';
import Router from 'vue-router';
import Login from './components/Login.vue';
import HelloWorld from './components/HelloWorld.vue';
import Register from './components/Register.vue'
import EventRegister from './components/EventRegister.vue'


Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,

    routes: [        
        {
            path: '/',
            name: 'home',
            name: 'dashboard',
            component: HelloWorld,
        },
        {
            path: '/loginLogin',
            name: 'login',
            component: Login,
        },
        {
          path: '/register',
          name: 'register',
          component: Register
        },
        {
          path: '/eventregister',
          name: 'Event-register',
          component: EventRegister
        }
    ],
});
    