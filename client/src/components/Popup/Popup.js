import React from 'react';
import './Popup.css'

function Popup({ isOpen, handleClose, title = 'Добавьте заголовок', text = 'Добавьте текст' }) {
  return (
    <div className={isOpen ? 'popup popup_active' : 'popup'}>
      <div className='popup__form'>
        <h5 className='popup__title'>{title}</h5>
        <p className='popup__text'>{text}</p>
        <button onClick={handleClose} className='popup__button'>Закрыть</button>
      </div>
    </div>
  );
}

export default Popup;
