const SavedData = require('../../models/SavedData');

module.exports = {
    saveUserData,
    getSavedUserData
};

async function saveUserData(req, res) {
    const { stockSymbol, scrapedData, plots } = req.body;
    const userEmail = req.user.email; // Assumes user email is in req.user set by auth middleware

    try {
        const result = await SavedData.saveData({ userEmail, stockSymbol, scrapedData, plots });
        res.status(200).json(result);
    } catch (error) {
        console.error("Error saving user data:", error.message);
        res.status(500).json({ message: "Error saving stock data." });
    }
}

async function getSavedUserData(req, res) {
    const userEmail = req.user.email; // Assumes user email is in req.user set by auth middleware

    try {
        const savedData = await SavedData.getSavedData(userEmail);
        res.status(200).json(savedData);
    } catch (error) {
        console.error("Error retrieving saved data:", error.message);
        res.status(500).json({ message: "Error retrieving saved data." });
    }
}
