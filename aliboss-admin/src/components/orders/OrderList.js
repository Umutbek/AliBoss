import React, {useCallback, useContext, useEffect, useState} from 'react'
import {
  CDataTable,
  CBadge,
  CButton,
  CModal,
  CModalBody,
  CModalFooter,
  CModalHeader,
  CTextarea
} from "@coreui/react"
import {useSelector} from "react-redux"
import FullContentSpinner from "../spinners/FullContentSpinner"
import {statuses} from "../../constants/orders"
import {toNormalDate} from "../../helpers/time"
import {useFirestore} from "react-redux-firebase"
import ServerServiceContext from "../../contexts/ServerServiceContext"
import WithBgSpinner from "../spinners/WithBgSpinner"
import OrderInfo from "./OrderInfo"
import {toast} from "react-toastify"

function OrdersList({ status = 'all' }) {

  const firestore = useFirestore()
  const userId = useSelector(state => state.auth.user.id)
  const serverService = useContext(ServerServiceContext)

  const {orders, isOrdersLoading} = useSelector(state => state.orders)
  const [isItemsLoading, setIsItemsLoading] = useState(false)

  const [orderItems, setOrderItems] = useState([])

  const [firestoreLoading, setFirestoreLoading] = useState(false)

  const [isOrderModalOpen, setIsOrderModalOpen] = useState(false)
  const [selectedOrder, setSelectedOrder] = useState(null)

  const openOrderModal = useCallback(async item => {

    console.log("Item", item.items[0])
    setSelectedOrder(item)
    setIsOrderModalOpen(true)
    await fetchOrderItems(userId, item)
  }, [])

  const fetchOrderItems = useCallback(async (usrId, docId) => {
    setIsItemsLoading(true)

    console.log("User Id", usrId)
    console.log("Doc ID", docId.items)

    const snapshot = await firestore.collection("stores")
      .doc(usrId.toString())
      .collection("orders")
      .doc(docId.toString())
      .get()

    setOrderItems(docId.items)
    setIsItemsLoading(false)
  }, [])

  const closeOrderModal = useCallback(() => {
    setSelectedOrder(null)
    setIsOrderModalOpen(false)
    setOrderItems([])
  }, [])

  const [declineReason, setDeclineReason] = useState('')
  const [isDeclineModalOpen, setIsDeclineModalOpen] = useState(false)

  const openDeclineModal = useCallback(() => {
    setDeclineReason('')
    setIsDeclineModalOpen(true)
  }, [])

  const closeDeclineModal = useCallback(() => setIsDeclineModalOpen(false), [])

  const updateOrderStatus = useCallback(async (userId, order, newStatus, reason = 'qwerty') => {

    closeOrderModal()

    try {
      const { hasError, data } = await serverService.updateStatus(order.id, newStatus, reason)
      if (hasError){
        toast.error('Что-то пошло не так')
      }
    }
    catch (e) {
      console.log(e)
      toast.error("Oоопс что-то пошло не так")
    }

    closeDeclineModal()
    closeOrderModal()
  }, [firestore])


  const onAccept = useCallback(async () => {
    await updateOrderStatus(userId, selectedOrder, statuses.PACKING)
  }, [selectedOrder])

  const onReady = useCallback(async () => {
    await updateOrderStatus(userId, selectedOrder, statuses.ON_WAY)
  }, [selectedOrder])

  const onDecline = useCallback(async () => {
    await updateOrderStatus(userId, selectedOrder, statuses.DECLINED, declineReason)
  }, [selectedOrder, declineReason])

  const actions = {
    onAccept,
    onReady,
    onDecline,
    openDeclineModal
  }

  const fields = [
    { key: 'index', label: '#', _style: { width: '6%'} },
    { key: 'clientName', label: 'Клиент', _style: { width: '22%'} },
    { key: 'clientAddress', label: 'Адресс', _style: { width: '30%'} },
    { key: 'status', label: 'Статус', _style: { width: '16%'} },
    { key: 'dateOrder', label: 'Дата', _style: { width: '16%'} },
    { key: 'totalCost', label: 'Общая сумма', _style: { width: '10%'} }
  ]

  const getStatusWithBadge = useCallback((statusId) => {

    console.log("Status ID", statusId)
    console.log("New", statuses.NEW)
    console.log("packing", statuses.PACKING)

    switch (statusId) {

      case statuses.NEW: return <CBadge style={{padding: '5px 10px', fontSize: 12}} color="warning">Новые</CBadge>
      case statuses.PACKING: return <CBadge style={{padding: '5px 10px', fontSize: 12}} color="primary">Упаковывается</CBadge>
      case statuses.ON_WAY: return <CBadge style={{padding: '5px 10px', fontSize: 12}} color="info">В пути</CBadge>
      case statuses.DELIVERED: return <CBadge style={{padding: '5px 10px', fontSize: 12}} color="success">Доставлено</CBadge>
      case statuses.DECLINED: return <CBadge style={{padding: '5px 10px', fontSize: 12}} color="danger">Отказано</CBadge>
      default: return 'primary'
    }
  })

  return (
    <div>
      {
        isOrdersLoading ? <FullContentSpinner/> :
          <CDataTable
            items={status === 'all' ? orders : orders.filter(o => o.status === status)}
            fields={fields}
            tableFilter={{label: 'Фильтрация', placeholder: 'Поиск...'}}
            hover
            sorter
            clickableRows
            onRowClick={item => openOrderModal(item)}
            scopedSlots = {{
              'index':
                (item, index)=>(
                  <td>
                    # { index + 1 }
                  </td>
                ),
              'clientName':
                (item)=>(
                  <td>
                    {item.clientname || item.phone }
                  </td>
                ),
              'clientAddress':
                (item)=>(
                  <td>
                    {item.address}
                  </td>
                ),
              'status':
                (item)=>(
                  <td>
                    {getStatusWithBadge(item.status)}
                  </td>
                ),
              'dateOrder':
                (item)=>(
                  <td>
                    { toNormalDate(item.date.seconds, 'Сегодня', 'Вчера') }
                  </td>
                ),
              'totalCost':
                (item)=>(
                  <td>
                    {item.totalCost} <span className="Som">Сом</span>
                  </td>
                ),
            }}
          />
      }
      {
        selectedOrder &&
        <CModal
          show={isOrderModalOpen}
          onClose={closeOrderModal}
          centered
          size="xl"
        >
          <CModalHeader closeButton>
            {/*<h6 className="d-inline-block">{ selectedOrder.clientName }</h6>*/}
            <div className="d-lg-inline-block ml-1">{ getStatusWithBadge(selectedOrder.status) }</div>
          </CModalHeader>
          <CModalBody>
            <OrderInfo selectedOrder={selectedOrder} orderItems={orderItems} isItemsLoading={isItemsLoading}/>
          </CModalBody>
          <CModalFooter>
            { getButtonsByStatus(selectedOrder.status, actions, firestoreLoading) }
          </CModalFooter>
        </CModal>
      }
      <>
        <CModal
          show={isDeclineModalOpen}
          onClose={closeDeclineModal}
          centered
        >
          <CModalHeader closeButton>
            Вы уверены что хотите отменить заказа ?
          </CModalHeader>
          <CModalBody>
            <CTextarea
              value={declineReason}
              onChange={e => setDeclineReason(e.target.value)}
              rows={4}
              placeholder="Напишите отмены заказа..."
            />
          </CModalBody>
          <CModalFooter>
            <CButton color="danger" className="px-4" onClick={onDecline}>Да</CButton>
            <CButton color="secondary" className="px-4" onClick={closeDeclineModal}>Нет</CButton>
          </CModalFooter>
        </CModal>
      </>
      <>
        { firestoreLoading && <WithBgSpinner/> }
      </>
    </div>
  )
}

const getButtonsByStatus = (status, actions) => {
  switch (status){
    case statuses.NEW:
      return (
        <>
          <CButton color="primary" onClick={() => actions.onAccept()}>
            Принять заказ
          </CButton>
          <CButton color="danger" className="ml-3" onClick={() => actions.openDeclineModal()}>
            Отменить заказ
          </CButton>
        </>
      )

    case statuses.PACKING:
      return (
        <>
          <CButton color="success" onClick={() => actions.onReady()}>
            Готово для доставки
          </CButton>
          <CButton color="danger" className="ml-3" onClick={() => actions.openDeclineModal()}>
            Отменить заказ
          </CButton>
        </>
      )

    case statuses.ON_WAY:
      return (
        <>
          <CButton color="success" onClick={() => actions.onReady()}>
            Доставлено
          </CButton>
          <CButton color="danger" className="ml-3" onClick={() => actions.openDeclineModal()}>
            Отказ заказа
          </CButton>
        </>
      )

    case statuses.DELIVERED:
      return (
        <>
        </>
      )
  }
}

export default OrdersList
