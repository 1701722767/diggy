import Emitter from "../services/Emitter.js";

export const notification = async function (payload) {
  Emitter.emit("show-notification", payload);
};
