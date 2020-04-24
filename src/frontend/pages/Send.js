import React from 'react';
import { Button } from 'antd';
import style from './Send.module.css';

const Send = () => {
  return (
    <div>
      <h1 className={style.heading}>Send Page</h1>
      <Button type="primary">Send Money</Button>
    </div>
  );
};

export default Send;
