import React from 'react';

function ComplectItem({ item, index, i, handleClick }) {
  return (
    <li
      key={item.code}
      className={`complect__item ${index === i && "complect__item_active"}`}
      onClick={() => handleClick(item, i)}
    >
      <p className="complect__material-name">ID материала: {item.name} ({item.color_short})</p>
      {item.data && item.data.length > 0 && item.data.map((param, j) => (
        <div className='complect__item-info-container' key={j}>
          <span className="complect__material-length">Необходимая длина: {param['length']}</span>
          <span className="complect__material-count">Отпилено: {param['quantity']} из {param['need_count']}</span>
        </div>
      ))}
    </li>
  );
}

export default ComplectItem;
