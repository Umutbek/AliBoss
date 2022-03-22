import {
  CLEAR_ORDERS,
  LOADING_ORDERS,
  FETCH_ORDERS_ERROR,
  SAVE_ORDERS
} from '../types/ordersTypes'

const initialState = {
  orders: [],
  isOrdersLoading: false,
  error: {}
}

export default function orderReducer(state = initialState, action) {
  switch (action.type) {
    case LOADING_ORDERS:
      return {
        ...state,
        isOrdersLoading: true,
        error: {}
      }
    case SAVE_ORDERS:
      return {
        ...state,
        orders: [...action.payload],
        isOrdersLoading: false,
        error: {}
      }
    case CLEAR_ORDERS:
      return {
        ...state,
        orders: [],
        error: {}
      }
    case FETCH_ORDERS_ERROR:
      return {
        ...state,
        isOrdersLoading: false,
        error: action.payload
      }
    default:
      return {
        ...state
      }
  }
}
