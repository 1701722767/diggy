import Vue from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import router from "./router";
import "vuetify/dist/vuetify.min.css";
import "leaflet/dist/leaflet.css";
import { AWS_CONFIG } from "./services/Auth.js";
import Amplify from "aws-amplify";
import { Hub } from "aws-amplify";


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




// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getMessaging, getToken, onMessage } from "firebase/messaging";
import Emitter from "./services/Emitter";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional

const firebaseConfig = {
  apiKey: process.env.VUE_APP_API_KEY,
  authDomain: "encoded-keyword-270113.firebaseapp.com",
  projectId: "encoded-keyword-270113",
  storageBucket: "encoded-keyword-270113.appspot.com",
  messagingSenderId: "607844518648",
  appId: "1:607844518648:web:430bd204cad711954c090d",
  measurementId: "G-CN3426KT9V",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Cloud Messaging and get a reference to the service
const messaging = getMessaging(app);

getToken(messaging, {
  vapidKey:
    "BEP3v3Oq4LO9qgMQuvxm2AtErmVXChzKgSJ_e64xxrK4Pss9p2eclhv0B0q_1R13o_hI95oBKObNSzuUFCnkMQI",
})
  .then((currentToken) => {
    if (currentToken) {
      // Send the token to your server and update the UI if necessary
      // ...
      console.log(currentToken);

      const h3 = document.createElement("h3");
      const newContent = document.createTextNode(currentToken);
      h3.appendChild(newContent); //añade texto al div creado.

      const app = document.getElementById("token");
      app.appendChild(h3);
    } else {
      // Show permission request UI
      console.log(
        "No registration token available. Request permission to generate one."
      );
      // ...
    }
  })
  .catch((err) => {
    console.log("An error occurred while retrieving token. ", err);
  });

/// Need implementation when page is in foreground!!!!
onMessage(messaging, (payload) => {
  console.log("Message received. ", payload);
  // ...
});

Vue.config.productionTip = false;
Vue.use(vuetify);

new Vue({
  vuetify,
  router,
  render: (h) => h(App),
}).$mount("#app");
