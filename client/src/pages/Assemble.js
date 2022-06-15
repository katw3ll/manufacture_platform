import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import 'antd/dist/antd.css';
import { Table, Button, Typography, Modal, Input, Radio } from 'antd';
import api from '../api/api';

const { Title } = Typography;
const columns = [
    {
      title: 'id материала',
      dataIndex: 'rollet_id',
    },
    {
      title: 'Номер проекта',
      dataIndex: 'project',
    },
    {
      title: 'Материал',
      dataIndex: 'material',
    },
    {
      title: 'Цвет',
      dataIndex: 'color',
    },
    {
      title: 'Высота',
      dataIndex: 'height',
    },
    {
      title: 'Ширина',
      dataIndex: 'width',
    },
    {
      title: 'Статус сборки',
      dataIndex: 'status_packed',
    },
  ];

  const rolletCompositionTitles = [
    {
      title: 'Класс',
      dataIndex: 'class',
    },
    {
      title: 'Цвет',
      dataIndex: 'color',
    },
    {
      title: 'Длина',
      dataIndex: 'length',
    },
    {
      title: 'Материал',
      dataIndex: 'material',
    },
    {
      title: 'Необходимое количество',
      dataIndex: 'need_count',
    },
    {
      title: 'Имеется в наличии',
      dataIndex: 'quantity',
    },
  ];

  const needToCutMaterialTableTitles = [
    {
      title: 'Материал',
      dataIndex: 'parts_name',
    },
    {
      title: 'Длина',
      dataIndex: 'length',
    },
    {
      title: 'Код',
      dataIndex: 'parts',
    },
    {
      title: 'Цвет',
      dataIndex: 'parts_color',
    },
    {
      title: 'Необходимое количество',
      dataIndex: 'to_need_count',
    },
  ];

  const needToOrderMaterialTableTitles = [
    {
      title: 'Материал',
      dataIndex: 'parts_name',
    },
    {
      title: 'Код',
      dataIndex: 'parts',
    },
    {
      title: 'Цвет',
      dataIndex: 'parts_color',
    },
    {
      title: 'Необходимое количество',
      dataIndex: 'to_need_count',
    },
  ];
const Assemble = ({
  onOpen,
  getOrdersIds
}) => {
  const [data, setData] = useState()
  const [currentRollet, setCurrentRollet] = useState({});
  const [rolletComposition, setRolletComposition] = useState([]);
  const [errorPopup, setErrorPopup] = useState(false);
  const [needToCutMaterials, setNeedToCutMaterials] = useState([])
  const [needToOrderMaterials, setNeedToOrderMaterials] = useState([])
  const [materialsToOrder, setMaterialsToOrder] = useState([]);

  const openErrorPopup = () => {
    setErrorPopup(true);
  };

  const closeErrorPopup = () => {
    setErrorPopup(false);
  };

  const successPopup = () => {
    let secondsToGo = 5;
    const modal = Modal.success({
      title: 'Сборка прошла успешно',
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

  const onSelectChange = (key, selectedRow) => {
    setCurrentRollet(selectedRow[0]);
    console.log(key, selectedRow);
  }

  const handleSelectOrderMaterials = (key, selectedRows) => {
    const arrayOfIds = selectedRows.map((item) => {
      return item.parts;
    })
    setMaterialsToOrder(arrayOfIds);
  }

  const handleOrderMaterials = () => {
    const sendData = {

    };
    api.addQueue(sendData)
      .then((res) => {
        console.log(res)
      })
      .catch((err) => console.log(err))
  }

  const handleAssembleRollet = () => {
    const sendData = {
      project_id: getOrdersIds()[0],
      rollet_id: currentRollet.rollet_id
    }
    api.assembleTheRollet(sendData)
      .then((res) => {
        if (res.status === 'not_ok') {
          openErrorPopup();
          setNeedToCutMaterials(res.need_to_cut);
          setNeedToOrderMaterials(res.need_to_order);
        } else if (res.status === 'error') {
          openErrorPopup();
        } else {
          successPopup();
          getProjectsRollets();

        }
      })
      .catch((err) => console.log(err));
  };

  const rowSelection = {
    type: 'radio',
    onChange: onSelectChange,
    selections: [
      Table.SELECTION_INVERT,
      Table.SELECTION_NONE,
    ],
  };

  const orderMaterialsRowSelection = {
    onChange: handleSelectOrderMaterials,
  }
  const getProjectsRollets = () => {
    const sendData = {
      project_ids: getOrdersIds()
    }
    api.getProjectRollets(sendData)
      .then(res => {
        const resData = res.results.map((item) => {
          const status = () => {
            if (item.status_packed) return 'Собрано';
            else return 'Не собрано'
          };
          return {
            color: item.color,
            height: item.height,
            material: item.material,
            project: item.project,
            rollet_id: item.rollet_id,
            status_packed: status(),
            width: item.width
          }
        })
        setData(resData)
      })
  };

  useEffect(() => {
    getProjectsRollets();
  }, [])

  useEffect(() => {
    if (!currentRollet?.rollet_id) return;
    const sendData = {
      project_id: getOrdersIds()[0],
      rollet_id: currentRollet.rollet_id
    }
    api.getRolletComposition(sendData)
      .then((res) => {
        setRolletComposition(res.results[0]);
      })
      .catch((err) => console.log(err));
  }, [currentRollet]);

  useEffect(() => {
    console.log(materialsToOrder);
  }, [materialsToOrder])
    return (
      <>

        <Modal
          title="Не удалось собрать роллету"
          visible={errorPopup}
          okText="Закрыть"
          // cancelText="Удалить"
          closable={true}
          onCancel={closeErrorPopup}
          onOk={closeErrorPopup}
          footer={[
            <Button key="submit" type="primary"onClick={closeErrorPopup}>
              Закрыть
            </Button>,
          ]}
        >
          {needToCutMaterials?.length > 0 && (
            <>
              <p>Необходимо выполнить распил следующих материалов</p>
              <Table
                columns={needToCutMaterialTableTitles} dataSource={needToCutMaterials}
              />
            </>
          )}
          {needToOrderMaterials?.length > 0 && (
            <>
              <p>Не хватает следующих материалов</p>
              <Table
                rowKey='parts'
                rowSelection={orderMaterialsRowSelection}
                columns={needToOrderMaterialTableTitles} dataSource={needToOrderMaterials}
              />
              <Button disabled={materialsToOrder?.length === 0} type="primary" onClick={handleOrderMaterials}>Заказать материалы</Button>
            </>
          )}
        </Modal>
        <Title>Сборка роллет</Title>
        <p>Выберите роллету для сборки</p>
        <Table
          rowKey='rollet_id'
          rowSelection={rowSelection}  columns={columns} dataSource={data}
        />
        {rolletComposition?.length > 0 && (
          <>
            <p>Необходимые материалы</p>
            <Table
              columns={rolletCompositionTitles} dataSource={rolletComposition}
            />
          </>
        )}
        <Button type="primary" disabled={!currentRollet?.rollet_id} onClick={handleAssembleRollet}>Собрать</Button>
      </>
    )
}

export default  Assemble ;
