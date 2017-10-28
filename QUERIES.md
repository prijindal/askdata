### Sample Queries
- These Queries defines these three things
    - Query in egnlish the user is searching
    - Corresponding Graph/Visualization that user is looking for
    - Data corresponding to that query
    - SQL Query corresponding to it

- Query #1
    - Female Literacy Rate by state
    - A scatter graph with X axis as the states and y axis as the percentage literacy
    - ```SELECT (Literate_-_Females/Total_Females)*100 FROM EDUCATION_LEVEL```

- Query #2
    - Increase in no. of schools affect increase in literacy rate
    - Bar graph with x axis as years, 2 bars: one with no. of schools, other literacy rate

- Query #3
    - Literacy rate of females in Punjab vs Tamil Nadu
    - A plot graph with x as ages, y axis with literacy rate for Punjab and Tamil Nadu
    - ```
        SELECT punjab_percentage_table.age_group, punjab_percentage, tamil_nadu_percentage FROM (
            SELECT age_group, (literate_females/total_females)*100 as punjab_percentage
                    FROM education
                    WHERE area_name LIKE 'State - PUNJAB%'
                    AND age_group NOT LIKE '%age%'
                    AND `total__rural__urban`='Total'
                    AND year=2011
                    GROUP BY age_group
                    ORDER BY (`age_group` * 1)
                    asc) as punjab_percentage_table,(
            SELECT age_group, (literate_females/total_females)*100 as tamil_nadu_percentage
                    FROM education
                    WHERE area_name LIKE 'State - TAMIL NADU%'
                    AND age_group NOT LIKE '%age%'
                    AND `total__rural__urban`='Total'
                    AND year=2011
                    GROUP BY age_group
                    ORDER BY (`age_group` * 1)
                    asc) as tamil_nadu_education_table
            WHERE tamil_nadu_education_table.age_group=punjab_percentage_table.age_group;
        ```

- Query #4
    - Increase in literay rate in Tamil Nadu over the years
    - X axis as years, y axis as literacy rates
    - ```
        SELECT year, (literate_females/total_females)*100 as literacy_rate
            FROM education
            WHERE area_name like '%State - TAMIL NADU%'
            AND age_group = 'All ages' and `total__rural__urban`='Total';
    ```

- Query #5
    - Which state had the maximum literacy rate growth in the past 5 years?
    - A scatter graph with literacy growth rate by state in 5 years, x axis as years, y axis as literacy growth for each state
    - 
    ```
        SELECT area_name, education_2001.literacy_rate as literacy_2001, education_2011.literacy_rate as literacy_2011 FROM 
            (SELECT state_code,
            (literate_females/total_females)*100 as literacy_rate, year
            FROM education
            WHERE year=2001 AND age_group = 'All ages' and `total__rural__urban`='Total'
            ) as education_2001,
            (SELECT area_name, state_code,
            (literate_females/total_females)*100 as literacy_rate, year
            FROM education
            WHERE year=2011 AND age_group = 'All ages' and `total__rural__urban`='Total'
            ) as education_2011
            WHERE education_2011.state_code = education_2001.state_code
            AND area_name NOT LIKE 'INDIA';

    ```

- Query #6
    - 
