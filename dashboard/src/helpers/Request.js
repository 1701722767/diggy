import { getToken } from "@/services/Auth.js";
import { APP_HOST } from "../config/Constants.js";
import { TOKEN_KEY } from "../config/Constants.js";

export const postJSON = async function (path = "", data = {}, needToken) {
  let url = APP_HOST + path;
  let headers = await getHeaders(needToken);

  const response = await fetch(url, {
    method: "POST",
    cache: "no-cache",
    credentials: "same-origin",
    redirect: "follow",
    headers: headers,
    referrerPolicy: "no-referrer",
    body: JSON.stringify(data),
  });

  return response.json();
};

export const getJSON = async function (path = "", params = null, needToken) {
  let url = APP_HOST + path;

  if (params !== null) {
    url += "?" + new URLSearchParams(params).toString();
  }

  let headers = await getHeaders(needToken);

  const response = await fetch(url, {
    method: "GET",
    cache: "no-cache",
    credentials: "same-origin",
    headers: headers,
    redirect: "follow",
    referrerPolicy: "no-referrer",
  });

  return response.json();
};

export const deleteJSON = async function (path = "", data = {}, needToken) {
  let url = APP_HOST + path;
  let headers = await getHeaders(needToken);

  const response = await fetch(url, {
    method: "DELETE",
    cache: "no-cache",
    credentials: "same-origin",
    headers: headers,
    redirect: "follow",
    referrerPolicy: "no-referrer",
    body: JSON.stringify(data),
  });

  return response.json();
};

const getHeaders = async (needToken) => {
  let headers = new Headers();

  if (!needToken) {
    return headers;
  }

  let token = await getToken();
  console.log("token:", token);
  if (token == null) {
    throw "No se pudo obtener el token";
  }

  headers.append(TOKEN_KEY, token);

  return headers
};
