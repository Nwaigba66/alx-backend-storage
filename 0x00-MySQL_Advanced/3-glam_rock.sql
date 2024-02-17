SELECT 
    band_name,
    CASE 
        WHEN lifespan = 'split -' THEN NULL
        ELSE YEAR('2022-01-01') - SUBSTRING_INDEX(lifespan, ' - ', 1)
    END AS lifespan
FROM
    metal_bands
WHERE
    main_style = 'Glam rock'
ORDER BY
    lifespan DESC;
