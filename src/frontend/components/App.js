import React, { lazy, Suspense } from 'react';
import { BrowserRouter, Switch, Route, Link } from 'react-router-dom';
import Button from 'antd/es/button';

const Home = lazy(() => import('@pages/Home'));
const Send = lazy(() => import('@pages/Send'));

const App = () => {
  return (
    <BrowserRouter>
      <Link to="/">
        <Button type="link" tabIndex="-1">
          Home
        </Button>
      </Link>
      <Link to="/send">
        <Button type="link" tabIndex="-1">
          Send
        </Button>
      </Link>

      <Suspense fallback={<p>Loading...</p>}>
        <Switch>
          <Route path="/" exact component={Home} />
          <Route path="/send" component={Send} />
        </Switch>
      </Suspense>
    </BrowserRouter>
  );
};

export default App;
