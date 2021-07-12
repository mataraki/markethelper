-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Get the description of the crime by the date and the place
SELECT description FROM crime_scene_reports WHERE
year = 2020
AND month = 7
AND day = 28
AND street = "Chamberlin Street";
-- Descripiton is "Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse.
-- Interviews were conducted today with three witnesses who were present at the time — each of their interview transcripts mentions the courthouse."

-- Get transcripts of the interviews from that day
SELECT name, transcript FROM interviews WHERE
year = 2020
AND month = 7
AND day = 28;
-- Info I got was: within ten minutes of the theft thief left the courthouse and drove away, at the same time he called someone to buy him a ticket to the earliest flight the day after.
-- At the same day thief withdrew some money from the ATM on Fifer street.

-- First, let's look at the ATM transactions from that day and location and find out the names, the numbers and license plates of all matching people
SELECT name, phone_number, license_plate FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE
year = 2020
AND month = 7
AND day = 28
AND transaction_type = "withdraw"
AND atm_location = "Fifer Street"));
--Bobby | (826) 555-1652 | 30G67EN
--Elizabeth | (829) 555-5269 | L93JTIZ
--Victoria | (338) 555-6650 | 8X428L0
--Madison | (286) 555-6063 | 1106N58
--Roy | (122) 555-4581 | QX4YZN3
--Danielle | (389) 555-5198 | 4328GD8
--Russell | (770) 555-1861 | 322W7JE
--Ernest | (367) 555-5533 | 94KL13X

-- Let's check who left the courthouse parking at that morning
SELECT license_plate FROM courthouse_security_logs WHERE
year = 2020
AND month = 7
AND day = 28
AND hour < 11
AND hour > 9
AND minute < 30
AND activity = "exit"
AND license_plate IN ("30G67EN", "L93JTIZ", "8X428L0", "1106N58", "QX4YZN3", "4328GD8", "322W7JE", "94KL13X");
-- So, it's Ernest, Danielle, Elizabeth and Russell

-- Now let's check who of them had a brief phone call that day
SELECT caller, receiver FROM phone_calls WHERE
year = 2020
AND month = 7
AND day = 28
AND duration < 60
AND caller IN ("(367) 555-5533", "(389) 555-5198", "(829) 555-5269", "(770) 555-1861", "(286) 555-6063");
-- It was two of them:
-- (367) 555-5533 | (375) 555-8161
-- (770) 555-1861 | (725) 555-3243
-- Ernest and Russell

-- Let's see what was the earliest flight from Fiftyville on July 29 that year
SELECT id, destination_airport_id FROM flights WHERE
year = 2020
AND month = 7
AND day = 29
AND origin_airport_id IN (SELECT id FROM airports WHERE city = "Fiftyville")
ORDER BY hour, minute;
-- It was a flight with id 36 to the airport with id 4

-- Which is
SELECT city FROM airports WHERE id = 4;
-- London

-- Now let's see who of them flew away on that flight
SELECT name FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36)
AND name IN ("Ernest", "Russell");
-- Ernest

-- Now let's find out who did he called
SELECT name FROM people WHERE phone_number = "(375) 555-8161";
-- Berthold helped him

-- Case closed