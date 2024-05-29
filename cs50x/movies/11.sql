SELECT title FROM people, stars, movies, ratings
WHERE people.id = stars.person_id
AND stars.movie_id = movies.id
AND ratings.movie_id = movies.id
AND people.name = 'Chadwick Boseman'
ORDER BY rating DESC
LIMIT 5;