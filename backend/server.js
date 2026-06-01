const express = require('express');
const { Pool } = require('pg');
const redis = require('redis');

const app = express();
app.use(express.json());

const pool = new Pool({
    user: 'postgres',
    host: 'db',
    database: 'scores',
    password: 'secret',
    port: 5432
});

const redisClient = redis.createClient({
    url: 'redis://redis:6379'
});

redisClient.connect();

pool.query(`
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    marks INT,
    grade VARCHAR(5)
)
`)
.then(() => console.log("Students table ready"))
.catch(err => console.log(err));

app.post('/calculate', async (req, res) => {
    try {
        const { name, marks } = req.body;

        const percentage = marks;
        let grade;

        if (percentage >= 90) {
            grade = 'A';
        } else if (percentage >= 75) {
            grade = 'B';
        } else {
            grade = 'C';
        }

        await pool.query(
            'INSERT INTO students (name, marks, grade) VALUES ($1, $2, $3)',
            [name, marks, grade]
        );

        await redisClient.setEx(
            name,
            3600,
            JSON.stringify({ marks, grade })
        );

        res.json({
            name,
            percentage,
            grade
        });

    } catch (error) {
        console.error(error);
        res.status(500).json({
            error: error.message
        });
    }
});

app.listen(5000, () => {
    console.log('Backend running on port 5000');
});
