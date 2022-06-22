// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getMessaging, getToken, onMessage } from "firebase/messaging";
import { isAuthenticate } from "./Auth";
import { postJSON } from "@/helpers/Request";
import { notification } from "@/helpers/Notifications";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

const firebaseConfig = {
  apiKey: process.env.VUE_APP_API_KEY,
  authDomain: "encoded-keyword-270113.firebaseapp.com",
  projectId: "encoded-keyword-270113",
  storageBucket: "encoded-keyword-270113.appspot.com",
  messagingSenderId: "607844518648",
  appId: "1:607844518648:web:430bd204cad711954c090d",
  measurementId: "G-CN3426KT9V",
};

const app = initializeApp(firebaseConfig);
const messaging = getMessaging(app);

export const getTokenFirebase = () => {
    getToken(messaging, {
        vapidKey:
        "BEP3v3Oq4LO9qgMQuvxm2AtErmVXChzKgSJ_e64xxrK4Pss9p2eclhv0B0q_1R13o_hI95oBKObNSzuUFCnkMQI",
       }).then( async (currentToken) => {
        if (currentToken) {
          let isAuth =  await isAuthenticate();
          if (isAuth) {
            const token = {
              FCM_token : currentToken
            }
            postJSON("/users/token",token,true)
            .then((res)=>{
              if(!res.error){
                notification({
                  message : "Te notificaremos cuando haya un evento nuevo de tú interés"
                })
              }
              else{
                notification({
                  message : "No se pudieron activar las notificaciones"
                })
              }
             
            })
            .catch((err)=>{
              notification({
                message : "No se pudieron activar las notificaciones"
              })
            })
          }
    
        
        } else {
          notification({
            message : "Activa las notificaciones para que no te pierdes los últimos eventos"
          })
        }
      })
      .catch((err) => {
        notification({
          message : "Activa las notificaciones para que no te pierdes los últimos eventos"
        })
      });
    
    /// Need implementation when page is in foreground!!!!
    onMessage(messaging, (payload) => {
      console.log("Message received. ", payload);
      // ...
    });
}

