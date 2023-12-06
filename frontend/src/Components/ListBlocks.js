import Button from "@mui/material/Button";
import SaveAltIcon from "@mui/icons-material/SaveAlt";
import {Tooltip} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import ImageIcon from "@mui/icons-material/Image";
import BlockComponent from "./Block";
import React, {useEffect, useState} from "react";
import {api} from "../Config/app.config";
import {useParams} from "react-router-dom";


export default function ListBlocks() {

    const [uncommented, setUncommented] = useState(false)
    const [blocks, setBlocks] = useState([]);
    const [documentID, setDocumentID] = useState(null)
    let {doc_id, mode} = useParams();

    useEffect(() => {
        fetchBlocks(doc_id)
    }, [doc_id]);

    const fetchBlocks = async (ID) => {
        try {
            setBlocks([])
            const response = await api.getBlocks(ID)
            setBlocks(response)
            setDocumentID(ID)
        } catch (e) {
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
            if (item.type_block === "TEXT")
                await api.updateTextBlockData(item.id, item.content)
        await api.saveDocument(documentID)
    }
    const handleDelete = async (block) => {
        await api.deleteBlock(block.id)
        fetchBlocks(documentID);
        setUncommented(true)
    }

    const handleAddText = async () => {
        await api.addBlock(documentID, 0, "TEXT")
        fetchBlocks(documentID)
        setUncommented(true)
    }
    const handleAddImage = async () => {
        await api.addBlock(documentID, 0, "IMG")
        fetchBlocks(documentID)
        setUncommented(true)
    }

    /*    const handleShowHistory= async (block) => {
            props.setHistoryBlock(block)
            window.location.href="#workspace/block_history"
        }*/

    return (
        <>
            <Button id="base-button" disabled={!uncommented}
                    sx={{marginTop: '20px', marginBottom: '20px', marginLeft: '80%'}} onClick={handleSave}>
                Сохранить
                <SaveAltIcon/>
            </Button>
            <Button sx={{border: 'none', outline: 'none'}}
                    variant="outlined" onClick={handleAddText}>
                <Tooltip sx={{width: '10px', height: '10px'}}
                         title="Добавить text блок"
                         placement="top"
                         arrow>
                    <AddIcon sx={{color: '#000000'}}/>
                </Tooltip>
            </Button>
            <Button sx={{border: 'none', outline: 'none'}}
                    variant="outlined" onClick={handleAddImage}>
                <Tooltip sx={{width: '10px', height: '10px'}}
                         title="Добавить image блок"
                         placement="top"
                         arrow>
                    <ImageIcon sx={{color: '#000000'}}/>
                </Tooltip>
            </Button>
            {blocks.map((item) => {
                return <BlockComponent mode={"edit"} onShowHistory={() => {
                }} onDelete={handleDelete} onChange={handleChange} block={item}/>
            })}</>)
}