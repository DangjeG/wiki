import 'bootstrap/dist/css/bootstrap.min.css';
import React from "react";
import {api} from "./Config/app.config";
import {useEffect, useState} from "react";
import AppNavbar from "./Components/Navbar";
import {HashRouter, Route, Routes} from "react-router-dom";
import Home from "./Pages/Home";
import Login from "./Pages/Login";
import Verify from "./Pages/Verify";
import SignUp from "./Pages/SignUp";
import Logout from "./Pages/Logout";
import Admin from "./Pages/Admin";
import Profile from "./Pages/Profile";
import Workspace from "./Pages/Workspace";
import TestPage from "./Pages/TestPage";
import ProtectedRoute from "./Components/ProtectedRoute";

export default function App() {

    const [user, setUser] = useState(null)

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await api.getMe();
                setUser(response);
            } catch (error) {
                console.log(error)
            }
        };
        fetchData();
    }, []);

    const UserContext = React.createContext()

        return (
            <UserContext.Provider value={user}>
                <HashRouter>
                    <AppNavbar/>
                    <Routes>
                        <Route path={"/"} element={<Home/>}/>
                        <Route path={"/login"} element={<Login/>}/>
                        <Route path={"/verify"} element={<Verify/>}/>
                        <Route path={"/signup"} element={<SignUp/>}/>
                        <Route path={"/logout"} element={<Logout/>}/>
                        <Route element={<ProtectedRoute requirement={
                            user !== null && user.wiki_api_client !== null && user.wiki_api_client.responsibility === 'ADMIN'
                        }/>}>
                            <Route path={"/admin"} element={<Admin/>}/>
                        </Route>
                        <Route element={<ProtectedRoute requirement={
                            user !== null && user.wiki_api_client !== null
                        }/>}>
                            <Route path={"/profile"} element={<Profile/>}/>
                            <Route path={"/workspace/*"} element={<Workspace/>}/>
                        </Route>
                        <Route path={"/test/*"} element={<TestPage/>}/>
                    </Routes>
                </HashRouter>
            </UserContext.Provider>
        )
}
