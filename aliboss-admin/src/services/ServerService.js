import {getToken} from "../helpers/store"
import {ERRORS} from "../constants/errors";
import axios from "axios"

const _baseApi = process.env.REACT_APP_BASE_API

export default class ServerService {

  getProducts = async params => {
    const options = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${getToken()}`
      }
    }
    console.log("Params", params)
    return await this._doRequestAndParse(`/core/item/${params}`, options)

  }

  createProduct = async form => {
    const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${getToken()}`
      },
      body: JSON.stringify(form)
    }

    return await this._doRequestAndParse(`/core/item/`, options)
  }

  getProduct = async id => {
    const options = {
      method: 'GET',
      headers: {
        'Authorization': `Token ${getToken()}`
      }
    }

    return await this._doRequestAndParse(`/core/item/${id}/`, options)
  }

  updateProduct = async (id, form) => {
    const options = {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${getToken()}`
      },
      body: JSON.stringify(form)
    }

    return this._doRequestAndParse(`/core/item/${id}/`, options)
  }

  deleteProduct = async id => {
    const options = {
      method: 'DELETE',
      headers: {
        'Authorization': `Token ${getToken()}`,
      }
    }

    return await this._doRequestAndParse(`/core/item/${id}/`, options)
  }

  getCategories = async () => {
    return await this._doRequestAndParse(`/category/`)
  }

  getSubCategories = async categoryId => {
    return await this._doRequestAndParse(`/subcategory/?category=${categoryId}`)
  }

  getSubSubCategories = async subCategoryId => {
    return await this._doRequestAndParse(`/subsubcategory/?subcategory=${subCategoryId}`)
  }

  updateStatus = async (id, status, declinereason) => {
    const options = {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${getToken()}`
      },
      body: JSON.stringify({status, declinereason: 'Test'})
    }

    return await this._doRequestAndParse(`/core/order/${id}/`, options)
  }

  _doRequestAndParse = async (url, options) => {
    console.log(options)

    try {
      const response = await fetch(_baseApi + url, options)
      const data = await response.json()

      if (response.ok){
        return { hasError: false, data }
      }
      return { hasError: true, data: data?.detail || ERRORS.SOMETHING_WENT_WRONG}
    } catch (e) {
      return { hasError: true, data: { detail: ERRORS.NETWORK_OR_SYNTAX_ERROR } }
    }
  }
}

export const getConfig = () => ({
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${getToken()}`
  }
})

const isRequestSuccess = status => status >= 200 && status < 300

export {_baseApi}
