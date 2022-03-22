import React, {useCallback, useState} from 'react'
import { Link } from 'react-router-dom'
import {
  CButton,
  CCard,
  CCardBody,
  CCardGroup,
  CCol,
  CContainer,
  CForm,
  CInput,
  CInputGroup,
  CInputGroupPrepend,
  CInputGroupText,
  CRow
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import {useDispatch, useSelector} from "react-redux"
import MiniSpinner from "../../components/spinners/MiniSpinner"
import {login} from "../../redux/actions/authActions"
import {useFirebase} from "react-redux-firebase"
import {useHistory} from 'react-router-dom'

const LoginPage = () => {

  const firebase = useFirebase()
  const history = useHistory()
  const dispatch = useDispatch()
  const auth = useSelector(state => state.auth)

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const onLogin = useCallback(() => {
    dispatch(login(username, password, firebase, redirectToMainWhenLogin))
  }, [username, password])

  const redirectToMainWhenLogin = useCallback(() => {
    history.push('/')
  }, [])

  return (
    <div className="c-app c-default-layout flex-row align-items-center">
      <CContainer>
        <CRow className="justify-content-center">
          <CCol md="8">
            <CCardGroup>
              <CCard className="p-4">
                <CCardBody>
                  <CForm>
                    <h1>Логин</h1>
                    <p className="text-muted">Вход в аккаунт</p>
                    <CInputGroup className="mb-3">
                      <CInputGroupPrepend>
                        <CInputGroupText>
                          <CIcon name="cil-user" />
                        </CInputGroupText>
                      </CInputGroupPrepend>
                      <CInput
                        type="text"
                        placeholder="Имя пользователя"
                        autoComplete="username"
                        value={username}
                        onChange={e => setUsername(e.target.value)}
                      />
                    </CInputGroup>
                    <CInputGroup className="mb-4">
                      <CInputGroupPrepend>
                        <CInputGroupText>
                          <CIcon name="cil-lock-locked" />
                        </CInputGroupText>
                      </CInputGroupPrepend>
                      <CInput
                        type="password"
                        placeholder="Пароль"
                        autoComplete="new-password"
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                      />
                    </CInputGroup>
                    <CRow>
                      <CCol xs="6">
                        <CButton color="primary" className="px-4" onClick={onLogin}>
                          { auth.isLoginLoading ? <MiniSpinner/> : 'Вход' }
                        </CButton>
                      </CCol>
                      <CCol md={12} className="text-danger mt-3">
                        { auth.error }
                      </CCol>
                    </CRow>
                  </CForm>
                </CCardBody>
              </CCard>
              <CCard className="text-white bg-primary py-5 d-md-down-none" style={{ width: '44%' }}>
                <CCardBody className="text-center">
                  <div className="mt-5">
                    <h2>Панель управления</h2>
                    <p>Добро пожаловать в панель управления AliBoss</p>
                  </div>
                </CCardBody>
              </CCard>
            </CCardGroup>
          </CCol>
        </CRow>
      </CContainer>
    </div>
  )
}

export default LoginPage
