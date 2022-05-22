import { APP_HOST } from "../config/Constants.js";
import { TOKEN_KEY } from "../config/Constants.js";

export const postJSON = async function (path = "", data = {}, needToken) {
  let url = APP_HOST + path;
  let aHeaders = new Headers();
  aHeaders.append("Content-Type", "application/json");

  if (needToken) {
    let token = localStorage.getItem(TOKEN_KEY);
    if (token != null) {
      aHeaders.append(TOKEN_KEY, token);
    } else {
      throw "No se pudo obtener el token";
    }
  }
  const response = await fetch(url, {
    method: "POST",
    cache: "no-cache",
    credentials: "same-origin",
    redirect: "follow",
    referrerPolicy: "no-referrer",
    body: JSON.stringify(data),
  });
  return response.json();
};

export const getJSON = async function (path = "", params = null, needToken) {
  let url = APP_HOST + path;
  if (needToken) {
    let token = localStorage.getItem(TOKEN_KEY);
    if (token != null) {
      aHeaders.append(TOKEN_KEY, token);
    } else {
      throw "No se pudo obtener el token";
    }
  }

  console.log(params);

  if (params !== null) {
    console.log("url");
    url += "?" + new URLSearchParams(params).toString();
  }
  console.log(url);

  const response = await fetch(url, {
    method: "GET",
    cache: "no-cache",
    credentials: "same-origin",
    redirect: "follow",
    referrerPolicy: "no-referrer",
  });


  return response.json();
};

export const deleteJSON = async function (path = "", data = {}, needToken) {
  let url = APP_HOST + path;
  let aHeaders = new Headers();
  aHeaders.append("Content-Type", "application/json");

  if (needToken) {
    let token = localStorage.getItem(TOKEN_KEY);
    if (token != null) {
      aHeaders.append(TOKEN_KEY, token);
    } else {
      throw "No se pudo obtener el token";
    }
  }
  const response = await fetch(url, {
    method: "DELETE",
    cache: "no-cache",
    credentials: "same-origin",
    headers: aHeaders,
    redirect: "follow",
    referrerPolicy: "no-referrer",
    body: JSON.stringify(data),
  });
  return response.json();
};
