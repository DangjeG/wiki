import React from 'react';
import { Paper, Typography } from '@mui/material';

export default function BlockComponent(props) {
    return (
        <Paper elevation={3} sx={{ padding: '1rem' }}>
            <Typography dangerouslySetInnerHTML={{ __html: props.content }} />
        </Paper>
    );
};
