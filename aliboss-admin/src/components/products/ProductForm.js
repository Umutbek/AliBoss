import React, {useCallback, useContext, useEffect, useState} from 'react'
import { CCard, CCardBody, CCardHeader, CCardFooter,
  CRow, CCol, CInputCheckbox,
  CInput, CLabel, CFormGroup, CTextarea, CFormText,
  CButton } from "@coreui/react"
import CIcon from "@coreui/icons-react"
import Container1000 from "../../containers/Container1000"
import {useHistory} from "react-router-dom"
import Select from "react-select"
import ImageCropper from "../ImageCropper"
import ServerServiceContext from "../../contexts/ServerServiceContext"
import {useFirebase} from "react-redux-firebase";
import {useSelector} from "react-redux";
import {toast} from "react-toastify";
import WithBgSpinner from "../spinners/WithBgSpinner";
import {ERRORS} from "../../constants/errors";
import { Checkbox } from 'react-input-checkbox';


const initialValidationErrors = {
  name: null,
  description: null,
  cost: null,
  category: null,
  costSale: null,
  phone: null,
  instagram: null,
  facebook: null,
  whatsapp: null,
  web: null,
  priority: null
}

function ProductForm({ product = null, isEdit = false }) {

  const history = useHistory()
  const serverService = useContext(ServerServiceContext)
  const firebase = useFirebase()

  const user = useSelector(state => state.auth.user)

  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const [inputs, setInputs] = useState(initialInputs)
  const [validationErrors, setValidationErrors] = useState(initialValidationErrors)
  const [photoBlob, setPhotoBlob] = useState(null)

  useEffect(() => {
    if (product){
      setInputs({
        name: product.name,
        description: product.description,
        cost: product.cost,
        costSale: product.costSale,
        phone: product.phone,
        instagram: product.instagram,
        facebook: product.facebook,
        whatsapp: product.whatsapp,
        web: product.web,
        imagelink: product.imagelink,
        priority: product.priority
      })
    }
  }, [product])

  const [currencies, setCurrencies] = useState([{ value: 'Сом', label: 'Сом' }])
  const [categories, setCategories] = useState([])
  const [subCategories, setSubCategories] = useState([])
  const [subSubCategories, setSubSubCategories] = useState([])

  const [selectedCurrency, setSelectedCurrency] = useState({ value: 'Сом', label: 'Сом' })
  const [selectedCategory, setSelectedCategory] = useState('')
  const [selectedSubCategory, setSelectedSubCategory] = useState('')
  const [selectedSubSubCategory, setSelectedSubSubCategory] = useState('')
  const [issale, setIsSale] = useState(false)
  const [isoptovik, setIsOptovik] = useState(false)



  const onIsSaleChange = useCallback(e => {
    setIsSale(e.target.checked)
    setError(null)
  }, [])

  const onIsOptovikChange = useCallback(e => {
    setIsOptovik(e.target.checked)
    setError(null)
  }, [])

  const fetchCategories = useCallback(async () => {
    const result = await serverService.getCategories()

    if (!result.hasError){
      setCategories(result.data)
    }
  }, [])

  const fetchSubCategories = useCallback(async categoryId => {
    const result = await serverService.getSubCategories(categoryId)

    if (!result.hasError){
      setSubCategories(result.data)
    }
  }, [])

  const fetchSubSubCategories = useCallback(async subCategoryId => {
    const result = await serverService.getSubSubCategories(subCategoryId)

    if (!result.hasError){
      setSubSubCategories(result.data)
    }
  }, [])

  useEffect(() => {
    fetchCategories().then(() => {})
  }, [])

  useEffect(() => {
    if (selectedCategory){
      fetchSubCategories(selectedCategory.value).then(() => {})
    }
  }, [selectedCategory])

  useEffect(() => {
    if (selectedSubCategory){
      fetchSubSubCategories(selectedSubCategory.value).then(() => {})
    }
  }, [selectedSubCategory])

  const onInputsChange = useCallback(e => {
    setInputs(state => ({ ...state, [e.target.name]: e.target.value}))
    setValidationErrors(state => ({ ...state, [e.target.name]: null }))
  }, [])


  const onSubmit = useCallback(async () => {

    setIsLoading(true)

    const { name, description, cost, phone, costSale, facebook, instagram, whatsapp, web, priority} = inputs
    const adminName = user.name

    // validation
    if (!name || !cost || !selectedCategory.value || !cost.toString().length){
      const err = { ...initialValidationErrors }
      !name && (err.name = 'Это поле не может быть пустым')
      !selectedCategory.value && (err.category = 'Выбрать категорию')
      !cost.toString().length && (err.cost = 'Это поле не может быть пустым')

      setValidationErrors(err)
      setIsLoading(false)
      window.scroll({ top: 0, left: 0, behavior: 'smooth' })
      return
    }

    let imagelink = ''

    if (photoBlob) {
      const filename = name || Date.now().toString()

      await firebase
        .storage()
        .ref()
        .child(`${adminName}/${filename}.png`)
        .put(photoBlob)

      imagelink = `https://firebasestorage.googleapis.com/v0/b/aliboss.appspot.com/o/undefined%2F${filename}.png?alt=media`
    }

    const form = {
      name,
      description,
      category: selectedCategory.value || null,
      subcategory: selectedSubCategory.value || null,
      subsubcategory: selectedSubSubCategory.value || null,
      cost: cost || null,
      costSale: costSale || 0,
      priority: priority || 0,
      phone: phone || null,
      instagram: instagram || null,
      facebook: facebook || null,
      whatsapp: whatsapp || null,
      web: web || null,
      supplier: user.id,
      imagelink: imagelink || null,
      isoptovik: isoptovik || false,
      issale: issale || false
    }

    console.log('form is: ', form)

    let result = {}

    if (isEdit){
      result = await serverService.updateProduct(product.id, form)
    } else {
      result = await serverService.createProduct(form)
    }

    if (!result.hasError){
      toast.success(isEdit ? 'Товар успешно изменен.' : 'Товар успешно добавлен.')
      history.push('/products')
    } else {
      setError(result.data.detail || ERRORS.SOMETHING_WENT_WRONG)
    }

    setIsLoading(false)
  }, [inputs, selectedCategory, selectedSubCategory, selectedSubCategory, selectedSubSubCategory, photoBlob, selectedCurrency])

  const onReset = useCallback(() => {
    if (product && isEdit){
      setInputs({
        name: product.name,
        description: product.description,
        cost: product.cost || '',
        costSale: product.costSale || '',

      })
      setPhotoBlob(null)
    } else {
      setInputs(initialInputs)
      setSelectedCategory('')
      setSelectedSubCategory('')
      setSelectedSubSubCategory('')
      setPhotoBlob(null)
    }
  }, [product])

  return (
    <>
      <Container1000>
        <CButton className="border mt-3" onClick={() => history.goBack()}>
          <CIcon name="cil-arrow-left" className="mr-1"/>
          Назад
        </CButton>
        <hr/>
        <CRow className="my-3">
          <CCol md={12}>
            <CCard>
              <CCardBody className="py-2 px-3">
                <h4> {
                    isEdit ? `Изменить товар "${product?.name}"` : `Создать товар`
                } </h4>
              </CCardBody>
            </CCard>
          </CCol>
          <CCol md={8}>
            <CCard>
              <CCardBody>
                <CFormGroup>
                  <CLabel htmlFor="pr-name">Название товара</CLabel>
                  <CInput
                    id="pr-name"
                    name="name"
                    autoComplete="pr-name"
                    value={inputs.name}
                    onChange={onInputsChange}
                    placeholder="Введите название товара..."
                    className={ validationErrors.name ? 'border-danger' : '' }
                  />
                  { validationErrors.name && <CFormText><span className="text-danger">{ validationErrors.name }</span></CFormText> }
                </CFormGroup>

                <CFormGroup>
                  <CLabel htmlFor="pr-description">Описание</CLabel>
                  <CTextarea
                    id="pr-description"
                    name="description"
                    autoComplete="pr-description"
                    value={inputs.description}
                    onChange={onInputsChange}
                    placeholder="Введите описание товара..."
                    rows={4}
                    className={ validationErrors.description ? 'border-danger' : '' }
                  />
                  { validationErrors.description && <CFormText><span className="text-danger">{ validationErrors.description }</span></CFormText> }
                </CFormGroup>
                <CFormGroup>
                  <CLabel htmlFor="pr-cost">Цена</CLabel>
                  <CInput
                    type="number"
                    id="pr-cost"
                    name="cost"
                    autoComplete="pr-cost"
                    value={inputs.cost}
                    onChange={onInputsChange}
                    placeholder="Введите цену товара..."
                    className={ validationErrors.cost ? 'border-danger' : '' }
                  />
                  { validationErrors.cost && <CFormText><span className="text-danger">{ validationErrors.cost }</span></CFormText> }
                </CFormGroup>

                <CFormGroup variant="custom-checkbox" inline>
                  <CInputCheckbox custom id="inline-checkbox2" name="inline-checkbox2" checked={issale} onChange={onIsSaleChange}/>
                  <CLabel variant="custom-checkbox" htmlFor="inline-checkbox2">Акционный товар?</CLabel>
                </CFormGroup>

                <CFormGroup>
                  <CInput
                    type="number"
                    id="pr-costSale"
                    name="costSale"
                    autoComplete="pr-costSale"
                    value={inputs.costSale}
                    onChange={onInputsChange}
                    placeholder="Введите акционную цену товара..."
                    className={ validationErrors.costSale ? 'border-danger' : '' }
                  />
                  { validationErrors.costSale && <CFormText><span className="text-danger">{ validationErrors.costSale }</span></CFormText> }
                </CFormGroup>

                <CFormGroup>
                  <CLabel htmlFor="pr-image">Фото</CLabel>
                  <ImageCropper setPhotoBlob={setPhotoBlob} id="pr-photo" />
                  {
                    !photoBlob && product?.image && <img src={product.image} width={200} alt="Product image"/>
                  }
                </CFormGroup>

                <CFormGroup>
                  <CLabel htmlFor="pr-facebook">Фейсбук</CLabel>
                  <CInput
                    id="pr-facebook"
                    name="facebook"
                    autoComplete="pr-facebook"
                    value={inputs.facebook}
                    onChange={onInputsChange}
                    placeholder="Введите ссылку на фейсбук ..."
                    className={ validationErrors.facebook ? 'border-danger' : '' }
                  />
                  { validationErrors.facebook && <CFormText><span className="text-danger">{ validationErrors.facebook }</span></CFormText> }
                </CFormGroup>

                <CFormGroup>
                  <CLabel htmlFor="pr-instagram">Инстаграм</CLabel>
                  <CInput
                    id="pr-instagram"
                    name="instagram"
                    autoComplete="pr-instagram"
                    value={inputs.instagram}
                    onChange={onInputsChange}
                    placeholder="Введите ссылку на инстаграм..."
                    className={ validationErrors.instagram ? 'border-danger' : '' }
                  />
                  { validationErrors.instagram && <CFormText><span className="text-danger">{ validationErrors.instagram }</span></CFormText> }
                </CFormGroup>

                <CFormGroup>
                  <CLabel htmlFor="pr-web">Веб</CLabel>
                  <CInput
                    id="pr-web"
                    name="web"
                    autoComplete="pr-web"
                    value={inputs.web}
                    onChange={onInputsChange}
                    placeholder="Введите ссылку на Веб ..."
                    className={ validationErrors.web ? 'border-danger' : '' }
                  />
                  { validationErrors.web && <CFormText><span className="text-danger">{ validationErrors.web }</span></CFormText> }
                </CFormGroup>

                <CFormGroup>
                  <CLabel htmlFor="pr-whatsapp">Ватсапп</CLabel>
                  <CInput
                    id="pr-whatsapp"
                    name="whatsapp"
                    autoComplete="pr-whatsapp"
                    value={inputs.whatsapp}
                    onChange={onInputsChange}
                    placeholder="Введите ссылку на Ватсапп ..."
                    className={ validationErrors.whatsapp ? 'border-danger' : '' }
                  />
                  { validationErrors.whatsapp && <CFormText><span className="text-danger">{ validationErrors.whatsapp }</span></CFormText> }
                </CFormGroup>

                <CFormGroup>
                  <CLabel htmlFor="pr-phone">Телефон номер</CLabel>
                  <CInput
                    id="pr-phone"
                    name="phone"
                    autoComplete="pr-phone"
                    value={inputs.phone}
                    onChange={onInputsChange}
                    placeholder="Введите номер ..."
                    className={ validationErrors.name ? 'border-danger' : '' }
                  />
                  { validationErrors.name && <CFormText><span className="text-danger">{ validationErrors.name }</span></CFormText> }
                </CFormGroup>

                <CFormGroup>
                  <CLabel htmlFor="pr-priority">Приоритет товара</CLabel>
                  <CInput
                    id="pr-priority"
                    type="number"
                    name="priority"
                    autoComplete="pr-priority"
                    value={inputs.priority}
                    onChange={onInputsChange}
                    placeholder="Введите приоритет товара ..."
                    className={ validationErrors.name ? 'border-danger' : '' }
                  />
                  { validationErrors.name && <CFormText><span className="text-danger">{ validationErrors.name }</span></CFormText> }
                </CFormGroup>

                <CFormGroup variant="custom-checkbox" inline>
                  <CInputCheckbox custom id="inline-checkbox" name="inline-checkbox" checked={isoptovik} onChange={onIsOptovikChange}/>
                  <CLabel variant="custom-checkbox" htmlFor="inline-checkbox">Оптовый товар?</CLabel>
                </CFormGroup>

              </CCardBody>
            </CCard>
          </CCol>
          <CCol md={4}>
            <CCard>
              <CCardBody>
                <CFormGroup>
                  <CLabel>Категория</CLabel>
                  <Select
                    options={categories.map(c => ({ value: c.id, label: c.nameRus }))}
                    value={selectedCategory}
                    onChange={val => {
                      setSelectedCategory(val)
                      setValidationErrors(state => ({ ...state, category: null }))
                    }}
                    className={validationErrors.category ? 'border-danger' : ''}
                  />
                  { validationErrors.category && <CFormText><span className="text-danger">{ validationErrors.category }</span></CFormText> }
                </CFormGroup>
                <CFormGroup>
                  <CLabel>Подкатегория</CLabel>
                  <Select
                    options={subCategories.map(c => ({ value: c.id, label: c.nameRus }))}
                    value={selectedSubCategory}
                    onChange={val => setSelectedSubCategory(val)}
                  />
                </CFormGroup>
                <CFormGroup>
                  <CLabel>Субподкатегория</CLabel>
                  <Select
                    options={subSubCategories.map(c => ({ value: c.id, label: c.nameRus }))}
                    value={selectedSubSubCategory}
                    onChange={val => setSelectedSubSubCategory(val)}
                  />
                </CFormGroup>
              </CCardBody>
            </CCard>
          </CCol>
        </CRow>
        <hr/>
        <div className="d-flex justify-content-between mb-5">
          <CButton color="secondary" onClick={onReset}>Сброс</CButton>
          <h5 className="text-danger">{ error }</h5>
          { isEdit ? <CButton color="success" onClick={onSubmit}>Изменить</CButton> : <CButton color="success" onClick={onSubmit}>Создать</CButton> }
        </div>
      </Container1000>
      { isLoading && <WithBgSpinner/> }
    </>
  )
}

export default ProductForm

const initialInputs = {
  name: '',
  description: '',
  cost: '',
  costSale: '',
  phone: '',
  instagram: '',
  facebook: '',
  whatsapp: '',
  web: '',
  priority: ''
}
