
// src/commands/photoCommands.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { createPhotoRepository } from '../repositories/PhotoRepository';
import { Photo } from '../types/Photo';

const photoRepository = createPhotoRepository();

export const useGetAllPhotos = async () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async () => await photoRepository.getAll(),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['photos'] });
        }
    });
}

export const useAddPhoto = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (photo: Omit<Photo, 'id'>) => await photoRepository.add(photo),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['photos'] });
        }
    });
};

export const useUpdatePhoto = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async ({ id, data }: { id: string; data: Partial<Photo> }) =>
            await photoRepository.update(id, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['photos'] });
        }
    });
};

export const useDeletePhoto = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (id: string) => await photoRepository.delete(id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['photos'] });
        }
    });
};