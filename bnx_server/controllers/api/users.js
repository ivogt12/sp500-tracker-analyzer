const User = require("../../models/user");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcrypt");

module.exports = {
    create,
    login,
};

async function create(req, res) {
    try {
        const user = await User.create(req.body);
        const token = createJWT(user);
        res.json(token);
    } catch (err) {
        res.status(400).json({ error: err.message });
    }
}

async function login(req, res) {
    try {
        const user = await User.findOne(req.body.email);

        if (!user) throw new Error("User not found");

        const match = await bcrypt.compare(req.body.password, user.password);
        console.log("Match: ", match);
        if (!match) throw new Error("Invalid password");
        console.log("User: ", user);

        res.json(createJWT(user));
    } catch (err) {
        res.status(400).json({ error: "Bad Credentials" });
    }
}

function createJWT(user) {
    return jwt.sign(
        { userId: user.id, email: user.email },
        process.env.SECRET,
        { expiresIn: "24h" }
    );
}
