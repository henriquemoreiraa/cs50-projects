SELECT DISTINCT p.name
FROM people p
JOIN stars s1 ON p.id = s1.person_id
JOIN stars s2 ON s1.movie_id = s2.movie_id
JOIN people kevin_bacon ON kevin_bacon.id = s2.person_id
WHERE kevin_bacon.name = 'Kevin Bacon'
AND kevin_bacon.birth = 1958
  AND p.name != 'Kevin Bacon';