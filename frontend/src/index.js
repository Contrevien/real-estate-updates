import React from 'react';
import ReactDOM from 'react-dom';
import { Route, Switch, BrowserRouter as Router } from 'react-router-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
import Unsubscribed from './Unsubscribed';
import NotFound from './components/NotFound/NotFound';

const routing = (
    <Router>
        <Switch>
            <Route exact path="/" component={App} />
            <Route exact path="/unsubscribe/:email" component={Unsubscribed} />
            <Route component={NotFound} />
        </Switch>
    </Router>
)

ReactDOM.render(routing, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
