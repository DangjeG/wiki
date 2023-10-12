import React, {useLayoutEffect, useState} from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import './Styles/App.css';
import AppNavbar from "./Components/Navbar";
import {BrowserRouter, Route, Routes,} from "react-router-dom";
import Home from "./Pages/Home";
import Login from "./Pages/Login";
import Verify from "./Pages/Verify";
import './Styles/Global.css';
import SignUp from "./Pages/SignUp";


export default function App() {

    const [isLogin, updateLogin] = useState(false)



        return (
        <BrowserRouter>
            <AppNavbar isLogin ={isLogin}/>
            <Routes>
                <Route path={"/"} element={<Home/>}/>
                <Route path={"/login"} element={<Login/>}/>
                <Route path={"/verify"} element={<Verify/>}/>
                <Route path={"/signup"} element={<SignUp/>}/>
            </Routes>
        </BrowserRouter>
    );
}
