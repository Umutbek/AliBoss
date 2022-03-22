import React, {useCallback} from 'react'
import {
  CBadge,
  CDropdown,
  CDropdownItem,
  CDropdownMenu,
  CDropdownToggle,
  CImg
} from '@coreui/react'
import CIcon from "@coreui/icons-react"
import {useDispatch, useSelector} from "react-redux"
import {logout} from "../redux/actions/authActions"
import {useFirebase} from "react-redux-firebase"
import {useHistory} from 'react-router-dom'

const TheHeaderDropdown = () => {

  const firebase = useFirebase()
  const dispatch = useDispatch()
  const history = useHistory()
  const user = useSelector(state => state.auth.user)

  const logoutHandler = useCallback(async () => {
    await firebase.logout()
    dispatch(logout())
  }, [])

  const avatar = "http://176.126.166.63" + user.avatar

  return (
    <CDropdown
      inNav
      className="c-header-nav-items mx-2"
      direction="down"
    >
      <CDropdownToggle className="c-header-nav-link" caret={false}>
        <div className="c-avatar" style={{ background: '#0288D1', color: '#fff', fontSize: 22 }}>
          { user.avatar ?
            <CImg
              src={avatar}
              className="c-avatar-img"
              alt="user-profile-avatar"
            /> :  user.login ? user.login[0] : ''
          }
        </div>
        <div className="ml-3">{ user.login }
          <span className="ml-1">
            <svg width={18} height={18} version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 129 129" xmlnsXlink="http://www.w3.org/1999/xlink" enableBackground="new 0 0 129 129">
              <g>
                <path d="m121.3,34.6c-1.6-1.6-4.2-1.6-5.8,0l-51,51.1-51.1-51.1c-1.6-1.6-4.2-1.6-5.8,0-1.6,1.6-1.6,4.2 0,5.8l53.9,53.9c0.8,0.8 1.8,1.2 2.9,1.2 1,0 2.1-0.4 2.9-1.2l53.9-53.9c1.7-1.6 1.7-4.2 0.1-5.8z"/>
              </g>
            </svg>
          </span>
        </div>
      </CDropdownToggle>
      <CDropdownMenu className="pt-0" placement="bottom-end">
        <CDropdownItem
          header
          tag="div"
          color="light"
          className="text-center"
        >
          <strong>Аккаунт</strong>
        </CDropdownItem>
        {
          (user.type === 3) && <CDropdownItem onClick={() => history.push(`/profile/${user.id}`)}>
            <CIcon name="cil-user" className="mr-1"/>
            Профиль
          </CDropdownItem>
        }
        <CDropdownItem onClick={logoutHandler}>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" className="c-icon c-icon-sm mfe-2" role="img">
            <polygon fill="var(--ci-primary-color, currentColor)"
                     points="77.155 272.034 351.75 272.034 351.75 272.033 351.75 240.034 351.75 240.033 77.155 240.033 152.208 164.98 152.208 164.98 152.208 164.979 129.58 142.353 15.899 256.033 15.9 256.034 15.899 256.034 129.58 369.715 152.208 347.088 152.208 347.087 152.208 347.087 77.155 272.034"
                     className="ci-primary"
            />
            <polygon fill="var(--ci-primary-color, currentColor)"
                     points="160 16 160 48 464 48 464 464 160 464 160 496 496 496 496 16 160 16"
                     className="ci-primary"
            />
          </svg>
          Выход
        </CDropdownItem>
      </CDropdownMenu>
    </CDropdown>
  )
}

export default TheHeaderDropdown
