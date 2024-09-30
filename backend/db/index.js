const pgp = require('pg-promise')();
require('dotenv').config();

let db; // Declare the db variable outside the function

const connectDb = async () => {
  if (!db) { // Check if db is not already instantiated
    let retries = 5;
    while (retries) {
      try {
        db = pgp({
          host: process.env.DB_HOST,
          port: process.env.DB_PORT,
          database: process.env.DB_NAME,
          user: process.env.DB_USER,
          password: process.env.DB_PASSWORD,
        });
        await db.connect(); // Attempt to connect
        console.log('Database connected successfully');
        return db; // Return the connected db instance
      } catch (err) {
        console.error('Database connection error:', err);
        retries -= 1;
        console.log(`Retries left: ${retries}`);
        await new Promise(res => setTimeout(res, 5000)); // Wait 5 seconds before retrying
      }
    }
    throw new Error('Could not connect to the database');
  }
  return db; // Return the existing db instance if already connected
};

module.exports = connectDb; // Export the connect function
