SELECT SUM(rating) / COUNT(rating) AS N FROM movies
JOIN ratings ON movies.id = ratings.movie_id
WHERE year = '2012';