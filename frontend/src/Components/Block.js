import React, {useEffect, useState} from 'react';
import {Accordion, AccordionDetails, AccordionSummary, Paper, Typography} from '@mui/material';
import Wysiwyg from "./Wysiwyg";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import EditIcon from '@mui/icons-material/Edit';
import {Box} from "@mui/system";
import {api} from "../Configs/app.config";


export default function BlockComponent(props) {

    const [content, setContent] = useState(props.block.content)
    const [updateCounter, setUpdateCounter] = useState(20)
    const block = props.block
    const onChange = (data) =>
    {
        props.onCange()
        setContent(data)
        block.content = content
        setUpdateCounter(updateCounter-1)
        if (updateCounter === 0) api.updateBlockData(block.id, content)
    }
    return (
        <div>
            <Accordion sx={{ width:'80%', borderRadius: '10px', marginLeft:'10%', marginBottom:'10px' }}>
                <AccordionSummary
                    expandIcon={<EditIcon />}
                    aria-controls="panel1a-content"
                    id="panel1a-header"
                >
                    <Typography dangerouslySetInnerHTML={{ __html: content}} />
                </AccordionSummary>
                <AccordionDetails sx={{display: 'flex', justifyContent: 'center'}}>
                    <Box sx={{width:'80%', borderRadius: '10px'}}>
                        <Wysiwyg content={content} onChange={onChange}/>
                    </Box>

                </AccordionDetails>
            </Accordion>
            {/*<Accordion sx={{ marginTop: '70px', marginBottom: '0', marginLeft: '20px', marginRight: '20px', borderRadius: '10px' }}>
                <AccordionSummary
                    expandIcon={<EditIcon />}
                    aria-controls="panel1a-content"
                    id="panel1a-header"
                    sx={{ margin: '0', borderRadius: '10px' }}
                >
                    <Typography dangerouslySetInnerHTML={{ __html: content}} />
                </AccordionSummary>
                <AccordionDetails sx={{ margin: '0', borderRadius: '10px', marginLeft: '20px', marginRight: '20px' }}>
                    <Wysiwyg content={content} onChange={(data) => setContent(data)}/>
                </AccordionDetails>
            </Accordion>*/}
            {/*<Paper elevation={3} sx={{ padding: '1rem', margin: "40px", borderRadius: "10px" }}>
                <Typography dangerouslySetInnerHTML={{ __html: content}} />
            </Paper>
            <Wysiwyg content={content} onChange={(data) => setContent(data)}/>*/}
        </div>
    );
};