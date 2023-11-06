import React, {useEffect, useState} from "react";
import {api} from "../app.config";
import BlockComponent from "../Components/Block";
import Button from "@mui/material/Button";
import Sidebar from "../Components/Sidebar";


export default function WorkspaceDocs (props){

    useEffect(() => {
        if (props.workspace_id === "")
            window.location.hash = "#workspace/select"
    }, []);

    const [sidebarOpen, setSidebarOpen] = React.useState(false);
    const [blocks, setBlocks] = useState([]);

    const toggleSidebar = () => {
        setSidebarOpen(!sidebarOpen);
    };

    const resetBlocks = (documentID) => {
        const fetchData = async () => {
            try {
                const response = await api.getBlocks(documentID)
                setBlocks(response)
            }
            catch (e){
                console.log(e)
            }
        };
        fetchData();
    }


    return (
        <>
            {blocks.map((item) =>{
                return <BlockComponent content={item.content}/>
            })}
            <Button sx={{ marginLeft: '8px', color: '#423e42', ':hover': {backgroundColor: '#bd97b6'}, background: '#f5d7f0'}} onClick={toggleSidebar}> open </Button>
            <Sidebar onSelect={resetBlocks} workspaceID={props.workspace_id} open={sidebarOpen} onClose={toggleSidebar}/>
        </>
    )
}