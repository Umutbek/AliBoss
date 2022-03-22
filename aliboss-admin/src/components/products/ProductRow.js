import React, {useCallback, useContext, useEffect, useState} from 'react'
import NoPhoto from "../../assets/images/no-photo.jpg"
import {CButton, CFormGroup, CInput} from "@coreui/react"
import EditIcon from "../../assets/icons/free-icon-edit.svg"
import DeleteIcon from "../../assets/icons/free-icon-delete.svg"
import {Link} from "react-router-dom";
import ServerServiceContext from "../../contexts/ServerServiceContext"
import MiniSpinner from "../spinners/MiniSpinner";

function ProductRow({ product, number, onDelete, fetchProducts }) {

  const serverService = useContext(ServerServiceContext)

  const [cost, setCost] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [success, setSuccess] = useState(true)

  useEffect(() => { setCost(product.cost) }, [product])

  useEffect(() => {
    if (product.cost.toString() === cost.toString()){
      setSuccess(true)
    } else {
      setSuccess(false)
    }
  }, [cost])

  const updateCost = useCallback(async () => {
    setIsLoading(true)
    const result = await serverService.updateProduct(product.id, {cost: cost.toString().length ? cost : null})
    if (!result.hasError){
      setSuccess(true)
    } else {
      setSuccess(false)
    }

    fetchProducts()
    setIsLoading(false)
  }, [cost, product])

  const keyPressHandler = e => {
    if (e.code === 'Enter'){
      updateCost().then(() => {})
    }
  }

  return (
    <tr key={product.id}>
      <th scope="row" style={{ width: '5%' }}>{ number }</th>
      <td style={{ width: '53%' }}>{ product.name }</td>
      <td style={{ width: '8%', padding: 0 }}>
        <div style={{ width: 50 }}>
          <img
            src={product.imagelink || NoPhoto}
            alt=""
            style={{ width: '100%', height: '100%' }}
          />
        </div>
      </td>
      <td style={{ width: '8%'}}>
            {product.cost}
      </td>

      <td style={{ width: '12$' }}>
        <div className="d-flex justify-content-around">
          <Link to={`/products/edit/${product.id}`} style={{width: "20px"}}>
            <img src={EditIcon} alt="" width="100%" height="100%"/>
          </Link>
          <a onClick={e => { e.preventDefault(); onDelete(product) }} style={{width: "20px", cursor: 'pointer'}}>
            <img src={DeleteIcon} alt="" width="100%" height="100%"/>
          </a>
        </div>
      </td>
    </tr>
  );
}

export default ProductRow
