// src/utils/importInitialData.ts
import initialData from '../../../arquivoPublico/metadata.json'; // seu array de metadados
import { PhotoRepository } from '../repositories/PhotoRepository';

export const importInitialData = async () => {
    const photoRepository = new PhotoRepository();

    for (const photo of initialData) {
        await photoRepository.add({
            ...photo,
            status: 'pending',
            url_imagem_colorida: undefined
        });
    }
};