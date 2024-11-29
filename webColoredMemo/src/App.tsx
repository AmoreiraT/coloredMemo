import { Button as MuiButton } from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { QueryClientProvider } from '@tanstack/react-query';
import { ConfigProvider } from 'antd';
import React from 'react';
import { useDeletePhoto } from './commands/photoCommands';
import Layout from './components/Layout';
import { queryClient } from './queryClient';
import { usePhotos } from './store/usePhotoStore';
import { Photo } from './types/Photo';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
  },
});

const App: React.FC = () => {
  const { data: photos, isLoading } = usePhotos();
  const deletePhotoMutation = useDeletePhoto();

  const handleDeletePhoto = async (id: string) => {
    await deletePhotoMutation.mutateAsync(id);
  };

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <ConfigProvider>
          <Layout>
            <div style={{ padding: '20px' }}>
              {isLoading ? (
                <div>Carregando...</div>
              ) : (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '20px' }}>
                  {photos?.map((photo: Photo) => (
                    <div key={photo.id} style={{ border: '1px solid #eee', padding: '10px', borderRadius: '8px' }}>
                      <img
                        src={photo.url_imagem_colorida || photo.url_imagem}
                        alt={photo.descricao || photo.notacao}
                        style={{ width: '100%', height: 'auto' }}
                      />
                      <div>
                        <p><strong>Notação:</strong> {photo.notacao}</p>
                        <p><strong>Local:</strong> {photo.local}</p>
                        <p><strong>Data:</strong> {photo.data}</p>
                        <p><strong>Autor:</strong> {photo.autor}</p>
                        <MuiButton
                          variant="contained"
                          color="secondary"
                          onClick={() => handleDeletePhoto(photo.id)}
                        >
                          Deletar
                        </MuiButton>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </Layout>
        </ConfigProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
};

export { App };
