# Data-Engineer-Performance-Task
performance task

Provide a SQL query that will answer a queston of your choosing about the data. (Examples: What is the median
age of vehicles? What are stats by region of vehicle manufacturer?)
1. The given query returns phone numbers with repeating characters, such as (718)365-8585
WITH Exploded AS (
    SELECT
        base_telephone_number,
        SUBSTR(base_telephone_number, num, 1) AS char,
        num
    FROM
        your_table_name
    CROSS JOIN UNNEST(SEQUENCE(1, LENGTH(base_telephone_number))) AS t (num)
)

SELECT
    e1.base_telephone_number
FROM
    Exploded e1
JOIN
    Exploded e2
ON
    e1.base_telephone_number = e2.base_telephone_number
    AND e1.char = e2.char
    AND e1.num != e2.num
GROUP BY
    e1.base_telephone_number
HAVING
    COUNT(DISTINCT e1.num) > 1;

  

2. Utilizing AWS Lambda's serverless architecture offers scalability. Storing data in S3 is an efficient approach for data storage management,
   especially when files are converted into formats like CSV, which enhances the querying process. For those familiar with SQL, Athena serves as a highly
   accessible tool and seamlessly integrates with S3. Collectively, executing these operations on AWS provides both scalability and cost-effectiveness.
3. What else would you do if you had more time?
    If I had more time, I would focus on enhancing error management processes and refining the data cataloging system.
