import React from "react";
import {api} from "../Config/app.config";
import {Grid} from "@mui/material";
import {Route, Routes, useParams} from "react-router-dom";
import ListBlocks from "../Components/ListBlocks";
import {Sidebar} from "../Components/Sidebar/index"

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
};
