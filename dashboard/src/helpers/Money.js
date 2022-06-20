export const toCurrency = function(value) {
  try {
    value = parseInt(value);
  } catch (error) {
    return value;
  }

  var formatter = new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    minimumFractionDigits: 0,
  });

  return formatter.format(value).replace(/\s/g, '');
};