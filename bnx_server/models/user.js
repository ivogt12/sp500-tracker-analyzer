const { sql } = require("../config/database");
const bcrypt = require("bcrypt");

const SALT_ROUNDS = 6;

class User {
    static async create({ email, password }) {
        try {
            const hashedPassword = await bcrypt.hash(password, SALT_ROUNDS);
            const request = new sql.Request();
            request.input("email", sql.VarChar, email);
            request.input("password", sql.VarChar, hashedPassword);

            await request.query(`
                INSERT INTO Users (email, password)
                VALUES (@email, @password)
            `);

            return { email };
        } catch (err) {
            throw new Error("Error creating user: " + err.message);
        }
    }

    static async findOne(email) {
        try {
            const request = new sql.Request();
            request.input("email", sql.VarChar, email);

            const result = await request.query(`
                SELECT * FROM Users WHERE email = @email
            `);

            return result.recordset[0] || null;
        } catch (err) {
            throw new Error("Error finding user: " + err.message);
        }
    }
}

module.exports = User;
