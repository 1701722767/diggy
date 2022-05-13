import Vue from 'vue';
import Router from 'vue-router';
import Login from './components/Login.vue';
import HelloWorld from './components/HelloWorld.vue';


Vue.use(Router);

export default new Router({
    routes: [        
        {
            path: '/',
            name: 'dashboard',
            component: HelloWorld,
        },
        {
            path: '/login',
            name: 'login',
            component: Login,
        }
    ],
    
});