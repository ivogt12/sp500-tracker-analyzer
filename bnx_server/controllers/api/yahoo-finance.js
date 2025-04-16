const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

module.exports = {
    getAllYahooSPData,
    getAllSPSymbols,
    getStockData,
}

async function getAllYahooSPData(req, res) {
    const pythonProcess = spawn(
        'python', 
        [
            path.join(
            __dirname, 
            '../../scraper/runYahooSPSpider.py')
        ]
    );

    let data = '';

    pythonProcess.stdout.on('data', (chunk) => {
        data += chunk.toString();
    });

    pythonProcess.stderr.on('data', (error) => {
        console.error(`Error: ${error}`);
    });

    pythonProcess.on('close', (code) => {
        if (code === 0) {
            try {
                const jsonData = JSON.parse(data); // Assuming the output is JSON
                res.json(jsonData[0]);
            } catch (error) {
                console.error(`JSON Parse Error: ${error}`);
                res.status(500).json({ message: 'Error parsing JSON data' });
            }
        } else {
            res.status(500).json({ message: 'Error occurred during scraping' });
        }
    });
}

async function getAllSPSymbols(req, res) {
    const pythonProcess = spawn(
        'python', 
        [
            path.join(
            __dirname, 
            '../../scraper/runWikiSPSpider.py')
        ]
    );

    let data = '';

    pythonProcess.stdout.on('data', (chunk) => {
        data += chunk.toString();
    });

    pythonProcess.stderr.on('data', (error) => {
        console.error(`Wikipedia Symbol Error: ${error}`);
    });

    pythonProcess.on('close', (code) => {
        if (code === 0) {
            try {
                const jsonData = JSON.parse(data); // Assuming the output is JSON
                res.json(jsonData[0]);
            } catch (error) {
                console.error(`Wikipedia Symbol JSON Parse Error: ${error}`);
                res.status(500).json({ message: 'Wikipedia Symbol Error parsing JSON data' });
            }
        } else {
            res.status(500).json({ message: 'Wikipedia Symbol Error occurred during scraping' });
        }
    });
}


// async function getStockData(req, res) {
//     isProcessing = true;
//     const symbol = req.params.symbol;
//     console.log("Request for:", symbol);

//     try {
//         const scrapedData = { test: "mocked data" };  // Mock data
//         const plots = ["plot1.png", "plot2.png"];
        
//         res.status(200).json({ scrapedData, plots });
//     } catch (error) {
//         res.status(500).json({ message: error.message });
//     } finally {
//         isProcessing = false;
//     }
// }

let isProcessing = false;

async function getStockData(req, res) {
    // if (isProcessing) {
    //     return res.status(429).json({ message: 'Request already in progress' });
    // }
    isProcessing = true;

    const symbol = req.params.symbol;
    const startTime = Date.now();
    console.log(`Request received for symbol: ${symbol}`);

    try {
        const scrapedData = await runPythonProcess(symbol, startTime);
        // res.status(200).json({ scrapedData }); 
        const plots = await runRProcess(scrapedData, symbol, req, startTime);
        
        console.log("Sending response with plots and scraped data.");
        console.log("Scraped Data:", scrapedData);
        
        console.log("Plots:", plots);
        // res.status(200).json({scrapedData, plots});
        res.status(200).json({scrapedData, plots});


    } catch (error) {
        console.error("Error occurred:", error.message);
        res.status(500).json({ message: error.message });
    } 
    // finally {
    //     isProcessing = false;
    //     console.log("Processing flag reset.");
    //     // res.json({message: "test"});
    //     // setTimeout(() => { isProcessing = false; }, 1000);
    // }
}

function runPythonProcess(symbol, startTime) {
    return new Promise((resolve, reject) => {
        const pythonProcess = spawn('python', [
            path.join(__dirname, '../../scraper/runYahooStockSpider.py'), symbol
        ]);

        let data = '';
        let errorData = '';

        pythonProcess.stdout.on('data', (chunk) => data += chunk.toString());
        pythonProcess.stderr.on('data', (error) => {
            errorData += error.toString();
            console.error(`Python Error: ${error.toString()}`);
        });

        pythonProcess.on('close', (code) => {
            const duration = (Date.now() - startTime) / 1000;
            console.log(`Python process closed after ${duration} seconds with code ${code}.`);

            if (code !== 0) {
                return reject(new Error(`Python scraper error: ${errorData}`));
            }

            try {
                const jsonData = JSON.parse(data);
                console.log("Scraped data received.");
                resolve(jsonData);
            } catch (parseError) {
                reject(new Error(`JSON parse error: ${parseError.message}`));
            }
        });

        setTimeout(() => {
            pythonProcess.kill('SIGTERM');
            reject(new Error("Python process timed out."));
        }, 60000);
    });
}

function runRProcess(scrapedData, symbol, req, startTime) {
    return new Promise((resolve, reject) => {
        const tmpDir = path.join(__dirname, '../../tmp');
        if (!fs.existsSync(tmpDir)) fs.mkdirSync(tmpDir);

        const jsonFilePath = path.join(tmpDir, `${symbol}_data.json`);
        fs.writeFileSync(jsonFilePath, JSON.stringify(scrapedData), 'utf8');

        const rScriptPath = path.join(__dirname, './financial-charts.R');
        const plotDir = path.join(__dirname, '../../../bnx_client/public/plots');

        const rProcess = spawn(
            'C:\\Program Files\\R\\R-4.4.1\\bin\\Rscript.exe',
            [rScriptPath, jsonFilePath, plotDir],
            { stdio: ['ignore', 'pipe', 'ignore'] } // Ignore stderr completely
        );

        let output = '';
        let isResolved = false;

        rProcess.stdout.on('data', (data) => {
            output += data.toString();
        });

        rProcess.on('exit', (rCode) => {
            if (isResolved) return;
            isResolved = true;

            const duration = (Date.now() - startTime) / 1000;
            console.log(`R process exited after ${duration} seconds with code ${rCode}.`);

            const plots = {
                financialRatiosBarChart: '/plots/financial_ratios_plot.png',
                revenueNetIncomeDualAxis: '/plots/revenue_net_income_dual_axis.png',
                cashFlowBalanceSheetStackedBar: '/plots/cash_flow_balance_sheet.png'
            };

            resolve(plots);
        });

        setTimeout(() => {
            if (isResolved) return;
            isResolved = true;
            
            rProcess.kill('SIGTERM');
            reject(new Error("R process timed out."));
        }, 120000);
    });
}
