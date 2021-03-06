import React from 'react';
import { Provider } from 'react-redux';
import './App.scss';
import {
    BrowserRouter as Router,
    Route,
    Switch,
    Redirect,
} from 'react-router-dom';
import Header from './components/Header/Header';
import Categories from './components/Categories/Categories';
import Channels from './components/Channels/Channels';
import Main from './pages/Main/Main';
import SettingsPage from './pages/SettingsPage/SettingsPage';
import TrendsPage from './pages/TrendsPage/TrendsPage';
import OneTrendPage from './pages/OneTrendPage/OneTrendPage';
import store from './store/createStore';

const App: React.FC = () =>
    (
        <Provider store={store}>
            <Router>
                <div className="App">
                    <Header />
                    <Categories />
                    <div className="App-Main">
                        <Route exact path="/main" component={Channels} />
                        <div className="App-Content">
                            <Switch>
                                <Redirect exact from="/" to="/main" />
                                <Route path="/settings" component={SettingsPage} />
                                <Route path="/:category/trends/:collectionId" component={OneTrendPage} />
                                <Route path="/:category/trends" component={TrendsPage} />
                                <Route path="/:category?" component={Main} />
                            </Switch>
                        </div>
                    </div>
                </div>
            </Router>
        </Provider>
    );

export default App;
