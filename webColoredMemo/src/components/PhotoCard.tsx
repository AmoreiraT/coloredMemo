import { Card, CardContent, CardMedia, Typography } from '@mui/material';
import React from 'react';

interface PhotoCardProps {
  photo: {
    url: string;
    description: string;
    colorUrl: string;
  };
}

const PhotoCard: React.FC<PhotoCardProps> = ({ photo }) => {
  return (
    <Card>
      <CardMedia
        component="img"
        height="140"
        image={photo.url}
        alt={photo.description}
        onMouseOver={(e) => (e.currentTarget.src = photo.colorUrl)}
        onMouseOut={(e) => (e.currentTarget.src = photo.url)}
      />
      <CardContent>
        <Typography variant="body2" color="text.secondary">
          {photo.description}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default PhotoCard;