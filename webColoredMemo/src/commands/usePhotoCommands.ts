// src/commands/usePhotoCommands.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { createPhotoRepository, Photo } from '../repositories/PhotoRepository'


export const useAddPhoto = () => {
    const photoRepository = createPhotoRepository()
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn: async (photo: Omit<Photo, 'id'>) => await photoRepository.add(photo),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['photos'] })
        }
    })
}