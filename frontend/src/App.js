import React from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import './Styles/App.css';
import AppNavbar from "./Components/Navbar";
import {BrowserRouter, Route, Routes,} from "react-router-dom";
import Home from "./Pages/Home";
import Login from "./Pages/Login";
import Verify from "./Pages/Verify";
import './Styles/Global.css';
import axios from "axios";


axios.defaults.headers.common['Authorization'] = `Bearer ${localStorage.getItem("token")}`;

function App() {
    return (
        <BrowserRouter>
            <AppNavbar/>
            <Routes>
                <Route path={"/"} element={<Home/>}/>
                <Route path={"/login"} element={<Login/>}/>
                <Route path={"/verify"} element={<Verify/>}/>
            </Routes>
        </BrowserRouter>
    );
}

export default App;
