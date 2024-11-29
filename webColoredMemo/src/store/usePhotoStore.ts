// src/store/usePhotoStore.ts
import { useQuery } from '@tanstack/react-query';
import { PhotoRepository } from '../repositories/PhotoRepository';
import { Photo } from '../types/Photo';

const photoRepository = new PhotoRepository();

export const usePhotos = () => {
    return useQuery<Photo[]>({
        queryKey: ['photos'],
        queryFn: () => photoRepository.getAll()
    });
};

export const usePhotosByStatus = (status: Photo['status']) => {
    return useQuery<Photo[]>({
        queryKey: ['photos', status],
        queryFn: () => photoRepository.getByStatus(status)
    });
};