import React, {useCallback, useContext, useEffect, useState} from 'react'
import {
  CCard,
  CCardFooter,
  CCardBody,
  CCardHeader,
  CPagination,
  CFormGroup,
  CCol,
  CRow,
  CLabel,
  CInput,
  CButton,
  CModal,
  CModalFooter,
  CModalBody
} from "@coreui/react"
import ServerServiceContext from "../../contexts/ServerServiceContext"
import {useQuery} from "../../helpers/hooks"
import FullContentSpinner from "../../components/spinners/FullContentSpinner"
import ProductRow from "../../components/products/ProductRow"
import {Link, useHistory} from "react-router-dom"
import {ScrollToTopController} from "../../containers/ScrollToTopController"
import {toast} from "react-toastify";
import WithBgSpinner from "../../components/spinners/WithBgSpinner";
import {useSelector} from "react-redux"




function ProductListPage(props) {

  const query = useQuery()
  const page = parseInt(query.get("page")) || 1
  const search = query.get("search") || ''

  const serverService = useContext(ServerServiceContext)
  const history = useHistory()

  const [isProductsLoading, setIsProductsLoading] = useState(false)
  const [products, setProducts] = useState([])
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const [searchText, setSearchText] = useState('')
  const [activePage, setActivePage] = useState(1)
  const [pagesCount, setPagesCount] = useState(1)

  const [deleteModal, setDeleteModal] = useState(false)
  const [selectedProduct, setSelectedProduct] = useState(null)
  const {user} = useSelector(state => state.auth)


  const fetchProducts = useCallback(async () => {
    let params = ''
    page && (params += `?page=${page}&supplier=${user.id}`)
    search && (params += `&search=${search}`)

    const result = await serverService.getProducts(params)

    if (!result.hasError){
      setProducts(result.data.results)
      setPagesCount(Math.trunc(parseInt(result.data.count) / 20) + 1)
    } else {
      setError(result.data.detail)
    }

    setIsProductsLoading(false)
  }, [page, search])

  useEffect(() => {
    setIsProductsLoading(true)
    fetchProducts().then(() => {})
  }, [page, search])

  useEffect(() => pushToUrl(activePage, searchText), [activePage])

  useEffect(() => pushToUrl(1, searchText), [searchText])

  const pushToUrl = useCallback((currPage, text) => {
    let path = `/products/?page=${currPage}`
    if (text){
      path += `&search=${text}`
    }
    history.push(path)
  }, [])

  const onOpenDeleteModal = useCallback(prod => {
    setSelectedProduct(prod)
    setDeleteModal(true)
  }, [])

  const onCloseDeleteModal = useCallback(() => {
    setDeleteModal(false)
    setSelectedProduct(null)
  }, [])

  const onConfirmDelete = useCallback(async () => {
    setIsLoading(true)
    const result = await serverService.deleteProduct(selectedProduct.id)

    if (!result.hasError){
      fetchProducts().then(() => {})
      onCloseDeleteModal()
      toast.warn(`Product ${selectedProduct.name} successfully deleted.`)
    } else {
      console.log("Selected id", selectedProduct.id)
      fetchProducts().then(() => {})
      onCloseDeleteModal()
      toast.warn(`Product ${selectedProduct.name} успешно удалено.`)

    }

    setIsLoading(false)
  }, [selectedProduct])

  return (
    <>
      <ScrollToTopController/>
      <CCard className="m-3">
        <CCardBody>
          <h3 className="mb-4">Список товаров</h3>
          <Link to="/products/create" className="float-right btn btn-twitter">Новый товар</Link>
          <CFormGroup row>
            <CCol md={6}>
              <CRow>
                <CCol md={10}>
                  <CInput
                    placeholder="Поиск..."
                    value={searchText}
                    onChange={e => setSearchText(e.target.value)}
                    name="search-text"
                    autoComplete="search-text"
                  />
                </CCol>
              </CRow>
            </CCol>
          </CFormGroup>
          {
            isProductsLoading ? <FullContentSpinner/> :
              <table className="table">
                <thead>
                <tr>
                  <th scope="col">#</th>
                  <th scope="col">Название</th>
                  <th scope="col">Фото</th>
                  <th scope="col">Цена</th>
                  <th scope="col"/>
                </tr>
                </thead>
                <tbody>
                { products.map((p, index) => (
                  <ProductRow key={p.id} product={p} number={(index + 1) + (20 * (page - 1))} onDelete={onOpenDeleteModal} />
                )) }
                </tbody>
              </table>
          }
        </CCardBody>
        <CCardFooter>
          <div className={'mt-2'} >
            <CPagination
              activePage={activePage}
              pages={pagesCount}
              onActivePageChange={i => setActivePage(i)}
            />
          </div>
        </CCardFooter>
      </CCard>
      <CModal
        show={deleteModal}
        onClose={onCloseDeleteModal}
        centered
      >
        <CModalBody>
          Вы уверены что хотите удалить товар? <br/>
          "{ selectedProduct?.name }" ?
        </CModalBody>
        <CModalFooter>
          <CButton color="danger" onClick={onConfirmDelete}>
            Удалить
          </CButton>
          <CButton color="secondary" onClick={onCloseDeleteModal}>
            Отмена
          </CButton>
        </CModalFooter>
      </CModal>
      { isLoading && <WithBgSpinner/> }
    </>
  )
}

export default ProductListPage
