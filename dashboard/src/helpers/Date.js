import moment from 'moment';

moment.locale('es');

export const formatDateAndTime = function (stringDate) {
  return moment.utc(stringDate).format('dddd D [de] MMMM [del] YYYY [a las] h:mm a');
}

export const transformDate = function (stringDate){
  return moment.utc(stringDate).format('YYYY-MM-DD HH:mm:ss');
}