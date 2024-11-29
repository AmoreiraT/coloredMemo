// src/commands/usePhotoCommands.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { Photo, PhotoRepository } from '../repositories/PhotoRepository'

const photoRepository = new PhotoRepository()

export const useAddPhoto = () => {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: (photo: Omit<Photo, 'id'>) => photoRepository.add(photo),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['photos'] })
        }
    })
}