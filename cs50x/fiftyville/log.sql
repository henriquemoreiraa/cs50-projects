-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT description FROM crime_scene_reports WHERE
month = 07 AND
day = 28 AND
year = 2021 AND
street = 'Humphrey Street';

SELECT transcript FROM interviews WHERE
month = 07 AND
day = 28 AND
year = 2021;

SELECT name, receiver, duration FROM phone_calls, people, bank_accounts, atm_transactions
WHERE phone_calls.caller = people.phone_number
AND people.id = bank_accounts.person_id
AND bank_accounts.account_number  = atm_transactions.account_number
AND atm_transactions.month = 07
AND atm_transactions.day = 28
AND atm_transactions.year = 2021
AND phone_calls.month = 07
AND phone_calls.day = 28
AND phone_calls.year = 2021
AND atm_location = 'Leggett Street';

SELECT name, destination_airport_id, hour, minute FROM people, passengers, flights, airports
WHERE people.passport_number = passengers.passport_number
AND passengers.flight_id = flights.id
AND flights.origin_airport_id = airports.id
AND month = 07
AND day = 29
AND year = 2021
AND city = 'Fiftyville'
AND hour = 8;

SELECT city FROM airports WHERE id = 4;

SELECT activity, license_plate FROM bakery_security_logs WHERE
month = 07 AND
day = 28 AND
year = 2021 AND
hour = 10 AND
activity = 'exit';

SELECT name FROM people WHERE phone_number = '(375) 555-8161';

