import React from 'react';
import { useQuery, useMutation, QueryClientProvider } from 'react-query';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { ConfigProvider, Form, Input, Button as AntButton } from 'antd';
import 'antd/dist/reset.css';
import { Button as MuiButton } from '@mui/material';
import Layout from './components/Layout';
import { firestoreCommands } from './commands/firestoreCommands';
import { queryClient } from './queryClient';
import { useFirestoreStore } from './store';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
  },
});

interface Document {
  id: string;
  name: string;
  email: string;
}

const App: React.FC = () => {
  const { documents, addDocument, removeDocument } = useFirestoreStore<Document>();

  const fetchDocuments = useQuery('documents', async () => {
    const response = await firestoreCommands.read<Document>('your-collection', 'documentId');
    return response;
  });

  const createMutation = useMutation(
    (newDoc: Document) => firestoreCommands.create<Document>('your-collection', newDoc),
    {
      onSuccess: (data) => {
        addDocument(data);
      },
    }
  );

  const handleSubmit = (values: any) => {
    createMutation.mutate(values);
  };

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <ConfigProvider>
          <Layout>
            <div style={{ padding: '20px' }}>
              <MuiButton variant="contained" color="primary">Material Button</MuiButton>
              <Form onFinish={handleSubmit} style={{ marginTop: '20px' }}>
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
              <div>
                {fetchDocuments.data?.map((doc) => (
                  <div key={doc.id}>
                    <p>{doc.name}</p>
                    <p>{doc.email}</p>
                    <MuiButton onClick={() => removeDocument(doc.id)}>Delete</MuiButton>
                  </div>
                ))}
              </div>
            </div>
          </Layout>
        </ConfigProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;