import React, {useEffect, useState} from 'react';
import {Accordion, AccordionDetails, AccordionSummary, Paper, Typography} from '@mui/material';
import Wysiwyg from "./Wysiwyg";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import EditIcon from '@mui/icons-material/Edit';
import {Box} from "@mui/system";
import TextBlock from "./TextBlock";
import ImageBlock from "../ImageBlock";

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
        //props.onDelete(block)
    }
    
    return (
        getBlockView()
    )
}