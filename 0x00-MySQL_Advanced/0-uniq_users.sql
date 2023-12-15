-- This script creates the 'users' table with the specified attributes

-- Check if the table already exists
IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'users') THEN

    -- Create the 'users' table
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) NOT NULL UNIQUE,
        name VARCHAR(255)
    );

END IF;
