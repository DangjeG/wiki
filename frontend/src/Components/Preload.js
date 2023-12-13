import {CircularProgress} from "@mui/material";
import React from "react";
import "../Styles/Preload.css"

export default function Preload(){
    return(
        <div className={"preload"}>
            <CircularProgress />
        </div>
    )
}