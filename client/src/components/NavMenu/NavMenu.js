import React from 'react';
import 'antd/dist/antd.css';
import { useNavigate } from 'react-router-dom';

import { Menu, Button } from 'antd';
import {
  AppstoreOutlined,
  MenuUnfoldOutlined,
  MenuFoldOutlined,
  PieChartOutlined,
  DesktopOutlined,
  ContainerOutlined,
  MailOutlined,
} from '@ant-design/icons';

function getItem(label, key, icon, children, type) {
  return {
    key,
    icon,
    children,
    label,
    type,
  };
}

const items = [
  getItem('Список проектов', 'orders'),
  getItem('Заказ материалов', 'queue'),
  getItem('Склад', 'store'),
  getItem('Выйти', 'logout')
];

const NavMenu = () => {
  const [collapsed, setCollapsed] = React.useState(false);
  const navigate = useNavigate()

  const toggleCollapsed = () => {
    setCollapsed(!collapsed);
  };

  const handleClickMenu = ({ item, key }) => {
    if (key === 'orders') navigate('/orders');
    if (key === 'queue') navigate('/queue');
    if (key === 'store') navigate('/store');
    if (key === 'logout') {
      localStorage.removeItem('jwt');
      navigate('/sign-in')
    }
  }

  return (
    <div
      style={{
        width: 256,
        height: '100vh',
        backgroundColor: '#001529',
      }}
    >

      <Menu
        defaultSelectedKeys={['1']}
        mode="inline"
        theme="dark"
        inlineCollapsed={collapsed}
        items={items}
        onClick={(e) => handleClickMenu(e)}
      />
    </div>
  );
};

export default NavMenu;
