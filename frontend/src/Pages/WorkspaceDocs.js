import React, {useEffect, useState} from "react";
import {api} from "../Config/app.config";
import BlockComponent from "../Components/Block";
import Button from "@mui/material/Button";
import Sidebar from "../Components/Sidebar";
import {Grid, Tooltip} from "@mui/material";
import SaveAltIcon from "@mui/icons-material/SaveAlt";
import AddIcon from "@mui/icons-material/Add";

export default function WorkspaceDocs (props){

    const [uncommented, setUncommented] = useState(false)
    const [blocks, setBlocks] = useState([]);
    const [documentID, setDocumentID] = useState(null)
    /*let interval = setInterval(() => console.log("hello"), 1000)*/

    const [blockVersions, setBlockVersions] = useState([])

    useEffect(() => {
        if (props.workspace_id === "")
            window.location.hash = "#workspace/select"

    }, []);

    const fetchVersions = async (block_id) => {
        let versionsInfo = []
        let versions = []
        try {
            versionsInfo = await api.getBlockVersions(block_id)
        }
        catch (e){
            console.log(e)
        }
        for (let version of versionsInfo){
            try {
                version.push(api.getBlockData(block_id, version.commit_id))
            }
            catch (e){
                console.log(e)
            }
        }
        setBlockVersions(versions)
    }

    const fetchBlocks = async (ID) => {
        try {
            const response = await api.getBlocks(ID)
            setBlocks(response)
            setDocumentID(ID)
        }
        catch (e){
            console.log(e)
        }
    };

    const handleChange = () => {
        if (!uncommented) {
            {
                setUncommented(true)
            }
        }
    }

    const handleSave = async () => {
        setUncommented(false)
        for (let item of blocks)
            await api.updateBlockData(item.id, item.content)
        await api.saveDocument(documentID)
    }

    const switchDocument = (ID) => {
        setBlocks([])
        fetchBlocks(ID);
        fetchVersions(blocks[0].id)
        alert(blockVersions.length)
    }

    const handleAdd = async () => {
        await api.addBlock(documentID,0 , "TEXT")
        fetchBlocks(documentID)
        setUncommented(true)
    }

    return (
        <>
            <Grid container spacing={0} style={{ marginTop:'70px', height: '100vh' }}>
                <Grid item xs={3}>
                    <Sidebar onSelect={switchDocument} workspaceID={props.workspace_id}/>
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
                        return <BlockComponent onChange={handleChange} block={item}/>
                    })}
                </Grid>
            </Grid>
        </>
    )
}