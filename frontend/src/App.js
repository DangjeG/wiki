import 'bootstrap/dist/css/bootstrap.min.css';
import './Styles/App.css';
import AppNavbar from "./Components/Navbar";
import {BrowserRouter, Route, Routes,} from "react-router-dom";
import Home from "./Pages/Home";
import Login from "./Pages/Login";
import Verify from "./Pages/Verify";
import './Styles/Global.css';
import SignUp from "./Pages/SignUp";
import {api} from "./app.config";
import Logout from "./Pages/Logout";
import Admin from "./Pages/Admin";


export default function App() {

        return (
        <BrowserRouter>
            <AppNavbar isLogin ={api.isLogin()}/>
            <Routes>
                <Route path={"/"} element={<Home/>}/>
                <Route path={"/login"} element={<Login/>}/>
                <Route path={"/verify"} element={<Verify/>}/>
                <Route path={"/signup"} element={<SignUp/>}/>
                <Route path={"/logout"} element={<Logout/>}/>
                <Route path={"/admin"} element={<Admin/>}/>
            </Routes>
        </BrowserRouter>
    );
}
