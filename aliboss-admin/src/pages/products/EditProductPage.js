import React, {useContext, useEffect, useState} from 'react'
import { useParams } from 'react-router-dom'
import ServerServiceContext from "../../contexts/ServerServiceContext"
import WithBgSpinner from "../../components/spinners/WithBgSpinner";
import ProductForm from "../../components/products/ProductForm";

function EditProductPage(props) {

  const { productId } = useParams()
  const serverService = useContext(ServerServiceContext)

  const [product, setProduct] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchProducts = async () => {
      setIsLoading(true)
      const result = await serverService.updateProduct(productId)
      if (!result.hasError){
        setProduct(result.data)
      } else {
        setError(result.data.detail)
      }
      setIsLoading(false)
    }

    fetchProducts().then(() => {})
  }, [productId])

  return (
    <>
      { isLoading ? <WithBgSpinner/> : product && <ProductForm product={product} isEdit /> }
      { error && <h4 className="d-flex justify-content-center vh-100 align-items-center text-danger">{ error }</h4> }
    </>
  )
}

export default EditProductPage
