import React, { useState, useEffect } from 'react';
import 'antd/dist/antd.css';
import QRCode from "react-qr-code";
import base64 from 'react-native-base64'
import Popup from '../../components/Popup/Popup';
import { Radio, Select, Input, Button, Typography } from 'antd';
import api from '../../api/api';
import './StorePage.css';

const { Option } = Select;

const { Title } = Typography;

const StorePage = () => {
  const [mode, setMode] = useState("lengths");
  const [addMode, setAddMode] = useState('addParameters')
  const [operation, setOperation] = useState('Поиск')
  const [data, setData] = useState([])
  const [lengths, setLengths] = useState([]);
  const [accessories, setAccessories] = useState([]);
  const [searchingItem, setSearchingItem] = useState('')
  const [values, setValues] = useState({});
  const [searchingItems, setSearchingItems] = useState([]);
  const [addingFile, setAddingFile] = useState([]);
  const [popup, setPopup] = useState(false);
  const [popupText, setPopupText] = useState({});

  const handleChangeInput = (e) => {
    const { name, value } = e.target;
    setValues({ ...values, [name]: value });
    console.log(values);
  };

  const handleChange = (str) => {
    setOperation(str)
  }
  const handleSelectStoreItem = (value) => {
    if (mode === 'lengths') {
      const val = value.split(':');
      const partcode = val[0];
      const color = val[1].trim();
      setSearchingItem({ partcode: partcode, color: color });
      const item = lengths.find(item => item.partcode === partcode);
      console.log(item);
    } else {
      const val = value.split(':');
      const partcode = val[0];
      const color = val[1].trim();
      setSearchingItem({ partcode: partcode, color: color });
      const item = accessories.find(item => item.partcode === partcode.trim());
      console.log(item);
    }

  };

  const handleSearching = () => {
    if (mode === 'lengths') {
      const searchingData = {
        length: values.width ? values.width : '',
        material_id: searchingItem.partcode ? searchingItem.partcode.trim() : '',
      }
      api.searchLengths(searchingData)
        .then((res) => {
          setSearchingItems(res.results)
        })
        .catch((err) => console.log(err));
    } else {
      const searchingData = {
        material_id: searchingItem.partcode ? searchingItem.partcode.trim() : '',
      }
      api.searchAccessories(searchingData)
        .then((res) => {
          setSearchingItems(res.results)
        })
        .catch((err) => console.log(err));
    }
  };

  const handleAddMaterial = () => {
    console.log(searchingItem.partcode);
    let sendData = {};
    if (mode === 'lengths') {
      sendData = {
        material_id: +searchingItem.partcode.trim(),
        length: +values.width,
        quantity: +values.quantity
      }
    } else {
      sendData = {
        material_id: +searchingItem.partcode.trim(),
        quantity: +values.quantity
      }
    }
    const closePopup = () => {
      setPopup(false);
    };
    api.addMaterialToStock(sendData)
      .then((res) => {
        setPopup(true);
        setPopupText({
          title: "Вы добавили материалы на склад",
          text: `${res.results.length ? `длина: ${res.results.length}` : ''}
          количество: ${res.results.quantity}`
        })
        setTimeout(closePopup, 4000);
      })
      .catch((err) => console.log(err));
  };
  const onChangeFile = (evt) => {
    if (evt.target.files[0]) {
      const files = [evt.target.files[0]];
      setAddingFile(files[0]);
    }
  };
  const addFile = () => {
    console.log(addingFile)
    api.addFile(addingFile, 'stock')
  };

  const getLengths = () => {
    api.getStoreItems('lengths')
      .then((res) => {
        setLengths(res.results);
      })
      .catch((err) => console.log(err));
  };
  const getAccessories = () => {
    api.getStoreItems('accessories')
      .then((res) => {
        setAccessories(res.results);
      })
      .catch((err) => console.log(err));
  }
  useEffect(() => {
    getLengths();
    getAccessories();
  }, []);

  useEffect(() => {
    setData([]);
    if (mode === 'lengths') setData(lengths);
    else if (mode === 'complectation') setData(accessories);
  }, [mode, lengths, accessories]);

  useEffect(() => {
    setValues({});
  }, [mode, operation]);

  return (
    <div className='store'>
      <Title>Склад</Title>
      <Popup
        isOpen={popup}
        handleClose={() => setPopup(false)}
        title={popupText.title}
        text={popupText.text}
      />
      <div className='store__control-container'>
        <Radio.Group defaultValue="lengths" buttonStyle="solid">
          <Radio.Button onClick={() => setMode('lengths')} value="lengths">Длиномеры</Radio.Button>
          <Radio.Button onClick={() => setMode('complectation')} value="complectation">Комплектация</Radio.Button>
        </Radio.Group>
        <Select defaultValue="Поиск" style={{ width: 220 }} onChange={handleChange}>
          <Option value="Поиск">Поиск по складу</Option>
          <Option value="Добавить">Добавить</Option>
        </Select>
      </div>
      <div className='store__control-container'>
        {operation === 'Поиск'
        ?
          <div className='store__select-container'>
            <Select
              showSearch
              style={{ width: 200 }}
              placeholder="Выбор материалов"
              optionFilterProp="children"
              filterOption={(input, option) => option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0}
              filterSort={(optionA, optionB) => optionA.children.toLowerCase().localeCompare(optionB.children.toLowerCase())}
              onChange={handleSelectStoreItem}
            >
              {data && data.length && data.length > 0 && data.map((item, index) => (
                <Option type="number" key={index} value={`${item.partcode}: ${item.color}`}>{`${item.name} ${item.color}`}</Option>
              ))}
            </Select>
            {mode === 'lengths' && <Input name="width" onChange={handleChangeInput} style={{ width: '30%' }} placeholder="Ширина, мм" />}
            <Button onClick={handleSearching}>Поиск</Button>
          </div>
        :
          <div className='store__control-container'>
            <div style={{display: 'flex'}}>
              <Radio.Group defaultValue="lengths" buttonStyle="solid">
                <Radio.Button onClick={() => setAddMode('addParameters')} value="lengths">Добавить по параметрам</Radio.Button>
                <Radio.Button onClick={() => setAddMode('addFile')} value="complectation">Добавить файл</Radio.Button>
              </Radio.Group>
            </div>
            {addMode === 'addParameters' ? (
              <div style={{display: 'flex'}}>
              <Select
                showSearch
                style={{ width: 200 }}
                placeholder="Выбор материалов"
                optionFilterProp="children"
                filterOption={(input, option) =>
                option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0}
                filterSort={(optionA, optionB) =>
                optionA.children.toLowerCase().localeCompare(optionB.children.toLowerCase())}
                onChange={handleSelectStoreItem}
              >
                {data && data.length && data.length > 0 && data.map((item, index) => (
                  <Option type="number" key={index} value={`${item.partcode}: ${item.color}`}>{`${item.name} ${item.color}`}</Option>
                ))}
              </Select>
              { mode === 'lengths' && <Input name="width" style={{ width: '30%' }} onChange={handleChangeInput} placeholder="Ширина, мм" />}
              <Input name="quantity" onChange={handleChangeInput} style={{ width: '30%' }} placeholder="Количество, шт" />
              <Button onClick={() => handleAddMaterial()}>Добавить</Button>
            </div>
            ) : (
              <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%', gap: '15px'}}>
                <input style={{alignSelf: 'center'}} onChange={onChangeFile} type="file" />
                <Button onClick={() => addFile()}>Добавить</Button>
              </div>
            )}
          </div>
        }
        <div style={{display: 'flex', flexDirection: 'column', gap: '15px', width: '100%', margin: '0 auto'}}>
          {searchingItems.length > 0 ? (
            searchingItems.map((item) => {
              return (
                <div className='searching-item'>
                  <div className='searching-item__parameter'>
                    <p className='searching-item__text searching-item__title-text'>Название</p>
                    <p className='searching-item__text searching-item__title-text'>{item.name}</p>
                  </div>
                  <div className='searching-item__parameter'>
                    <p className='searching-item__text searching-item__title-text'>Код материала</p>
                    <p className='searching-item__text'>{item.partcode}</p>
                  </div>
                  {item.length && (
                    <div className='searching-item__parameter'>
                      <p className='searching-item__text searching-item__title-text'>Длина</p>
                    <p className='searching-item__text'>{item.length}</p>
                  </div>
                  )}
                  <div className='searching-item__parameter'>
                    <p className='searching-item__text searching-item__title-text'>Количество на складе</p>
                    <p className='searching-item__text'>{item.count}</p>
                  </div>
                  <div className='searching-item__parameter'>
                    <p className='searching-item__text searching-item__title-text'>Цвет</p>
                    <p className='searching-item__text'>{item.color === 'None' ? 'Без цвета' : item.color}</p>
                  </div>
                  <div className='searching-item__parameter'>
                    <p className='searching-item__text searching-item__title-text'>Штрихкод материала</p>
                    {/* <p className='searching-item__text'>{base64.decode(item.barcode)}</p> */}
                    <QRCode size="128"
                      value={item.barcode}
                    />
                  </div>
                </div>
              )
            })
          ) : (
            <p>По вашему запросу ничего не найдено</p>
          )}
        </div>
      </div>
    </div>
  )
}

export default StorePage;
