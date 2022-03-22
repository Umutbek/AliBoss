import React, {Suspense, lazy} from "react"
import {Redirect, Route, Switch} from "react-router-dom"
import PrivateRoute from "../containers/PrivateRoute"
import WithBgSpinner from "../components/spinners/WithBgSpinner"

const LoginPage = lazy(() => import('./auth/LoginPage'))
const Page404 = lazy(() => import('./Page404'))
const OrdersPage = lazy(() => import('./orders/OrdersPage'))
const ProductListPage = lazy(() => import('./products/ProductListPage'))
const CreateProductPage = lazy(() => import('./products/CreateProductPage'))
const EditProductPage = lazy(() => import('./products/EditProductPage'))

export default function Router(){
  return (
    <Suspense fallback={<WithBgSpinner/>}>
      <Switch>
        <Route exact path="/auth/login">
          <LoginPage/>
        </Route>
        <PrivateRoute exact path="/orders">
          <OrdersPage/>
        </PrivateRoute>
        <PrivateRoute exact path="/products">
          <ProductListPage/>
        </PrivateRoute>
        <PrivateRoute exact path="/products/create">
          <CreateProductPage/>
        </PrivateRoute>
        <PrivateRoute exact path="/products/edit/:productId">
          <EditProductPage/>
        </PrivateRoute>
        <Route exact path="/login">
          <Redirect to="/auth/login" />
        </Route>
        <Route exact path="/">
          <Redirect to="/orders" />
        </Route>
        <Route>
          <Page404/>
        </Route>
      </Switch>
    </Suspense>
  )
}
