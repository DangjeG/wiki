import Sidebar from "../Components/Sidebar";
import React, {useEffect, useState} from "react";
import {api} from "../app.config";
import {List, ListItemButton, ListItemText, ListSubheader} from "@mui/material";
import Button from "@mui/material/Button";




export default function Workspace(){


    useEffect(() => {

    }, []);

    const [sidebarOpen, setSidebarOpen] = React.useState(true);

    const toggleSidebar = () => {
        setSidebarOpen(!sidebarOpen);
    };


    return (
        <>
            <Button onClick={toggleSidebar} variant={"outlined"}> open </Button>
            <Sidebar open={sidebarOpen} onClose={toggleSidebar} />
        </>
    )
}