import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Typography, Button, Modal, Input } from 'antd';
import Preloader from '../components/Preloader/Preloader';
import ComplectItem from '../components/Cutting/ComplectItem';
import CuttingItem from '../components/Cutting/CuttingItem';
import CuttingItemOld from '../components/Cutting/CutingItemOld';
import './ComplectationPage.css'
import api from '../api/api'

const { Title } = Typography;

const ComplectPage = ({selectedOrders, getOrdersIds}) => {
  const [elements, setElements] = useState([]);
  const [currentElement, setCurrentElement] = useState(null);
  const [index, setIndex] = useState('')
  const [cuts, setCuts] = useState([]);
  const [isLoading, setIsLoading] = useState(false)
  const [values, setValues] = useState({});
  const [cutDefectValues, setCutDefectValues] = useState({});
  const [currentCut, setCurrentCut] = useState(null);
  const [orderCut, setOrderCut] = useState(null);
  const [cutPopup, setCutPopup] = useState(false);
  const [defectPopup, setDefectPopup] = useState(false);
  const navigate = useNavigate();

  const openCutPopup = () => {
    setCutPopup(true)
  };

  const closeCutPopup = () => {
    setCutPopup(false);
  };

  const openDefectPopup = () => {
    setDefectPopup(true);
  };

  const closeDefectPopup = () => {
    setDefectPopup(false);
    setCutDefectValues([]);
  };

  const handleChangeCutDefect = (evt) => {
    const { name, value } = evt.target;
    setCutDefectValues({ ...cutDefectValues, [name]: +value });
  };

  const handleChange = (evt) => {
    const { name, value } = evt.target;
    setValues({ ...values, [name]: value });
  };

  const handleClick = (element, i) => {
    setCurrentElement(element)
    setIndex(i)
  }

  const handleSetCurrentCut = (item, i) => {
    setCurrentCut({...item, index: i});
  }

  const handleSetOrderCut = (item) => {
    setOrderCut(item);
    console.log(item);
  }

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

  const errorPopup = (title) => {
    let secondsToGo = 5;
    const modal = Modal.error({
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

  const getAllMaterials = () => {
    const ids ={ data: getOrdersIds()}
    api.getMaterialBySelectOrders(ids)
      .then(res => {
        setElements(res.results)
      })
  };

  const getMaterialCutting = () => {
    setIsLoading(true);
    setCuts([]);
    const data = {
      project_ids: getOrdersIds(),
      material_id: currentElement.code
    };
    api.getMap(data)
    .then(res => {
      console.log(res)
      setCuts(res.results)
    })
    .finally(() => setIsLoading(false));
  };

  const handleClickButton = () => {
    getMaterialCutting();
  }

  const handleOrderCuts = () => {
    const sendData = {
      list_order: [
        orderCut
      ],
      project_ids: getOrdersIds() ,
      material_id: currentElement.code
    }
    api.addQueue(sendData)
      .then((res) => {
        if (res.results.list[0].status === 'already booked') {
          errorPopup('Материалы уже добавлены в очередь');
          console.log(res);
          return;
        }
        successPopup('Заказанные материалы добавлены в очередь');
        console.log(res);
      })
      .catch((err) => console.log(err));
  };

  const handleCutMaterial = () => {
    const sendData = {
      project_ids: getOrdersIds() ,
      material_id: +currentElement.code,
      quantity: +values.cut_amount,
      length: +currentCut.material,
      map: currentCut.map
    }
    api.cutMaterial(sendData)
      .then((res) => {
        console.log(res);
        closeCutPopup();
        getAllMaterials();
        getMaterialCutting();
      })
      .catch((err) => console.log(err));
  };

  const handleDefectMaterial = () => {
    let map = []
    Object.entries(cutDefectValues).forEach(([key, value]) => {
      map = [...map, value]
    });
    const sendData = {
      material_id: +currentElement.code,
      map: map,
      quantity: 1,
      project_ids: getOrdersIds(),
      rest: +values.cut_rest,
      // length: +currentCut.material
    };
    api.defectCut(sendData)
      .then((res) => {
        console.log(res);
        closeDefectPopup();
        successPopup('Материалы добавлены в брак')
      })
      .catch((err) => console.log(err));
    console.log(sendData);
  };

  useEffect(() => {
    getAllMaterials();
  }, [])

  useEffect(() => {
    console.log(currentCut);
  }, [currentCut]);

  useEffect(() => {
    console.log(currentElement);
  }, [currentElement]);
  return (
    <>
      <Modal
        title="Распил материала"
        visible={cutPopup}
        okText="Создать"
        cancelText="Отмена"
        closable={false}
        onCancel={closeCutPopup}
        onOk={() => handleCutMaterial()}
        okButtonProps={{disabled: (!values?.cut_amount && values?.cut_amount <= currentCut?.count && values?.cut_amount > 0) && true}}
      >
        <p>Укажите количество распиленных длинномеров</p>
        <Input
          name="cut_amount"
          onChange={(e) => handleChange(e)}
          min="0"
          max={currentCut?.count}
          type="number"
        />
      </Modal>
      <Modal
        title="Брак при распиле"
        visible={defectPopup}
        okText="Отправить"
        cancelText="Отмена"
        closable={false}
        onCancel={closeDefectPopup}
        onOk={() => handleDefectMaterial()}
        // okButtonProps={{disabled: (!values?.cut_amount && values?.cut_amount <= currentCut?.count && values?.cut_amount > 0) && true}}
      >
        <p>Укажите количество распиленных длинномеров</p>
        <CuttingItemOld
          item={currentCut}
          // key={i}
          handleSetCurrentCut={handleSetCurrentCut}
        />
        <p>Укажите длину распиленной части</p>
        <div style={{ display: 'flex'}}>
          {currentCut?.map?.map((item, index) => {
            return (
              <Input
                key={index}
                placeholder={item}
                name={`cutDefect_${index}`}
                value={cutDefectValues[`cutDefect_${index}`]}
                onChange={(e) => handleChangeCutDefect(e)}
                min="0"
                max={currentCut?.count}
                type="number"
              />
            )
          })}
        </div>
        <p>Остаток</p>
        <Input
          placeholder={currentCut?.rest}
          name="cut_rest"
          value={values?.cut_rest}
          onChange={(e) => handleChange(e)}
          min="0"
          max={currentCut?.count}
          type="number"
        />
      </Modal>

    {elements !== []
    ?
    <>
      <div style={{width: '85%', margin: '0 auto'}}>
        <Title className="complect__title">Потребность комплектующих</Title>
        <ul className="complect__list">
          {elements && elements.length > 0 && elements.map((item, i) => (
            <ComplectItem
              item={item}
              i={i}
              index={index}
              handleClick={handleClick}
            />
          ))}
        </ul>
        <Button type="primary" disabled={!currentElement} onClick={handleClickButton}>Получить карту раскроя</Button>
        <div className='complect__list-container'>
          {isLoading && <div style={{margin: '0 auto'}}><Preloader /></div> }
          {cuts?.res_new?.length > 0 && (
            <div className='cuts__list-new-container'>
              <h4>Новые длинномеры (под заказ)</h4>
                <ul className="cuts__list-new">
                  {cuts.res_new.length > 0 && cuts.res_new.slice(0,4).map((item, i) => (
                    <div className='cut__item-container'>
                      <label htmlFor={`cut-new-${i}`}>
                        <CuttingItem
                          item={item}
                          key={i}
                        />
                      </label>
                      <input id={`cut-new-${i}`} name='cut-new' onChange={() => handleSetOrderCut(item)} type="radio" />
                    </div>
                  ))}
                </ul>
                <Button type="primary" disabled={!orderCut} onClick={() => handleOrderCuts()}>Заказать</Button>
            </div>
          )}
          {cuts?.res_old?.length > 0 && (
            <div>
              <h4>Длинномеры из остатков</h4>
              <ul className="cuts__list-old">
                {cuts.res_old.length > 0 && cuts.res_old.slice(0,4).map((item, i) => (
                  <div className='cut__item-container'>
                    <label htmlFor={`cut-old-${i}`}>
                      <CuttingItemOld
                        item={item}
                        key={i}
                        handleSetCurrentCut={handleSetCurrentCut}
                      />
                    </label>
                    <input id={`cut-old-${i}`} name='cut-old' onChange={() => handleSetCurrentCut(item, i)} type="radio" />
                  </div>
                ))}
              </ul>
              <div>
                <Button type="danger" disabled={!currentCut} onClick={openDefectPopup}>Брак при распиле</Button>
                <Button type="primary" disabled={!currentCut} onClick={openCutPopup}>Отрезать</Button>
              </div>
          </div>
          )}
        </div>
      </div>
      <Button type="primary" onClick={() => navigate('/assemble')}>К сборке рольставней</Button>
    </>
    : <Preloader />
    }
    </>
  )
}

export default ComplectPage;
