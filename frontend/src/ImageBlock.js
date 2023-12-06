import {Accordion, AccordionDetails, AccordionSummary, Typography} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import {Box} from "@mui/system";
import Wysiwyg from "./Components/Wysiwyg";
import React, {useState} from "react";
import FileUploader from "./Components/FileUploader";
import {api} from "./Config/app.config";


export default function ImageBlock({block, onChange}){

    const handleChange = (event) => {
        const file = event.target.files[0];

        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                const fileContent = event.target.result;
                const fileBlob = new Blob([fileContent], { type: file.type });
                const formData = new FormData();
                formData.append('file', fileBlob, file.name)

                api.updateFileBlockData(block.id, formData);
            }
            reader.readAsBinaryString(file);
        }

        //Make a request to server and send formData
    }

    return(
        <div style={{marginLeft:'10%', marginBottom:'10px'}}>
            <Accordion sx={{width:'80%', borderRadius: '10px'}}>
                <AccordionSummary
                    expandIcon={<EditIcon />}
                    aria-controls="panel1a-content"
                    id="panel1a-header">
                    <img src={block.link} width="600"/>
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