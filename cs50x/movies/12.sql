SELECT title FROM people, stars, movies
WHERE people.id = stars.person_id
AND stars.movie_id = movies.id
AND name = 'Bradley Cooper'
AND title IN
(SELECT title FROM people, stars, movies
WHERE people.id = stars.person_id
AND stars.movie_id = movies.id
AND name = 'Jennifer Lawrence');