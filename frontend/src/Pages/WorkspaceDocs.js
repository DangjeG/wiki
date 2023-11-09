import React, {useEffect, useState} from "react";
import {api} from "../Configs/app.config";
import BlockComponent from "../Components/Block";
import Button from "@mui/material/Button";
import Sidebar from "../Components/Sidebar";
import {Grid, Tooltip} from "@mui/material";
import SaveAltIcon from "@mui/icons-material/SaveAlt";
import AddIcon from "@mui/icons-material/Add";

export default function WorkspaceDocs (props){

    useEffect(() => {
        if (props.workspace_id === "")
            window.location.hash = "#workspace/select"
    }, []);

    const [uncommented, setUncommented] = useState(false)
    const [sidebarOpen, setSidebarOpen] = React.useState(false);
    const [blocks, setBlocks] = useState([]);
    const [documentID, setDocumentID] = useState()
    /*let interval = setInterval(() => console.log("hello"), 1000)*/

    const toggleSidebar = () => {
        setSidebarOpen(!sidebarOpen);
    };


    const handleChange = () => {
        if (!uncommented) {
            {
                setUncommented(true)
            }
        }
    }

    const handleSave = async () => {
        for (let item of blocks)
            await api.updateBlockData(item.id, item.content)
        await api.saveDocument(documentID)
        setUncommented(false)
    }

    const fetchData = async (ID) => {
        try {
            const response = await api.getBlocks(ID)
            setBlocks(response)
            setDocumentID(ID)
        }
        catch (e){
            console.log(e)
        }
    };

    const switchDocument = (ID) => {
        setBlocks([])
        fetchData(ID);
    }

    const handleAdd = async () => {
        await api.addBlock(documentID,0 , "TEXT")
        fetchData(documentID)
        setUncommented(true)
    }
 
    return (
        <>
            <Grid container spacing={0} style={{ marginTop:'70px', height: '100vh' }}>
                <Grid item xs={3}>
                    <Sidebar onSelect={switchDocument} workspaceID={props.workspace_id} open={sidebarOpen} onClose={toggleSidebar}/>
                </Grid>
                <Grid item xs={9} sx={{ borderLeft: '1px solid #443C69', marginTop:'10px' }}>
                    <Button id="base-button" disabled={!uncommented} sx={{marginTop:'20px', marginBottom:'20px', marginLeft: '80%'}} onClick={handleSave}>
                        Сохранить
                        <SaveAltIcon/>
                    </Button>
                    <Button sx={{border: 'none', outline: 'none' }}
                            variant="outlined" onClick={handleAdd}>
                        <Tooltip sx={{width: '10px', height: '10px'}}
                                 title="Добавить блок"
                                 placement="top"
                                 arrow>
                            <AddIcon sx={{color: '#000000'}}/>
                        </Tooltip>
                    </Button>
                    {blocks.map((item) =>{
                        return <BlockComponent onCange={handleChange} block={item}/>
                    })}
                </Grid>
            </Grid>

        </>
    )
}