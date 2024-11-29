import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { ConfigProvider, Form, Input, Button as AntButton } from 'antd';
import 'antd/dist/reset.css';
import { Button as MuiButton } from '@mui/material';
import Layout from './components/Layout';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <ConfigProvider>
        <Layout>
          <div style={{ padding: '20px' }}>
            <MuiButton variant="contained" color="primary">Material Button</MuiButton>
            <AntButton type="primary" style={{ marginLeft: '10px' }}>Ant Design Button</AntButton>
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
          </div>
        </Layout>
      </ConfigProvider>
    </ThemeProvider>
  );
}

export default App;