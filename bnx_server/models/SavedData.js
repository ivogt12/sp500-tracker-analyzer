const { sql } = require("../config/database");

class SavedData {
    static async saveData({ userEmail, stockSymbol, scrapedData, plots }) {
        try {
            const request = new sql.Request();
            request.input("userEmail", sql.VarChar, userEmail);
            request.input("stockSymbol", sql.VarChar, stockSymbol);
            request.input("scrapedData", sql.NVarChar, JSON.stringify(scrapedData));
            request.input("plots", sql.NVarChar, JSON.stringify(plots));

            await request.query(`
                INSERT INTO SavedData (userEmail, stockSymbol, scrapedData, plots)
                VALUES (@userEmail, @stockSymbol, @scrapedData, @plots)
            `);

            return { message: "Stock data saved successfully." };
        } catch (err) {
            throw new Error("Error saving stock data: " + err.message);
        }
    }

    static async getSavedData(userEmail) {
        try {
            const request = new sql.Request();
            request.input("userEmail", sql.VarChar, userEmail);

            const result = await request.query(`
                SELECT * FROM SavedData WHERE userEmail = @userEmail
            `);

            return result.recordset;
        } catch (err) {
            throw new Error("Error retrieving saved data: " + err.message);
        }
    }
}

module.exports = SavedData;
