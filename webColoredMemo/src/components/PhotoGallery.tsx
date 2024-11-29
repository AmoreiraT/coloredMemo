// src/components/PhotoGallery.tsx
import React from 'react'
import { Photo } from '../repositories/PhotoRepository'
import { usePhotos } from '../store/usePhotoStore'

const PhotoGallery = (): JSX.Element => {
  const [photosS, setPhotos] = React.useState<Photo[]>([])
  const { data: photos, isLoading } = usePhotos();

  React.useEffect(() => {
    if (photos) {
      setPhotos(photos)
    }
    console.log(photosS)
  }, [photos])


  return (
    isLoading ? (
      <div>Carregando...</div>
    ) : (
      <div>
        {photos?.map((photo: Photo) => (
          <div key={photo.id}>
            <img src={photo.colorizedUrl} alt={photo.description} />
            <p>{photo.description}</p>
          </div>
        ))}
      </div>
    )
  )
}

export { PhotoGallery }
