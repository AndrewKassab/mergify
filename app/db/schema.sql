CREATE TABLE Users (user_id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, username VARCHAR(100) UNIQUE, auth_token VARCHAR(500));
CREATE TABLE Tokens (user_id INTEGER NOT NULL AUTO_INCREMENT, access_token TEXT, expiration_time INTEGER, refresh_token VARCHAR(500), PRIMARY KEY(user_id), FOREIGN KEY (user_id) REFERENCES Users(user_id));
