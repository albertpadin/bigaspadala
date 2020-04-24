import React from 'react';
import { BrowserRouter, Switch, Route, Link } from 'react-router-dom';

import Home from '@pages/Home';
import Send from '@pages/Send';

const App = () => {
  return (
    <BrowserRouter>
      <Link to="/">Home</Link>
      <Link to="/send">Send</Link>

      <Switch>
        <Route path="/" exact component={Home} />
        <Route path="/send" component={Send} />
      </Switch>
    </BrowserRouter>
  );
};

export default App;
