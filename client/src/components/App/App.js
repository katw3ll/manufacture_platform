import { useState, useEffect } from 'react';
import 'antd/dist/antd.css';
import {Route, Routes, useNavigate} from 'react-router-dom';
import { Modal, Button } from 'antd';
import OrdersPage  from '../../pages/OrdersPage';
import ComplectPage from '../../pages/ComplectationPage';
import NavMenu from '../../components/NavMenu/NavMenu';
import StorePage from '../../pages/StorePage/StorePage';
import Assemble from '../../pages/Assemble';
import Queue from '../../pages/Queue';
import api from '../../api/api';
import ModalSwitch from '../ModalSwitch/ModalSwitch';
import LoginPage from '../../pages/LoginPage/LoginPage';
import './App.css';

function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [isLogedin, setIsLogedin] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();
  const [currentOrder, setCurrentOrder] = useState({});
  const [selectedOrders, setSelectedOrders] = useState([]);
  const [isOpenPopupCreateOrder, setIsOpenPopupCreateOrder] = useState(false)

  const handleOpenPopupCreateOrder = () => {
    setIsOpenPopupCreateOrder(true)
  }

  const onSetOrder = (order) => {
    setCurrentOrder(order);
  }

  const onSetSelectedOrder = (items) => {
    setSelectedOrders(items)
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

  const createNewOrder = () => {

  }

const onLogin = () => {
  api
    .auth()
    .then((res) => {
      console.log(res)
      localStorage.setItem('jwt', res.token);
      // localStorage.setItem('refresh', res.refreshToken)
      // setCurrentUser(res);
      navigate('/orders');
      setIsLogedin(true)
      //res.isAdmin ? history.push('/users') : history.push('/me');
    })
    .catch((err) => console.log(err));
}
  const checkToken = () => {
    const jwt = localStorage.getItem('jwt');
    console.log(jwt)
    if (jwt) {
      setIsLogedin(true)
      // api.getCurrentUser()
      // .then(res => {
      //   console.log(res);
      //   setCurrentUser(res);
      //   setIsLogedin(true);
      //   navigate('/orders');
      // })
    // .catch(err => {
    //   console.log(err);
    //   navigate('/sign-in');
    // })
    // .finally(() => setIsLoading(false))
    } else {
      setIsLogedin(false);
      localStorage.removeItem('jwt');
      setIsLoading(false)
      navigate('/sign-in');
    }
      // api.getCurrentUser()
      //   .then(res => {
      //     setCurrentUser(res);
      //     setIsLogedin(true);
      //     navigate('/orders');
      //   })
      // .catch(err => {
      //   console.log(err);
      //   navigate('/sign-in');
      // })
      // .finally(() => setIsLoading(false))
  }

  useEffect(() => {
    checkToken()
  }, [])


  return (
    <div className="App">
      <Routes>
        <Route
          path='/'
          element={<ModalSwitch currentUser={currentUser} />}
        >
          <Route
            path="orders"
            element={
            <OrdersPage
              onSetCurrentOrder={onSetOrder}
              onOpen={handleOpenPopup}
              onSetSelectedOrder={onSetSelectedOrder}
              onOpenPopupCreateNewOrder={handleOpenPopupCreateOrder}
            />}
          />
          <Route path='store' element={<StorePage  />} />
          <Route path='complect' element={<ComplectPage selectedOrders={selectedOrders} getOrdersIds={getOrdersIds} />} />
          <Route path='queue' element={<Queue  />} />
          <Route path='assemble' element={<Assemble getOrdersIds={getOrdersIds} />} />
        </Route>
        <Route path='/sign-in' element={<LoginPage onSubmit={onLogin} />} />
      </Routes>
    </div>
  );
}

export default App;
