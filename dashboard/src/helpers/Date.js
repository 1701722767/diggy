import moment from 'moment';

moment.locale('es');

export const formatDateAndTime = function (strigDate) {
  return moment.utc(strigDate).format('dddd D [de] MMMM [del] YYYY [a las] h:mm a');
}