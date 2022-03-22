import React from "react"
import {BrowserRouter} from "react-router-dom"
import ServerServiceContext from "./contexts/ServerServiceContext"
import ServerService from "./services/ServerService"
import {Provider} from "react-redux"
import store from "./redux/store"

import {ReactReduxFirebaseProvider} from "react-redux-firebase"
import firebase from "firebase"
import {createFirestoreInstance} from "redux-firestore"
import "firebase/auth"
import "firebase/firestore"

const firebaseConfig = {
  apiKey: process.env.REACT_APP_API_KEY,
  authDomain: process.env.REACT_APP_AUTH_DOMAIN,
  projectId: process.env.REACT_APP_PROJECT_ID,
  storageBucket: process.env.REACT_APP_STORAGE_BUCKET,
  messagingSenderId: process.env.REACT_APP_MESSAGING_SENDER_ID,
  appId: process.env.REACT_APP_APP_ID,
  measurementId: process.env.REACT_APP_MEASUREMENT_ID
}

const rrfConfig = {
  userProfile: "users",
  useFirestoreForProfile: true,
}

firebase.initializeApp(firebaseConfig)
firebase.firestore()

const rrfProps = {
  firebase,
  config: rrfConfig,
  dispatch: store.dispatch,
  createFirestoreInstance, //since we are using Firestore
}

export default function Providers({children}){
  return (
    <BrowserRouter>
      <ReactReduxFirebaseProvider {...rrfProps}>
        <ServerServiceContext.Provider value={new ServerService()}>
            <Provider store={store}>
              { children }
            </Provider>
        </ServerServiceContext.Provider>
      </ReactReduxFirebaseProvider>
    </BrowserRouter>
  )
}
