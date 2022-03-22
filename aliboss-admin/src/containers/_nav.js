import React from 'react'
import CIcon from '@coreui/icons-react'

const _nav =  [
  {
    _tag: 'CSidebarNavItem',
    name: 'Заказы',
    to: '/orders',
    icon: <CIcon name="cil-speedometer" customClasses="c-sidebar-nav-icon"/>,
    badge: {
      color: 'warning',
      text: '',
    }
  },
  {
    _tag: 'CSidebarNavDropdown',
    name: 'Товары',
    route: '/products',
    icon: 'cil-puzzle',
    _children: [
      {
        _tag: 'CSidebarNavItem',
        name: 'Новый товар',
        to: '/products/create',
      },
      {
        _tag: 'CSidebarNavItem',
        name: 'Список товаров',
        to: '/products',
      },
    ],
  },
]

export default _nav
