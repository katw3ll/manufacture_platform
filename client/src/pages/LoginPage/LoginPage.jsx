import React, { useState } from 'react';

import './LoginPage.css';

const LoginPage = ({ onSubmit }) => {

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const changeEmail = (e) => {
    setEmail(e.target.value)
  }

  const changePassword = (e) => {
    setPassword(e.target.value)
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    const form = document.getElementById('login__form');
    let sendData = new FormData(form)
    sendData.append('username', email);
    sendData.append('password', password);
    console.log(sendData)
    // const sendData = {
    //   username: email,
    //   password: password
    // };
    onSubmit(sendData);
  }

  return (
    <div className="login">
      <form id="login__form" onSubmit={handleSubmit} style={{"margin": "200px auto 0", "width":"200px"}}>
        <input className="login__input" placeholder="Имя пользователя" name="username" type="text" value={email} onChange={changeEmail} />
        <input className="login__input" name="password" placeholder="Пароль" type="password" value={password} onChange={changePassword} />
        <button type="submit" className="login__submit">Войти</button>
      </form>
    </div>
  )
}

export default LoginPage;
