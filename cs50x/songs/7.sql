SELECT SUM(energy) / COUNT(energy) AS n FROM songs
JOIN artists ON songs.artist_id = artists.id
WHERE artists.name = 'Drake';
