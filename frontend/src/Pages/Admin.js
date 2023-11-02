import React, { useState } from 'react';
import Box from '@mui/material/Box';
import Tab from '@mui/material/Tab';
import Tabs from '@mui/material/Tabs';
import UsersTable from '../Components/UsersTable';
import OrganizationsTable from '../Components/OrganizationsTable';

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
                return <OrganizationsTable />;
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
        <Box sx={{ padding: '50px 150px' }}>
            <Tabs textColor="primary" indicatorColor="primary" value={activeTab} onChange={handleTabChange} variant="fullWidth">
                <Tab sx={{color: '#423e42' , ':hover': {backgroundColor: '#cdf'} }} value="users" label="Users" />
                <Tab sx={{color: '#423e42' , ':hover': {backgroundColor: '#cdf'} }} value="organizations" label="Organizations" />
            </Tabs>
            {renderTable()}
        </Box>
    );
}
