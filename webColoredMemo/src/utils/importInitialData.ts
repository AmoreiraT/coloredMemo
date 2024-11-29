// src/utils/importInitialData.ts
import initialData from '../../../arquivoPublico/metadata.json'; // seu array de metadados
import { createPhotoRepository } from '../repositories/PhotoRepository';

export const importInitialData = async () => {
    const photoRepository = createPhotoRepository();

    for (const photo of initialData) {
        await photoRepository.add({
            ...photo,
            status: 'pending',
            url_imagem_colorida: '',
            colorizedUrl: '',
            description: ''
        });
    }
};