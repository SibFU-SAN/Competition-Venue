CREATE TABLE IF NOT EXISTS `users` (
    `id` int(5) UNIQUE NOT NULL,
    `login` varchar(32) UNIQUE NOT NULL,
    `password` varchar(32) NOT NULL,
    `wins` int NOT NULL DEFAULT 0,
    `played` int NOT NULL DEFAULT 0,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS `games` (
    `id` int(5) UNIQUE NOT NULL,
    `name` tinytext NOT NULL,
    `start_time` int NOT NULL,
    `end_time` int NOT NULL,
    `period` tinyint NOT NULL,
    `owner` int(5) NOT NULL,
    `status` tinyint NOT NULL DEFAULT 0,
    `private` boolean NOT NULL,
    `settings` JSON NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS `players` (
    `id` int(5) UNIQUE NOT NULL,
    `game` int(5) NOT NULL,
    `user` int(5) NOT NULL,
    PRIMARY KEY(id)
);
