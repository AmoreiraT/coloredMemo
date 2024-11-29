// src/store/usePhotoStore.ts
import { useQuery } from '@tanstack/react-query';
import { createPhotoRepository } from '../repositories/PhotoRepository';
import { Photo } from '../types/Photo';

const photoRepository = createPhotoRepository();

export const usePhotos = () => {


  return useQuery<Photo[]>({
    queryKey: ['photos'],
    queryFn: async () => {
      const res = await photoRepository.getAll();

      return res;
    }
  });
};