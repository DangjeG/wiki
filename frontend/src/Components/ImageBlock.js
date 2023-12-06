import {Accordion, AccordionDetails, AccordionSummary, Typography} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import {Box} from "@mui/system";
import Wysiwyg from "./Wysiwyg";
import React, {useState} from "react";
import FileUploader from "./FileUploader";
import {api} from "../Config/app.config";


export default function ImageBlock({block, onChange}){

    const [link, setLink] = useState(block.link)
    const handleChange = (event) => {
        const file = event.target.files[0];

        if (file) {

            let formData = new FormData();
            formData.append('file', file);
            api.updateFileBlockData(block.id, formData).then((link) => {
                setLink(link)
            });

        }
    }

    return(
        <div style={{marginLeft:'10%', marginBottom:'10px'}}>
            <Accordion sx={{width:'80%', borderRadius: '10px'}}>
                <AccordionSummary
                    expandIcon={<EditIcon />}
                    aria-controls="panel1a-content"
                    id="panel1a-header">
                    <img src={link} width="600"/>
                </AccordionSummary>
                <AccordionDetails sx={{display: 'flex', justifyContent: 'center'}}>
                    <Box sx={{width:'100%', borderRadius: '10px'}}>
                        <FileUploader onChange={handleChange}/>
                    </Box>
                </AccordionDetails>
            </Accordion>
        </div>
    )
}