import React, { useEffect, useState } from 'react';
import 'antd/dist/antd.css';
import { Table, Button, Typography, Modal, Input } from 'antd';
import api from '../api/api';

const { Title } = Typography;
const columns = [
    {
      title: 'Класс',
      dataIndex: 'classes',
    },
    {
      title: 'Материал',
      dataIndex: 'material',
    },
    {
      title: 'Длина',
      dataIndex: 'length',
    },
    {
      title: 'Количество',
      dataIndex: 'quantity',
    },
    {
      title: 'артикул',
      dataIndex: 'artnumber',
    },
    {
      title: 'Цвет',
      dataIndex: 'color',
    },
    {
      title: 'Цена',
      dataIndex: 'price',
    },
    {
      title: 'id материала',
      dataIndex: 'material_id',
    },
  ];

const Queue = ({onSetCurrentOrder, onOpen, onSetSelectedOrder, }) => {
  const [data, setData] = useState()
  const [selectedRows, setSelectedRows] = useState([]);
  const [deletePopup, setDeletePopup] = useState(false);
  const [addToStorePopup, setAddToStorePopup] = useState(false);
  const [quantity, setQuantity] = useState(0);

  const successPopup = (title) => {
    let secondsToGo = 5;
    const modal = Modal.success({
      title: title,
      content: `Это окно закроется автоматически через ${secondsToGo} сек.`,
    });
    const timer = setInterval(() => {
      secondsToGo -= 1;
      modal.update({
        content: `Это окно закроется автоматически через ${secondsToGo} сек.`,
      });
    }, 1000);
    setTimeout(() => {
      clearInterval(timer);
      modal.destroy();
    }, secondsToGo * 999);
  };

  const openDeletePopup = () => {
    setDeletePopup(true);
  };

  const closeDeletePopup = () => {
    setDeletePopup(false);
  };

  const openAddStorePopup = () => {
    setAddToStorePopup(true);
  };

  const closeAddStorePopup = () => {
    setAddToStorePopup(false);
  };

  const handleSetQuantity = (e) => {
    const { value } = e.target;
    setQuantity(value);
  }

  const onSelectChange = (selectedRowKeys, selectedRows) => {
    setSelectedRows(selectedRows);
  }

  const getAllQueue = () => {
    api.getAllQueue()
    .then((res) => {
      const queueData = res.map((item) => {
        return {
          id: item.id,
          classes: item.classes,
          material: item.material_name,
          length: item.length,
          quantity: item.quantity,
          project: item.project,
          artnumber: item.parts.artnumber,
          color: item.color_name,
          parts_id: item.parts.id,
          material_id: item.parts.material_id,
          price: item.parts.price,
          price_currency: item.parts.price_currency
        }
      });
      setData(queueData);
    })
    .catch((err) => console.log(err));
  };

  const handleDeleteQueue = () => {
    let sendData = {};
    if (selectedRows.length === 1) {
      sendData = {
      material_id: selectedRows[0].parts_id,
      list: [{
        status: false,
        quantity: selectedRows[0].quantity,
        material: selectedRows[0].length
      }]
      };
    } else {
      const arr = selectedRows.map((item) => {
        return {
          material_id: item.parts_id,
          list: [{
                status: false,
                quantity: item.quantity,
                material: item.length
              }]
        }
      })
      sendData = {
        material_ids: arr
      };
    }
    // const sendData = {
    //   material_id: selectedRows.parts_id,
    //   list: [{
    //     status: false,
    //     quantity: selectedRows.quantity,
    //     material: selectedRows.length
    //   }
    //   ]
    // }
    api.deleteQueue(sendData)
      .then((res) => {
        getAllQueue();
        closeDeletePopup();
        successPopup('Материалы удалены из списка');
      })
      .catch((err) => console.log(err))
      .finally(() => closeDeletePopup());
  };

  const addQueueToStore = () => {
    let sendData = {};
    if (selectedRows.length === 1) {
      sendData = {
      material_id: selectedRows[0].parts_id,
      list: [{
        status: true,
        quantity: +quantity,
        material: selectedRows[0].length
      }]
      };
    } else {
      const arr = selectedRows.map((item) => {
        return {
          material_id: item.parts_id,
          list: [{
                status: true,
                quantity: item.quantity,
                material: item.length
              }]
        }
      })
      sendData = {
        material_ids: arr
      };
    }
    api.deleteQueue(sendData)
      .then((res) => {
        getAllQueue();
        closeAddStorePopup();
        successPopup('Материалы добавлены на склад');
      })
      .catch((err) => console.log(err))
      .finally(() => closeAddStorePopup());
  }

  const rowSelection = {
    // type: 'radio',
    selectedRows,
    onChange: onSelectChange,
    selections: [
      Table.SELECTION_ALL,
      Table.SELECTION_INVERT,
      Table.SELECTION_NONE,
    ],
  };

  useEffect(() => {
    getAllQueue();
  }, [])

    return (
      <>
        <Modal
          title="Удалить заказ?"
          visible={deletePopup}
          okText="Удалить"
          cancelText="Отмена"
          closable={false}
          onCancel={closeDeletePopup}
          onOk={handleDeleteQueue}
        >
        </Modal>
        <Modal
          title="Добавить заказ на склад?"
          visible={addToStorePopup}
          okText="Добавить на склад"
          cancelText="Отмена"
          closable={false}
          onCancel={closeAddStorePopup}
          onOk={addQueueToStore}
        >
          {selectedRows.length === 1 && (
            <>
              <p>Укажите количество материалов, которые вы хотите добавить на склад</p>
              <Input placeholder='Количество' type="number" name="quantity" onChange={handleSetQuantity} value={quantity} />
            </>
          )}
        </Modal>
        <Title>Заказ материалов</Title>
        <Table
          rowKey='id'
          rowSelection={rowSelection}  columns={columns} dataSource={data}
        />
        <div style={{display: 'flex', gap: '30px', width: '100%', justifyContent: 'center'}}>
          <Button disabled={selectedRows.length === 0} danger  onClick={openDeletePopup}>Удалить отмеченное</Button>
          <Button disabled={selectedRows.length === 0} type="primary" onClick={openAddStorePopup}>Добавить на склад</Button>
        </div>
      </>
    )
}

export default  Queue ;
