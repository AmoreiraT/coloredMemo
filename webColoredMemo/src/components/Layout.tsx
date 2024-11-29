import React from 'react';
import { AppBar, Toolbar, Typography, CssBaseline, Container } from '@mui/material';

interface LayoutProps {
    children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
    return (
        <>
            <CssBaseline />
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h6">
                        Colored Memo
                    </Typography>
                </Toolbar>
            </AppBar>
            <Container>
                {children}
            </Container>
        </>
    );
};

export default Layout;