import TextBlock from "./components/view/TextBlock";
import ImageBlock from "./components/view/ImageBlock";
import {Accordion, AccordionDetails, AccordionSummary, Button, IconButton} from "@mui/material";
import {Delete} from "@mui/icons-material";
import HistoryIcon from '@mui/icons-material/History';
import EditIcon from "@mui/icons-material/Edit";
import {Box} from "@mui/system";
import Wysiwyg from "./components/editor/Wysiwyg";
import React, {useState} from "react";
import FileUploader from "./components/editor/FileUploader";
import "../../Styles/Block.css"
import Menu from "@mui/material/Menu";
import MoreVertIcon from '@mui/icons-material/MoreVert';
import MenuItem from "@mui/material/MenuItem";


export default function BlockComponent(props) {

    const [showEditor, setShowEditor] = useState(false)
    const [block, setBlock] = useState(props.block)
    const [anchorEl, setAnchorEl] = useState(null);
    const handleClick = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };

    const [showMenu, setShowMenu] = useState(false);

    const handleMouseEnter = () => {
        setShowMenu(true);
    };

    const handleMouseLeave = () => {
        setShowMenu(false);
    };


    const getBlockView = () =>{
        switch(block.type_block) {
            case 'TEXT':
            return <TextBlock block={block}/>
            case 'IMG':
                return <ImageBlock block={block} />
        }
    }

    const getBlockEditor = () => {
        switch(block.type_block) {
            case 'TEXT':
                return <Wysiwyg block={block} onChange={handleChange}/>
            case 'IMG':
                return <FileUploader block={block} onChange={handleChange}/>
        }
    }

    const getTools = () => {
        switch(props.mode) {
            case 'view':
                return(
                    <div style={{float: 'right'}}>
                        <MenuItem onClick={handleShowHistory}>
                            <HistoryIcon/>
                        </MenuItem>
                    </div>
                )
            case 'edit':
                return(
                    <div >
                        <MenuItem onClick={handleDelete}>
                            <Delete/>
                        </MenuItem>
                        <MenuItem onClick={handleShowHistory}>
                            <HistoryIcon/>
                        </MenuItem>
                        <MenuItem onClick={handleShowEditor}>
                            <EditIcon/>
                        </MenuItem>
                    </div>
            /*case 'version':
                return (
                    <div style={{float: 'right'}}>
                        <IconButton onClick={handleDelete}>
                            <Delete/>
                        </IconButton>
                    </div>*/
                )
        }
    }

    const handleAddAbove = () => {
        //props.onAddAbove(block)
    }

    const handleAddBelow = () => {
        //props.onAddBelow(block)
    }

    const handleMoveDown = () => {
        //props.onMoveDown(block)
    }

    const handleMoveUp = () => {
        //props.onMoveUp(block)
    }

    const handleDelete = () => {
        props.onDelete(block)
    }

    const handleShowHistory = () => {
        props.onShowHistory(block)
    }

    const handleShowEditor = () => {
        setShowEditor(!showEditor)
    }

    const handleChange = (newBlock) => {
        setBlock(newBlock)
        props.onChange()
    }


    return (
        <div
            className={"block-container"}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
        >
            {showEditor ?
                <div className={"block-editor"}>
                    {getBlockEditor()}
                </div> :
                <div className={"block-view"}>
                    {getBlockView()}
                </div>
                }
            <div className={showMenu ? "block__toolbar_visibility_visible" : "block__toolbar_visibility_hidden"}>
                <Button onClick={handleClick}>
                    <MoreVertIcon/>
                </Button>
                <Menu
                    open={Boolean(anchorEl)}
                    onClose={handleClose}
                    anchorEl={anchorEl}
                >
                    {getTools()}
                </Menu>
            </div>
        </div>
    )
}