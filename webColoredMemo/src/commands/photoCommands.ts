
// src/commands/photoCommands.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { PhotoRepository } from '../repositories/PhotoRepository';
import { Photo } from '../types/Photo';

const photoRepository = new PhotoRepository();

export const useAddPhoto = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (photo: Omit<Photo, 'id'>) => photoRepository.add(photo),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['photos'] });
        }
    });
};

export const useUpdatePhoto = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, data }: { id: string; data: Partial<Photo> }) =>
            photoRepository.update(id, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['photos'] });
        }
    });
};

export const useDeletePhoto = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => photoRepository.delete(id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['photos'] });
        }
    });
};