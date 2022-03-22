import {
  USER_SUCCESS,
  USER_LOADING,
  USER_FAIL,
  LOGOUT,
  LOGIN_FAIL,
  LOGIN_SUCCESS,
  LOGIN_LOADING,
  CLEAR_ERROR,
} from "../types/authTypes"
import {_baseApi} from "../../services/ServerService"
import {ERRORS} from "../../constants/errors"


export const loadUser = () => async (dispatch, getState) => {
  dispatch(userLoading())

  const options = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${getState().auth.token}`,
    }
  }

  try {
    const response = await fetch(`${_baseApi}/getme/`, options)

    const data = await response.json()

    if (response.ok){

      dispatch(userSuccess(data))
    } else {
      dispatch(userFail(''))
    }
  } catch (e) {
      dispatch(userFail(''))
  }

}

export const login = (username, password, firebase, redirectToMainWhenLogin) => async (dispatch, getState) => {
  dispatch(loginLoading())

  try {
    const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ login: username, password })
    }

    const response = await fetch(`${_baseApi}/login/`, options)

    const data = await response.json()

    console.log("Data", data)
    console.log("Response", response)

    if (response.ok){
      await firebase.auth().signInWithEmailAndPassword('admin@gmail.com', 'qwerty')
      console.log("Are you working?")

      dispatch(loginSuccess(data.data[0], data.token))
      redirectToMainWhenLogin()
    } else {
      dispatch(loginFail(data?.detail[0] || ERRORS.LOGIN_FAIL_ERROR))
    }
  } catch (e) {
    dispatch(loginFail(ERRORS.NETWORK_OR_SYNTAX_ERROR))
  }

}

export const loginLoading = () => ({ type: LOGIN_LOADING })
export const loginSuccess = (user, token) => ({ type: LOGIN_SUCCESS, payload: {user, token} })
export const loginFail = error => ({ type: LOGIN_FAIL, payload: error })

export const userLoading = () => ({ type: USER_LOADING })
export const userSuccess = (user, token) => ({ type: USER_SUCCESS, payload: {user, token} })
export const userFail = error => ({ type: USER_FAIL, payload: error })

export const logout = () => ({ type: LOGOUT })

export const clearError = () => ({ type: CLEAR_ERROR })
