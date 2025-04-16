// routes/api/saved-data.js
const express = require('express');
const router = express.Router();
const savedDataController = require('../../controllers/api/savedData'); // Check this path
const { requireAuth } = require("../middleware/auth");

// Add requireAuth middleware to both routes
router.post('/save', requireAuth, savedDataController.saveUserData);
router.get('/', requireAuth, savedDataController.getSavedUserData);

module.exports = router;
