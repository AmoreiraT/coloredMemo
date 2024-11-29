// src/types/Photo.ts
export interface Photo {
    colorizedUrl: string | undefined;
    description: string | undefined;
    id: string;
    titulo: string;
    descricao: string;
    referencias: string;
    notacao: string;
    autor: string;
    local: string;
    data: string;
    cor: string;
    dimensao: string;
    notas: string;
    descritores: string;
    url_imagem: string;
    url_imagem_colorida?: string; // Para a versão colorizada pela IA
    nome_arquivo: string;
    status: 'pending' | 'processing' | 'completed'; // Para controlar o estado da colorização
}