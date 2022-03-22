export const getYesterday = date1 => {
  const dt = new Date(date1);
  return new Date((dt.setDate(dt.getDate()-1))).toDateString();
}

export const toNormalDate = (seconds, todayText, yesterdayText) => {

  const dateObject = new Date(seconds * 1000)

  const orderDay = dateObject.toLocaleString("en-EN", {day: "numeric"})
  const orderMonth = dateObject.toLocaleString("en-EN", {month: "long"})
  const orderYear = dateObject.toLocaleString("en-EN", {year: "numeric"})

  let orderHour = dateObject.toLocaleString("en-EN", {hour: "numeric"})
  let orderMinute = dateObject.toLocaleString("en-EN", {minute: "numeric"})

  orderHour = orderHour.length === 1 ? '0' + orderHour : orderHour
  orderMinute = orderMinute.length === 1 ? '0' + orderMinute : orderMinute

  const orderDateString = dateObject.toDateString()
  const todayDateString = new Date().toDateString()

  const isToday = (todayDateString === orderDateString)
  const isYesterday = (getYesterday(todayDateString) === orderDateString)

  // slice month length like January -> Jan
  let date = orderDay + ' ' + orderMonth.slice(0, 3) + ' ' + orderYear

  if (isToday) date = todayText
  else if (isYesterday) date = yesterdayText

  const time = orderHour + ':' + orderMinute

  return date + '  ' + time
}
