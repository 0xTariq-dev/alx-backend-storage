-- script that creates a stored procedure ComputeAverageScoreForUser
-- that computes and store the average score for a student.

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(user_id INT)
BEGIN
    DECLARE total INT DEFAULT 0;
    DECLARE count INT DEFAULT 0;
    DECLARE average FLOAT DEFAULT 0;

    SELECT SUM(score) INTO total
    FROM corrections
    WHERE user_id = user_id;

    SELECT COUNT(*) INTO count
    FROM corrections
    WHERE user_id = user_id;

    IF count > 0 THEN
        SET average = total / count;

        UPDATE users
        SET average_score = average
        WHERE id = user_id;
    END IF;


END //

DELIMITER ;
