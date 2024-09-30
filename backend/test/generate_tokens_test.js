const { process_params } = require('express/lib/router');
const jwt = require('jsonwebtoken');
require('dotenv').config(); // Load environment variables

const user = {
    id:1,
    email: "testuser@example.cim"
};

// secret key for JWT from environment variable
const jwtSecret = process.env.JWT_SECRET;
console.log('JWT Secret:', jwtSecret);

// Function to generate boh access and refresh tokens
function generateTokens(user) {
    try {
        // generate access token
        const accessToken = jwt.sign({ id: user.id, email: user.email }, jwtSecret, { expiresIn: '15m' });
        const refreshToken = jwt.sign({ id: user.id, email: user.email }, jwtSecret, { expiresIn: '7d' });
        return {accessToken, refreshToken};
    } catch (error) {
        console.error('Error generating tokens:', error);
        return null;
    }
};


const tokens = generateTokens(user);

if(tokens) {
    console.log("Access Token:", tokens.accessToken);
    console.log("Refresh Token:", tokens.refreshToken);
} else {
    console.log("Token generation failed.");
}