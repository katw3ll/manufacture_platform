import React from 'react';
import './InfoHoverPopup.css';

function InfoHoverPopup({ isOpen, data, position }) {
  console.log(data);
  return (
    <div style={{
      position: 'absolute',
      top: position.top,
      left: position.left,
      pointerEvents: 'none',
    }} className={isOpen ? 'popup-info popup_visible' : 'popup-info'}>
      <p>Рольставни в проекте</p>
      {data?.rollets?.map((item) => {
        return (
          <>
            <div className='popup__parameter-container'>
              <p>Высота</p>
              <p>{item.height}</p>
            </div>
            <div className='popup__parameter-container'>
              <p>Ширина</p>
              <p>{item.width}</p>
            </div>
            <div className='popup__parameter-container'>
              <p>Тип материала</p>
              <p>{item.material_name}</p>
            </div>
            <div className='popup__parameter-container'>
              <p>Цвет</p>
              <p>{item.color_name}</p>
            </div>
            <hr />
          </>
        )
      })}
      {/* <div className='popup__parameter-container'>
        <p>{data.name}</p>
        <p>{data.parameter}</p>
      </div>
      <div className='popup__parameter-container'>
        <p>{data.name}</p>
        <p>{data.parameter}</p>
      </div> */}
    </div>
  );
}

export default InfoHoverPopup;
