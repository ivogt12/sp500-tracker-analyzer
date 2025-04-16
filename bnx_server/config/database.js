const sql = require('mssql');

const config = {
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    server: process.env.DB_SERVER,
    database: process.env.DB_DATABASE,
    options: {
        trustServerCertificate: true, // Use this if you're using a self-signed certificate
        trustedConnection: true, // Use Windows Authentication
        enableArithAbort: true,
    },
};

async function connection() {
    try {
        await sql.connect(config);
        console.log('Connected to BNX SQL Database.');
    } catch (err) {
        console.error('Database connection error:', err);
    }
}

module.exports = { sql, connection};