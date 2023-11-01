import React from 'react';
import Button from '@mui/material/Button';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Stack from '@mui/material/Stack';
import Toolbar from '@mui/material/Toolbar';
import AppBar from '@mui/material/AppBar';
import Typography from '@mui/material/Typography';
import {Box} from "@mui/system";


export default function AppNavbar(props) {
    const [anchorEl, setAnchorEl] = React.useState(null);

    const handleMenuOpen = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleMenuClose = () => {
        setAnchorEl(null);
    };

    function getLeftPanel() {

        let base =
            <Typography variant="h6"
                        component="a"
                        href="/"
                        sx={{flexGrow: 1, color: '#423e42'}}>
                Home
            </Typography>

        if (!props.user === null) {
            return (
                <>
                    <Stack>
                        {base}
                        {props.user.wiki_api_client.responsibility === 'ADMIN' ? (
                            <Button sx={{color: '#423e42', ':hover': {backgroundColor: '#bd97b6'}, background: '#d4b0ce'}}
                                    variant="contained" href="#admin">
                                Admin Tools
                            </Button>
                        ) : null}
                        <Button sx={{color: '#423e42', ':hover': {backgroundColor: '#bd97b6'}, background: '#d4b0ce'}}
                                variant="contained" href="#workspace">
                            Go to workspaces
                        </Button>
                    </Stack>
                </>
            )
        } else return base
    }

    function getRightPanel() {
        if (props.user === null) {
            return (
                <Stack direction="row" spacing={2}>
                    <Button sx={{color: '#423e42', ':hover': {backgroundColor: '#bd97b6'}, background: '#d4b0ce'}}
                            variant="contained" href="#login">
                        Login
                    </Button>
                    <Button sx={{color: '#423e42', ':hover': {backgroundColor: '#bd97b6'}, background: '#d4b0ce'}}
                            variant="contained" href="#signup">
                        Sign Up
                    </Button>
                </Stack>
            );
        } else {
            return (
                <Stack direction="row">
                    <Button
                        variant="contained"
                        onClick={handleMenuOpen}
                        id="user-dropdown"

                    >
                        {props.user.username}
                    </Button>
                    <Menu
                        anchorEl={anchorEl}
                        open={Boolean(anchorEl)}
                        onClose={handleMenuClose}
                        anchorOrigin={{
                            vertical: 'bottom',
                            horizontal: 'right',
                        }}
                        transformOrigin={{
                            vertical: 'top',
                            horizontal: 'right',
                        }}
                    >
                        <MenuItem href="#profile" onClick={handleMenuClose}>
                            Profile
                        </MenuItem>
                        <MenuItem href="#logout" onClick={handleMenuClose}>
                            Logout
                        </MenuItem>
                    </Menu>
                </Stack>
            );
        }
    }

    return (
        <>
            <Box sx={{flexGrow: 1}}>
                <AppBar position="fixed" sx={{background: '#d4b0ce'}}>
                    <Toolbar sx={{background: '#d4b0ce'}}>
                        {getLeftPanel()}
                        {getRightPanel()}
                    </Toolbar>
                </AppBar>
            </Box>
        </>
    )
}
