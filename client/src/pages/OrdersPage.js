import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import 'antd/dist/antd.css';
import InfoHoverPopup from '../components/InfoHoverPopup';
import { Table, Button, Typography, Modal, Input } from 'antd';
import api from '../api/api';

const { Title } = Typography;
const columns = [
    {
      title: 'Номер заказа',
      dataIndex: 'id',
    },
    {
      title: 'Дата поступления',
      dataIndex: 'receipt_date',
    },
    {
      title: 'Статус',
      dataIndex: 'status_name',
    },
    {
      title: 'Дедлайн',
      dataIndex: 'deadline_date',
    },
    {
      title: 'Количество',
      dataIndex: 'count_rollets',
    },
  ];

const OrdersPage = ({onSetCurrentOrder, onOpen, onSetSelectedOrder, }) => {
  const [data, setData] = useState()
  const [selectedRows, setSelectedRows] = useState([]);
  const [createProjectPopup, setCreateProjectPopup] = useState(false);
  const [deleteProjectPopup, setDeleteProjectPopup] = useState(false);
  const [downloadFile, setDownloadFile] = useState({});
  const [rowPopup, setRowPopup] = useState(false);
  const [rowPopupPosition, setRowPopupPosition] = useState({});
  const [rowData, setRowData] = useState({});
  const navigate = useNavigate()

  const handleFocusRow = (rowData) => {
    setRowData(rowData);
    const openPopup = () => {
      setRowPopup(true);
    };
    setTimeout(openPopup, 500);
  };

  const handleBlurRow = () => {
    const closePopup = () => {
      setRowPopup(false);
    };
    closePopup();
    setTimeout(closePopup, 500);
  };

  const openCreateProjectPopup = () => {
    setCreateProjectPopup(true);
  };

  const closeCreateProjectPopup = () => {
    setCreateProjectPopup(false);
    setDownloadFile({});
  };

  const openDeleteProjectPopup = () => {
    setDeleteProjectPopup(true);
  };

  const closeDeleteProjectPopup = () => {
    setDeleteProjectPopup(false);
  };
  const onChangeDownloadFile = (e) => {
    if (e.target.files[0]) {
      const files = [e.target.files[0]];
      setDownloadFile(files[0]);
    }
  };

  const handleCreateProject = () => {
    api.addFile(downloadFile, 'rollets')
      .then((res) => {
        console.log(res);
        api.getOrderList()
        .then((res) => setData(res.results))
        .catch(err => console.log(err))
        closeCreateProjectPopup();
      })
      .catch((err) => console.log(err));
  };

  const handleClickRow = (order) => {
    onSetCurrentOrder(order);
    onOpen();
  }

  const onSelectChange = selectedRowKeys => {
    console.log('selectedRowKeys changed: ', selectedRowKeys);
    setSelectedRows(selectedRowKeys );
    const res = [];

    selectedRowKeys.forEach(item => {
      data.forEach(order => {
        if (order.id === item) {
          res.push(order)
        }
      })
    })
    onSetSelectedOrder(res)
  }
  const handleDeleteProject = () => {
    const sendData = {
      project_ids: selectedRows
    }
    api.deleteProject(sendData)
      .then((res) => {
        console.log(res)
      })
      .catch((err) => console.log(err));
    console.log(selectedRows);
  };

  const handleClickButton = () => {
    navigate('/complect');
  }

  const rowSelection = {
    selectedRows,
    onChange: onSelectChange,
    selections: [
      Table.SELECTION_ALL,
      Table.SELECTION_INVERT,
      Table.SELECTION_NONE,
    ],
  };

  useEffect(() => {
    api.getOrderList()
    .then((res) => setData(res.results))
    .catch(err => console.log(err))
  }, [])

  useEffect(() => {
    const handleMouseMove = (event) => {
      setRowPopupPosition({
        top: event.pageY,
        left: event.pageX,
      });
    }

        // Список действий внутри одного хука
    document.addEventListener('mousemove', handleMouseMove);

        // Возвращаем функцию, которая удаляет эффекты
    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
    };
  });
    return (
      <>
        <Modal
          title="Новый заказ"
          visible={createProjectPopup}
          okText="Создать"
          cancelText="Отмена"
          closable={false}
          onCancel={closeCreateProjectPopup}
          onOk={handleCreateProject}
          okButtonProps={{disabled: !downloadFile?.name && true}}
        >
          <p>Выберите файл для загрузки нового проекта</p>
          <p>Поддерживаются только файлы формата .xml</p>
          <Input onChange={(e) => onChangeDownloadFile(e)} type="file" />
        </Modal>
        <Modal
          title="Вы уверены, что хотите удалить проект?"
          visible={deleteProjectPopup}
          okText="Отмена"
          cancelText="Удалить"
          closable={false}
          onCancel={handleDeleteProject}
          onOk={closeDeleteProjectPopup}
        >
        </Modal>
        <Title>Заказы клиентов</Title>
        <Button type="primary" onClick={openCreateProjectPopup}>Создать заказ</Button>
        <Table
          rowKey='id'
          onRow={(record, rowIndex) => {
            return {
              onClick: event => {handleClickRow(record)},
              onMouseEnter: event => {handleFocusRow(record)}, // mouse enter row
              onMouseLeave: event => {handleBlurRow()}, // mouse leave row
            };
          }}
          rowSelection={rowSelection}  columns={columns} dataSource={data}
        />
        <InfoHoverPopup position={rowPopupPosition} data={rowData} isOpen={rowPopup} />
        <div style={{display: 'flex', gap: '30px', width: '100%', justifyContent: 'center'}}>
          <Button disabled={selectedRows.length === 0} onClick={openDeleteProjectPopup}>Удалить проект</Button>
          <Button disabled={selectedRows.length === 0} type="primary" onClick={handleClickButton}>Скомплектовать</Button>
        </div>
      </>
    )
}

export default  OrdersPage ;
