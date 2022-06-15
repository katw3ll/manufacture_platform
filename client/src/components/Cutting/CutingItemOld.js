import React from 'react';
import './CuttingItem.css';
import { colors } from '../../utils/mocks';

function CuttingItemOld({ item, handleSetCurrentCut }) {
  return (
    <li
      className="cut"
      style={{marginBottom: '20px'}}
      onClick={() => handleSetCurrentCut(item)}
    >
      <p>Начальная длина: {item.material} </p>
      <p>Количество: {item.count} </p>
      <div className="cut__container">
        {item.map && item.map.length > 0 && item.map.map((part, i) => (
          <div
            className='cut__item'
            style={{width: `${(part / item.material) * 100}%`, backgroundColor: `${colors[i]}`}}
            key={i}
          >
            {part}
          </div>
        ))}
      </div>
      <p>Остаток: {item.rest}</p>
    </li>
  );
}

export default CuttingItemOld;
