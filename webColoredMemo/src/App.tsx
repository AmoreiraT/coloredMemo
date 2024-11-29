import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { ConfigProvider, Form, Input, Button as AntButton, Switch } from 'antd';
import 'antd/dist/reset.css';
import { Button as MuiButton } from '@mui/material';
import Layout from './components/Layout';
import PhotoCard from './components/PhotoCard';

const App: React.FC = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [photos] = useState([
    { url: 'https://via.placeholder.com/150', description: 'Sample Photo 1' },
    { url: 'https://via.placeholder.com/150', description: 'Sample Photo 2' }
  ]);

  const theme = createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
      primary: {
        main: '#1976d2',
      },
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <ConfigProvider>
        <Layout>
          <div style={{ padding: '20px' }}>
            <MuiButton variant="contained" color="primary">Material Button</MuiButton>
            <AntButton type="primary" style={{ marginLeft: '10px' }}>Ant Design Button</AntButton>
            <div style={{ marginTop: '20px' }}>
              <Switch checked={darkMode} onChange={() => setDarkMode(!darkMode)} /> Toggle Dark Mode
            </div>
            <Form style={{ marginTop: '20px' }}>
              <Form.Item label="Name" name="name">
                <Input />
              </Form.Item>
              <Form.Item label="Email" name="email">
                <Input />
              </Form.Item>
              <Form.Item>
                <AntButton type="primary" htmlType="submit">Submit</AntButton>
              </Form.Item>
            </Form>
            <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
              {photos.map((photo, index) => (
                <PhotoCard key={index} photo={photo} />
              ))}
            </div>
          </div>
        </Layout>
      </ConfigProvider>
    </ThemeProvider>
  );
}

export default App;