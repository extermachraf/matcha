const express = require('express');
const bcrypt = require('bcrypt');
const { body, validationResult } = require('express-validator');
const jwt = require('jsonwebtoken');
const connectDb = require('../../db/index');
const router = express.Router();

// Register a new user route
router.post('/register', 
    // Validation and sanitization
    [
        body('email').isEmail().withMessage('Must be a valid email').normalizeEmail(),
        body('username').isLength({ min: 3 }).withMessage('Username must be at least 3 characters long').trim().escape(),
        body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters long')
    ],
    async (req, res) => {
        const errors = validationResult(req); // Check for validation errors
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }

        const { email, username, password } = req.body;
        const db = await connectDb();

        try {
            // Check if the user already exists
            const existingUser = await db.oneOrNone('SELECT * FROM users WHERE email = $1 OR username = $2', [email, username]);
            
            if (existingUser) {
                return res.status(400).json({ error: 'User with this email or username already exists.' });
            }

            // Hash the password
            const hashedPassword = await bcrypt.hash(password, 10);

            // Save the new user to the database, but don't consider them fully registered yet
            const newUser = await db.one(
                'INSERT INTO users(email, username, password_hash) VALUES($1, $2, $3) RETURNING *', 
                [email, username, hashedPassword]
            );

            console.log('User created, starting token generation');

            // Generate access token
            const accessToken = jwt.sign({ id: newUser.id, email: newUser.email }, process.env.JWT_SECRET, { expiresIn: '15m' });
            console.log('Access token generated:', accessToken);

            // Generate refresh token
            const refreshToken = jwt.sign({ id: newUser.id, email: newUser.email }, process.env.JWT_SECRET, { expiresIn: '7d' });
            console.log('Refresh token generated:', refreshToken);

            // Store the refresh token in the database
            try {
                await db.none('UPDATE users SET refresh_token = $1 WHERE id = $2', [refreshToken, newUser.id]);
                console.log('Refresh token successfully stored');
            } catch (error) {
                console.error('Error storing refresh token:', error);
                // If storing the refresh token fails, delete the user and respond with an error
                await db.none('DELETE FROM users WHERE id = $1', [newUser.id]);
                return res.status(500).json({ error: 'Failed to store refresh token. User registration rolled back.' });
            }

            // If everything succeeds, respond with tokens
            res.status(201).json({ 
                message: 'User registered successfully!', 
                accessToken, 
                refreshToken 
            });

        } catch (error) {
            console.error('Error registering user:', error);
            res.status(500).json({ error: 'An error occurred while registering the user.' });
        }
    }
);


// router.post('/refresh', async (req, res) => {
//     const { refreshToken } = req.body;
    
//     if (!refreshToken) {
//         return res.status(401).json({ error: 'Refresh token is required.' });
//     }

//     try {
//         const decoded = jwt.verify(refreshToken, process.env.JWT_SECRET);
//         const db = await connectDb();
        
//         // Optionally, check if the refresh token exists in your database
//         const user = await db.one('SELECT * FROM users WHERE id = $1 AND refresh_token = $2', [decoded.id, refreshToken]);
        
//         // If valid, generate a new access token
//         const accessToken = jwt.sign({ id: decoded.id, email: decoded.email }, process.env.JWT_SECRET, { expiresIn: '15m' });

        
//         res.status(200).json({ accessToken });
//     } catch (error) {
//         console.error('Invalid refresh token:', error);
//         res.status(403).json({ error: 'Invalid refresh token.' });
//     }
// });

module.exports = router;