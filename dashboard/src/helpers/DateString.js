export const transformDate = function (date){
    date = new Date(date);
    const hour = date.toLocaleTimeString();
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();

    return `${year}-${month}-${day} ${hour}`;
}