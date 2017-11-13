-- Assignment: Friendships
-- Using the below ERD, write the SQL query that returns a list of users along with their friends names

-- first iteration
SELECT *
FROM users
LEFT JOIN friendships ON user_id = friendships.user_id
LEFT JOIN users AS users2 ON users2.id = friendships.friend_id
ORDER BY users.first_name;

-- second iteration
SELECT users.first_name, users.last_name, users2.first_name, users2.last_name
FROM users
LEFT JOIN friendships ON user_id = friendships.user_id
LEFT JOIN users AS users2 ON users2.id = friendships.friend_id
ORDER BY users.first_name;

-- final iteration with appropriate column renames
SELECT users.first_name, users.last_name, users2.first_name as friend_first_name, users2.last_name as friend_last_name -- renaming the users2 columns
FROM users
LEFT JOIN friendships ON user_id = friendships.user_id -- joining the friendships table to the users table via user_id
LEFT JOIN users AS users2 ON users2.id = friendships.friend_id -- joining the users table BACK to the friendships table by setting AS users2 and via friend_id
ORDER BY users.first_name;

-- Take note that we're joining the users table again but we're specifying the second users table as user2.  
-- You can then reference the second users by calling user2 (e.g. user2.id, user2.first_name, etc).  

-- Knowing how to do joins can be tricky but is used quite often and will most likely appear again in your belt exam!
