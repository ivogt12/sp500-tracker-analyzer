const jwt = require("jsonwebtoken");

async function requireAuth(req, res, next) {
    console.log("requireAuth middleware executed"); // Debug log
    const authHeader = req.headers.authorization;

    if (!authHeader) {
        return res.status(401).json({ message: "Authorization header missing." });
    }

    const token = authHeader.split(" ")[1];

    try {
        const payload = jwt.verify(token, process.env.SECRET);
        req.user = payload;
        
        console.log("User in middleware:", req.user); // Debug log
        next();
    } catch (error) {
        return res.status(401).json({ message: "Invalid token." });
    }
}

module.exports = {requireAuth}; // Export the middleware function