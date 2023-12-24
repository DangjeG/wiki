import React from "react";
import {Grid} from "@mui/material";
import {Route, Routes} from "react-router-dom";
import ListBlocks from "../Components/ListBlocks";
import {Sidebar} from "../Components/Sidebar/Sidebar";

export default function WorkspaceDocs () {
    return (
        <>
            <Grid container spacing={0} style={{ marginTop:'70px', height: '100vh' }}>
                <Grid item xs={3}>
                    <Sidebar/>
                </Grid>
                <Grid item xs={9} sx={{ borderLeft: '1px solid #443C69', marginTop:'10px' }}>

                    <Routes>
                        <Route path={"/"} element={<h1>Выберите документ</h1>}/>
                        <Route path={"/document/:doc_id/:mode/:commit_id?"} element={<ListBlocks/>}/>
                    </Routes>
                </Grid>
            </Grid>
        </>
    )
};
