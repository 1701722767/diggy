import Vue from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import router from "./router";
import "vuetify/dist/vuetify.min.css";
import "leaflet/dist/leaflet.css";
import { AWS_CONFIG } from "./services/Auth.js";
import Amplify from "aws-amplify";
import { Hub } from "aws-amplify";
import DatetimePicker from 'vuetify-datetime-picker';
import { getTokenFirebase } from "./services/Firebase"


Amplify.configure(AWS_CONFIG.Auth);

const listener = (data) => {
  switch (data.payload.event) {
    case "tokenRefresh_failure":
      Emitter.emit("reload-navbar-items");
      router.push({ path: "/login" });
      break;
  }
};

Hub.listen("auth", listener);

getTokenFirebase();

Vue.config.productionTip = false;
Vue.use(vuetify);
Vue.use(DatetimePicker);

new Vue({
  vuetify,
  router,
  render: (h) => h(App),
}).$mount("#app");
