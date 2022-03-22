import {
  CLEAR_ORDERS,
  FETCH_ORDERS_ERROR,
  LOADING_ORDERS,
  SAVE_ORDERS,
} from "../types/ordersTypes"

export const fetchAllOrders = (firestore) => async (dispatch, getState) => {
  const userId = getState().auth.user.id

  const today = new Date()
  today.setHours(0, 0, 0, 0)

  dispatch(loadingOrders())
  console.log('orders in fetchAllOrders: ')
  console.log('User ID', userId)

  return firestore.collection("orders")
    .where("store", "==", userId)
    .onSnapshot(async querySnapshot => {
      const docs = []
      querySnapshot.forEach(doc => docs.push({ id: doc.id, ...doc.data() }))
      dispatch(saveOrders(docs))
    }, error => {
      dispatch(fetchOrdersError(error.toString()))
    })
}

export const saveOrders = orders => {
  return {
    type: SAVE_ORDERS,
    payload: orders
  }
}

export const loadingOrders = () => {
  return {
    type: LOADING_ORDERS
  }
}

export const fetchOrdersError = () => {
  return {
    type: FETCH_ORDERS_ERROR
  }
}

export const clearOrders = () => {
  return {
    type: CLEAR_ORDERS
  }
}
