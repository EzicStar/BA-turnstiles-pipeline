{{ config(materialized='table') }}

WITH turnstiles AS
(
  SELECT *,
  FROM {{ source('staging','turnstiles_part_clust') }}
),

holidays AS
(
  SELECT * FROM {{ ref('public_holidays_2018')}}
  UNION ALL
  SELECT * FROM {{ ref('public_holidays_2019')}}
)

SELECT 
    t.Line,
    t.TurnstileID,
    t.Station,
    CAST(t.PaxAmount AS INTEGER) AS PaxAmount,
    t.StartDateTime,
    t.EndDateTime,
    -- A flag that is 1 if the date is a public holiday
    CASE WHEN h.date IS NULL THEN 0 ELSE 1 END AS IsHoliday
FROM turnstiles t
LEFT JOIN holidays h ON CAST(t.EndDateTime AS date) = h.date
WHERE PaxAmount < 1000
-- We remove the records that have an impossible passenger amount for 15 minutes
