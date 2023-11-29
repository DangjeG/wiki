import React, { useState } from 'react';
import Box from '@mui/material/Box';
import Tab from '@mui/material/Tab';
import Tabs from '@mui/material/Tabs';
import UsersTable from '../Components/UsersTable';
import "../Styles/AdminTools.css";
import ButtonAddUser from "../Components/ModalButton/ButtonAddForUserTable";
import ButtonAddOrganization from "../Components/ModalButton/ButtonAddForOrganizationsTable";
import OrganizationsTable from '../Components/OrganizationsTable';
import {Grid} from "@mui/material";
import {api} from "../Config/app.config";

export default function Admin() {
    const [activeTab, setActiveTab] = useState('users');

    const handleTabChange = (event, newValue) => {
        setActiveTab(newValue);
    };


    const renderTable = () => {
        switch (activeTab) {
            case 'users':
                return <UsersTable />;
            case 'organizations':
                return <OrganizationsTable  />;
            default:
                return null;
        }
    };

    const renderButtonAdd = () => {
        switch (activeTab) {
            case 'users':
                return <ButtonAddUser />;
            case 'organizations':
                return <ButtonAddOrganization />;
            default:
                return null;
        }
    };

    const styles = {
        tabsContainer: {
            display: 'flex',
            justifyContent: 'center',
        },
    };

    return (
        <Box id="box-container">

            <Grid container spacing={1}>
                <Grid item xs={1} >
                    <></>
                </Grid>
                <Grid item xs={11}>
                    <Tabs textColor="primary" indicatorColor="primary" value={activeTab} onChange={handleTabChange} variant="fullWidth">
                        <Tab sx={{color: '#423e42' , ':hover': {backgroundColor: '#cdf'} }} value="users" label="Пользователи" />
                        <Tab sx={{color: '#423e42' , ':hover': {backgroundColor: '#cdf'} }} value="organizations" label="Группы" />
                    </Tabs>
                </Grid>
                <Grid item xs={1} sx={{display: 'flex'}}>
                    {renderButtonAdd()}
                </Grid>
                <Grid item xs={11}>
                    {renderTable()}
                </Grid>
            </Grid>

        </Box>
    );
}
