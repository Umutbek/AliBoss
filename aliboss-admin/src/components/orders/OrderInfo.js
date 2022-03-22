import React from 'react'
import {CCol, CFormGroup, CInput, CLabel, CRow, CTextarea} from "@coreui/react"
import {toNormalDate} from "../../helpers/time"
import {statuses} from "../../constants/orders"
import FullContentSpinner from "../spinners/FullContentSpinner"
import MiniSpinner from "../spinners/MiniSpinner";

function OrderInfo({ selectedOrder, orderItems, isItemsLoading }) {


  return (
    <>
      <CRow>
        {/*first column*/}
        <CCol md={4} xs={12}>
          <CFormGroup>
            <CLabel>Телефон номер</CLabel>
            <CInput
              value={selectedOrder.phone}
              disabled
              className="bg-white text-black-80"
            />
          </CFormGroup>
          <CFormGroup>
            <CLabel>Order Date</CLabel>
            <CInput
              value={toNormalDate(selectedOrder.date.seconds, 'Сегодня', 'Вчера')}
              disabled
              className="bg-white text-black-80"
            />
          </CFormGroup>
          <CFormGroup>
            <CLabel>Клиент</CLabel>
            <CInput
              value={selectedOrder.user}
              disabled
              className="bg-white text-black-80"
            />
          </CFormGroup>
        </CCol>
        {/*second column*/}
        <CCol md={4} xs={12}>
          <CFormGroup>
            <CLabel>Номер заказа</CLabel>
            <CInput
              value={parseFloat(selectedOrder.id)}
              disabled
              className="bg-white text-black-80"
            />
          </CFormGroup>
          <CFormGroup>
            <CLabel>Общая сумма</CLabel>
            <CInput
              value={parseFloat(selectedOrder.totalCost).toFixed(2)}
              disabled
              className="bg-white text-black-80"
            />
          </CFormGroup>

          { ((selectedOrder.status === statuses.DECLINED) && selectedOrder.declineReason) &&
          <CFormGroup>
            <CLabel>Причина отказа</CLabel>
            <CTextarea
              value={selectedOrder.declinereason}
              rows={3}
              disabled
              className="bg-white text-black-80"
            />
          </CFormGroup>
          }
        </CCol>
        {/*third column*/}
        <CCol md={4} xs={12}>
          <CFormGroup>
            <CLabel>Адресс</CLabel>
            <CInput
              value={selectedOrder.address}
              disabled
              className="bg-white text-black-80"
            />
          </CFormGroup>
        </CCol>
      </CRow>
      <h4 className="my-2">Товары</h4>

      {
        isItemsLoading ? <MiniSpinner center/> :
          <table className="table">
            <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Название товара</th>
              <th scope="col">Цена</th>
              <th scope="col">Количество</th>
              <th scope="col">Общая сумма</th>

            </tr>
            </thead>
            <tbody>
            { orderItems.map((item, index) => (
              <tr key={item.id}>
                <th scope="row">{ index + 1 }</th>
                <td>{ item.item.name }</td>
                <td>{ item.item.cost }</td>
                <td>{ item.quantity }</td>
                <td>{ item.quantity * item.item.cost }</td>
              </tr>
            )) }
            </tbody>
          </table>
      }
    </>
  )
}

export default OrderInfo
