import React from "react"
import { Route, Redirect } from "react-router-dom"
import { useSelector } from "react-redux"
import { isLoaded, isEmpty } from "react-redux-firebase"

import TheSidebar from "./TheSidebar"
import TheHeader from "./TheHeader"

const PrivateRoute = ({ children, ...remainingProps }) => {

  const isAuthenticated = useSelector(state => state.auth.isAuth)
  const firebaseAuth = useSelector(state => state.firebase.auth)

  return (
    <Route
      {...remainingProps}
      render={({ location }) =>
        isLoaded(firebaseAuth) && !isEmpty(firebaseAuth) && isAuthenticated ? (
            <div className="c-app c-default-layout">
              <TheSidebar/>
              <div className="c-wrapper">
                <TheHeader/>
                <div className="c-body">
                  { children }
                </div>
              </div>
            </div>
        ) : (
          <Redirect
            to={{
              pathname: '/login',
              state: { from: location },
            }}
          />
        )
      }
    />
  )
}

export default PrivateRoute
