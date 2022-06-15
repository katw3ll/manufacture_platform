import { useState, useEffect } from 'react';
import 'antd/dist/antd.css';
import {Route, Routes, useNavigate} from 'react-router-dom';
import { Modal, Button } from 'antd';
import OrdersPage  from '../../pages/OrdersPage';
import ComplectPage from '../../pages/ComplectationPage';
import Queue from '../../pages/Queue';
import NavMenu from '../../components/NavMenu/NavMenu';
import StorePage from '../../pages/StorePage/StorePage';
import api from '../../api/api';
import Assemble from '../../pages/Assemble';


const ModalSwitch = ({
    currentUser
}) => {
  const [currentOrder, setCurrentOrder] = useState({});
  const [selectedOrders, setSelectedOrders] = useState([]);
  const [isOpenPopupCreateOrder, setIsOpenPopupCreateOrder] = useState(false)

  const onSetOrder = (order) => {
    setCurrentOrder(order);
  }

  const onSetSelectedOrder = (items) => {
    setSelectedOrders(items)
  }

  const handleOpenPopupCreateOrder = () => {
    setIsOpenPopupCreateOrder(true)
  }

  const [isOpenedPopup, setIsOpenedPopup] = useState(false);

  const handleOpenPopup = () => {
    setIsOpenedPopup(true);
  }

  const handleClosePopup = () => {
    setIsOpenedPopup(false);
    setIsOpenPopupCreateOrder(false);
    setCurrentOrder({})
  }

  const getOrdersIds = () => {
    const actorIds = [];
    selectedOrders.forEach(item => actorIds.push(item.id))
    return actorIds
  }

  return (
    <div className="App">
      <NavMenu />
      <div style={{width: '100%', padding: '0 20px'}}>
        <Routes>
          <Route
            path="orders"
            element={
              <OrdersPage
                onSetCurrentOrder={onSetOrder}
                onOpen={handleOpenPopup}
                onSetSelectedOrder={onSetSelectedOrder}
                onOpenPopupCreateNewOrder={handleOpenPopupCreateOrder}
              />
            } />
          {/* </Route> */}
            <Route path='complect' element={<ComplectPage selectedOrders={selectedOrders} getOrdersIds={getOrdersIds} />} />
            <Route path='store' element={<StorePage  />} />
            <Route path='queue' element={<Queue  />} />
            <Route path='assemble' element={
              <Assemble
                onSetCurrentOrder={onSetOrder}
                onSetSelectedOrder={onSetSelectedOrder}
                getOrdersIds={getOrdersIds}
              />}
            />
        </Routes>
      </div>
      <Modal title="Новый заказ" visible={isOpenPopupCreateOrder}  okText="Закрыть" cancelText="Редактировать" closable={false} onOk={handleClosePopup}>
        <h2>{currentOrder.orderNumber}</h2>
        {currentOrder !== {} && currentOrder.orderSpecification && currentOrder.orderSpecification.map((item, i) => (
          <div key={i} style={{display: 'flex'}}>
            <p>{item.name}</p>
            <span>{item.count}</span>
          </div>
        ))}
      </Modal>
    </div>
  );
}

export default ModalSwitch;
