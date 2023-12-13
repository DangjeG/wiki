import React, {useEffect, useState} from "react";
import {api} from "../Config/app.config";
import BlockComponent from "../Components/Block/Block";
import Button from "@mui/material/Button";
import Sidebar from "../Components/Sidebar";
import {Grid, Tooltip} from "@mui/material";
import SaveAltIcon from "@mui/icons-material/SaveAlt";
import AddIcon from "@mui/icons-material/Add";
import ImageIcon from '@mui/icons-material/Image';
import {Route, Routes, useParams} from "react-router-dom";
import ListBlocks from "../Components/ListBlocks";


export default function WorkspaceDocs (){

    return (
        <>
            <Grid container spacing={0} style={{ marginTop:'70px', height: '100vh' }}>
                <Grid item xs={3}>
                    <Sidebar/>
                </Grid>
                <Grid item xs={9} sx={{ borderLeft: '1px solid #443C69', marginTop:'10px' }}>

                    <Routes>
                        <Route path={"/"} element={<h1>Выберите документ</h1>}/>
                        <Route path={"/document/:doc_id/:mode"} element={<ListBlocks/>}/>
                    </Routes>
                </Grid>
            </Grid>
        </>
    )
}