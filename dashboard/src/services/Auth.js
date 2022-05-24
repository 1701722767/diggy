import { Auth } from "aws-amplify";

export const AWS_CONFIG = {
  Auth: {
    // REQUIRED - Amazon Cognito Region
    region: "us-east-1",

    // OPTIONAL - Amazon Cognito User Pool ID
    userPoolId: "us-east-1_ioOQInE4T",

    // OPTIONAL - Amazon Cognito Web Client ID (26-char alphanumeric string)
    userPoolWebClientId: "3g6lojauvfl66gvinpqregv3mf",

    // OPTIONAL - Enforce user authentication prior to accessing AWS resources or not
    mandatorySignIn: true,
  },
};

export const logIn = (username, password) => {
  try {
    return Auth.signIn(username, password);
  } catch (err) {
    console.log(err);
    throw "Ocurrió un error al iniciar sesión";
  }
};

export const logOut = () => {
  try {
    return Auth.signOut();
  } catch (err) {
    console.log(err);
    throw "Ocurrió un error al iniciar sesión";
  }
};

export const getToken = async () => {
  let token = await Auth.currentSession()
    .then((res) => {
      let accessToken = res.getIdToken();
      return accessToken.getJwtToken();
    })
    .catch((err) => {
      console.log(err);
      throw "Ocurrió un error al obtener credenciales";
    });

  return token;
};

export const isAuthenticate = async () => {
  try {
    let response = await Auth.currentSession();
    if (response) {
      return true;
    }

    return false;
  } catch (error) {
    return false;
  }
};
