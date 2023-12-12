import Button from "@mui/material/Button";
import SaveAltIcon from "@mui/icons-material/SaveAlt";
import {MenuList, Tooltip} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import SaveIcon from '@mui/icons-material/Save';
import ImageIcon from "@mui/icons-material/Image";
import BlockComponent from "./Block/Block";
import React, {useEffect, useState} from "react";
import {api} from "../Config/app.config";
import {useParams} from "react-router-dom";
import Menu from '@mui/material/Menu';
import TextFieldsIcon from '@mui/icons-material/TextFields';
import MenuItem from '@mui/material/MenuItem';
import Styles from '../Styles/DocumentSpace.css';
import Grid from '@mui/material/Unstable_Grid2';
import Typography from '@mui/material/Typography';
import {
    createTheme,
    responsiveFontSizes,
    ThemeProvider,
  } from '@mui/material/styles';


export default function ListBlocks() {

    const [anchorEl, setAnchorEl] = useState(null);
    const [isHovered, setIsHovered] = useState(false);

    const [uncommented, setUncommented] = useState(false)
    const [blocks, setBlocks] = useState([]);
    const [documentID, setDocumentID] = useState(null)
    let {doc_id, mode} = useParams();

    let theme = createTheme();

    theme = responsiveFontSizes(theme);

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

    //

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };
    
    const handleClose = () => {
        setAnchorEl(null);
    };

    /*    const handleShowHistory= async (block) => {
            props.setHistoryBlock(block)
            window.location.href="#workspace/block_history"
        }*/

    return (
        <div className="Styles.container" class="container">
            <div className="Styles.documentHeader" class="documentHeader">
                <ThemeProvider theme={theme}>
                    <Typography variant="h5">
                        {documentID ? documentID: null}
                    </Typography>
                </ThemeProvider>
                <Button 
                        // id="base-button" 
                        // sx={{marginTop: '20px', marginBottom: '20px', marginLeft: '80%'}}
                        variant="outlined"
                        disabled={!uncommented}
                        onClick={handleSave}>
                    <Tooltip sx={{width: '10px', height: '10px'}}
                            title="Сохранить"
                            placement="top"
                            arrow>
                        <SaveIcon sx={{color: '#1976d2'}}/>
                    </Tooltip>
                </Button>
                <Button variant="contained" 
                        onClick={handleClick}>
                    <Tooltip sx={{width: '10px', height: '10px'}}
                            title="Добавить блок"
                            placement="top"
                            arrow>
                        <AddIcon sx={{color: '#FFFFFF'}}/>
                    </Tooltip>
                </Button>
                <Menu
                    anchorEl={anchorEl}
                    open={Boolean(anchorEl)}
                    onClose={handleClose}
                >
                    <MenuItem onClick={handleClose}>
                        <Button sx={{border: 'none', outline: 'none'}}
                                variant="outlined" onClick={handleAddText}>
                            <Tooltip sx={{width: '10px', height: '10px'}}
                                    title="Добавить текстовый блок"
                                    placement="top"
                                    arrow>
                                <TextFieldsIcon sx={{color: '#000000'}}/>
                            </Tooltip>
                        </Button>
                    </MenuItem>
                    <MenuItem onClick={handleClose}>
                        <Button sx={{border: 'none', outline: 'none'}}
                                variant="outlined" onClick={handleAddImage}>
                            <Tooltip sx={{width: '10px', height: '10px'}}
                                    title="Добавить блок с изображением"
                                    placement="top"
                                    arrow>
                                <ImageIcon sx={{color: '#000000'}}/>
                            </Tooltip>
                        </Button>
                    </MenuItem>
                </Menu>
            </div>
            
            <div className="Styles.blockList" class="blockList">
                {blocks.map((item) => {
                    return <BlockComponent mode={"edit"} onShowHistory={() => {
                    }} onDelete={handleDelete} onChange={handleChange} block={item}/>
                })}
            </div>
        </div>
    )
}