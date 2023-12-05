import TextBlock from "./TextBlock";
import ImageBlock from "../ImageBlock";
import {IconButton} from "@mui/material";
import {Delete} from "@mui/icons-material";
import HistoryIcon from '@mui/icons-material/History';

export default function BlockComponent(props) {

    const block = props.block

    const getBlockView = () =>{
        switch(block.type_block) {
            case 'TEXT':
            return <TextBlock block={block} onChange={props.onChange}/>
            case 'IMG':  // if (x === 'value2')
                return <ImageBlock block={block} onChange={props.onChange}/>
        }
    }
    const getTools = () => {
        switch(props.mode) {
            case 'edit':
                return(
                    <div style={{float: 'right'}}>
                        <IconButton onClick={handleDelete}>
                            <Delete/>
                        </IconButton>
                        <IconButton onClick={handleShowHistory}>
                            <HistoryIcon/>
                        </IconButton>
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

    return (
        <div>
            {getBlockView()}
            {getTools()}
        </div>
    )
}