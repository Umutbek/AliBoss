import React from 'react'
import ProductForm from "../../components/products/ProductForm";
import {ScrollToTopController} from "../../containers/ScrollToTopController";

function CreateProductPage(props) {
  return (
    <>
      <ScrollToTopController/>
      <ProductForm />
    </>
  )
}

export default CreateProductPage
