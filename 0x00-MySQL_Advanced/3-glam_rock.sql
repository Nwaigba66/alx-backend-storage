-- Import the provided table dump
-- Assuming the table is named "metal_bands"

-- Calculate the lifespan in years until 2022
SELECT 
    band_name,
    YEAR('2022-01-01') - SUBSTRING_INDEX(lifespan, ' - ', 1) AS lifespan
FROM
    metal_bands
WHERE
    main_style = 'Glam rock'
ORDER BY
    lifespan DESC;

