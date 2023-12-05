import {Accordion, AccordionDetails, AccordionSummary, Typography} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import {Box} from "@mui/system";
import Wysiwyg from "./Wysiwyg";
import React, {useState} from "react";


export default function TextBlock({block, onChange}){

    const [content, setContent] = useState(block.content)
    const handleChange = (data) => {
        if (content===data) return
        block.content=data
        setContent(data)
        onChange(block)
    }

    return(
        <div style={{marginLeft:'10%', marginBottom:'10px' }}>
            <Accordion sx={{ width:'80%', borderRadius: '10px' }}>
                <AccordionSummary
                    expandIcon={<EditIcon />}
                    aria-controls="panel1a-content"
                    id="panel1a-header">
                    <Typography dangerouslySetInnerHTML={{ __html: content}} />
                </AccordionSummary>
                <AccordionDetails sx={{display: 'flex', justifyContent: 'center'}}>
                    <Box sx={{width:'100%', borderRadius: '10px'}}>
                        <Wysiwyg sx={{marginLeft:'10%'}} content={content} onChange={handleChange}/>
                    </Box>
                </AccordionDetails>
            </Accordion>
        </div>
    )
}