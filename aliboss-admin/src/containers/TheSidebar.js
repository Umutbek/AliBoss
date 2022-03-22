import React from 'react'
import { useSelector, useDispatch } from 'react-redux'
import {
  CCreateElement,
  CSidebar,
  CSidebarBrand,
  CSidebarNav,
  CSidebarNavDivider,
  CSidebarNavTitle,
  CSidebarMinimizer,
  CSidebarNavDropdown,
  CSidebarNavItem,
} from '@coreui/react'


// sidebar nav config
import navigation from './_nav'
import {set} from "../redux/actions/settingsActions";

const TheSidebar = () => {
  const dispatch = useDispatch()
  const show = useSelector(state => state.settings.sidebarShow)

  return (
    <CSidebar
      show={show}
      onShowChange={(val) => dispatch(set(val))}
    >
      <CSidebarBrand className="d-md-down-none" to="/">
        <div className="c-sidebar-brand-full">
        <h4>AliBoss</h4>
        </div>
      </CSidebarBrand>

      <CSidebarNav>

        <CCreateElement
          items={navigation}
          components={{
            CSidebarNavDivider,
            CSidebarNavDropdown,
            CSidebarNavItem,
            CSidebarNavTitle
          }}
        />
      </CSidebarNav>
      <CSidebarMinimizer className="c-d-md-down-none"/>
    </CSidebar>
  )
}

export default React.memo(TheSidebar)