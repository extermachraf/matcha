const jwt = require('jsonwebtoken');
const db = require('../db/index');


const verifyAccessToken = async (req, res, next) => {
    const authHeader = req.headers['authorization'];
    const accessToken = authHeader && authHeader.split(' ')[1];

    if (!accessToken) {
        return checkRefreshToken(req, res, next);
    }
    jwt.verify(accessToken, process.env.JWT_SECRET, async (err, user) => {
        if (err) {
            return checkRefreshToken(req, res, next);
        }

        req.user = user;
        next();
    });
}

const checkRefreshToken = async (req, res, next) => {
    const { refreshToken } = req.body;

    if (!refreshToken) {
        return res.status(401).json({ error: 'Refresh token is required.' });
    }

    try {
        const decodedRefreshToken = jwt.verify(refreshToken, process.env.JWT_SECRET);
        const existingUser = await db.oneOrNone('SELECT * FROM users WHERE id = $1 AND refresh_token = $2', [decodedRefreshToken.id, refreshToken]);
        if (!existingUser) {
            return res.status(403).json({ error: 'Invalid refresh token.' });
        }
        const newAccessToken = jwt.sign({ id: decodedRefreshToken.id, email: decodedRefreshToken.email }, process.env.JWT_SECRET, { expiresIn: '15m' });
        return res.status(200).json({ accessToken: newAccessToken });
    } catch (error) {
        console.error('Invalid refresh token:', error);
        return res.status(403).json({ error: 'Invalid refresh token.' });
    }
};