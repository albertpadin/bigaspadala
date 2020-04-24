import React, { lazy, Suspense } from 'react';
import { BrowserRouter, Switch, Route, Link } from 'react-router-dom';

const Home = lazy(() => import('@pages/Home'));
const Send = lazy(() => import('@pages/Send'));

const App = () => {
  return (
    <BrowserRouter>
      <Link to="/">Home</Link>
      <Link to="/send">Send</Link>

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
