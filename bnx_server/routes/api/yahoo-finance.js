const express = require('express');
const router = express.Router();
const yahooFinance = require('../../controllers/api/yahoo-finance');

router.get('/', yahooFinance.getAllYahooSPData);
router.get('/symbols', yahooFinance.getAllSPSymbols);
router.get('/stock/:symbol', yahooFinance.getStockData);

module.exports = router;