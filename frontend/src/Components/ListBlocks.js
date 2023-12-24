import Button from "@mui/material/Button";
import {Chip, Tooltip} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import SaveIcon from '@mui/icons-material/Save';
import ImageIcon from "@mui/icons-material/Image";
import BlockComponent from "./Block/Block";
import React, {useEffect, useState} from "react";
import {api} from "../Config/app.config";
import {useNavigate, useParams} from "react-router-dom";
import Menu from '@mui/material/Menu';
import TextFieldsIcon from '@mui/icons-material/TextFields';
import MenuItem from '@mui/material/MenuItem';
import Typography from '@mui/material/Typography';
import {
    createTheme,
    responsiveFontSizes,
    ThemeProvider,
} from '@mui/material/styles';
import "../Styles/DocumentSpace.css"
import Preload from "./Preload";
import UndoIcon from "@mui/icons-material/Undo";


export default function ListBlocks() {

    const [docLoad, setDocLoad] = useState(true);
    const [blocksLoad, setBlocksLoad] = useState(true);
    const [anchorEl, setAnchorEl] = useState(null);
    const [uncommented, setUncommented] = useState(false)
    const [blocks, setBlocks] = useState([]);
    const [document, setDocument] = useState(null)
    let {wp_id,doc_id, mode, commit_id} = useParams();
    let theme = createTheme();
    let navigate = useNavigate()

    theme = responsiveFontSizes(theme);

    useEffect(() => {
        setBlocksLoad(true)
        setDocLoad(true)
        fetchBlocks()
        fetchDoc(doc_id)
    }, [doc_id, commit_id]);



    const fetchBlocks = async () => {
        try {
            setBlocks([])
            let response = []
            if (commit_id !== undefined)
                response = await api.getBlocks(doc_id, commit_id)
            else
                response = await api.getBlocks(doc_id)
            setBlocks(response)

        } catch (e) {
            console.log(e)
        }
        setBlocksLoad(false)
    };

    const fetchDoc = async (ID) => {
        try {
            setBlocks([])
            const response = await api.getDocumentsInfo(ID)
            setDocument(response)
        } catch (e) {
            console.log(e)
        }
        setDocLoad(false)
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
        await api.saveDocument(doc_id)
    }
    const handleDelete = async (block) => {
        await api.deleteBlock(block.id)
        setBlocksLoad(true)
        fetchBlocks(doc_id);
    }

    const handleAddText = async () => {
        await api.addBlock(doc_id, 0, "TEXT")
        setBlocksLoad(true)
        fetchBlocks(doc_id)
    }
    const handleAddImage = async () => {
        await api.addBlock(doc_id, 0, "IMG")
        setBlocksLoad(true)
        fetchBlocks(doc_id)
    }

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleRollback = async () => {
        await api.rollbackDoc(doc_id, commit_id)
        navigate(`/workspace/${wp_id}`)
    }

    const renderModeDocInfo = () => {
        switch (mode) {
            case "edit":
                return "Вы редактируете"
            case "view":
                return "Вы в режиме просмотра"
            case "version":
                return "Вы в режиме просмотра версии"
        }
    }

    const renderToolbar = () => {
        switch (mode) {
            case "edit" :
                return (
                    <>
                        <Button
                            // id="base-button"
                             sx={{widh : '40px', height: '40px'}}
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
                        <Button
                            sx={{widh : '40px', height: '40px'}}
                            variant="contained"
                            onClick={handleClick}>
                            <Tooltip sx={{width: '10px', height: '10px'}}
                                     title="Добавить блок"
                                     placement="top"
                                     arrow>
                                <AddIcon sx={{color: '#FFFFFF'}}/>
                            </Tooltip>
                        </Button>
                    </>
                )
            case "version" :
                return (
                    <Button
                        sx={{widh : '40px', height: '40px'}}
                        variant="outlined"
                        onClick={handleRollback}>
                        <Tooltip sx={{width: '10px', height: '10px'}}
                                 title="Откатиться к версии" arrow
                                 placement="top">
                                <UndoIcon sx={{color: '#1976d2'}}/>
                        </Tooltip>
                    </Button>
                )
        }

    }

    return (
        <>
            {docLoad || blocksLoad ? <Preload/> :
                <div className="container">
                    <div className="documentHeader">
                        <ThemeProvider theme={theme}>
                            <Typography
                                variant="h4"
                                style={{"margin-right": "20px"}}
                            >
                                {document? document.title : null}

                            </Typography>
                            <Chip
                                label={renderModeDocInfo()}
                                style={{"margin-right": "auto"}}
                            />
                        </ThemeProvider>
                        {renderToolbar()}
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

                    <div className="blockList">
                        {blocks.map((item) => {
                            // В режиме просмотра пустые блоки не отображаем
                            if (!(mode === "view" && item.content.trim() === "")) {
                                return <BlockComponent mode={mode} onShowHistory={() => {
                                }} onDelete={handleDelete} onChange={handleChange} block={item}/>
                            }
                        })}
                    </div>
                </div>}
        </>
    )
}