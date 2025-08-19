DROP TABLE IF EXISTS final_summary;
CREATE TABLE final_summary AS
SELECT
    owner_company,
    owner_company_country,
    DATE_TRUNC('month', check_out_date)::DATE AS month,
    COUNT(*) AS bookings,
    CASE owner_company_country
        WHEN 'UK' THEN COUNT(*) * 10
        WHEN 'USA' THEN COUNT(*) * 14
        WHEN 'France' THEN COUNT(*) * 12
    END AS revenue_original,
    CASE owner_company_country
        WHEN 'UK' THEN 'GBP'
        WHEN 'USA' THEN 'USD'
        WHEN 'France' THEN 'EUR'
    END AS currency,
    GREATEST(
        CASE owner_company_country
            WHEN 'UK' THEN COUNT(*) * 10
            WHEN 'USA' THEN COUNT(*) * 14
            WHEN 'France' THEN COUNT(*) * 12
        END,
        CASE owner_company_country
            WHEN 'UK' THEN 100
            WHEN 'USA' THEN 140
            WHEN 'France' THEN 120
        END
    ) AS final_fee_original,
    GREATEST(
        CASE owner_company_country
            WHEN 'UK' THEN COUNT(*) * 10 * cr.rate_to_gbp
            WHEN 'USA' THEN COUNT(*) * 14 * cr.rate_to_gbp
            WHEN 'France' THEN COUNT(*) * 12 * cr.rate_to_gbp
        END,
        CASE owner_company_country
            WHEN 'UK' THEN 100 * cr.rate_to_gbp
            WHEN 'USA' THEN 140 * cr.rate_to_gbp
            WHEN 'France' THEN 120 * cr.rate_to_gbp
        END
    ) AS final_fee_gbp
FROM bookings_raw
JOIN currency_rates cr ON
    (owner_company_country = 'UK' AND cr.currency = 'GBP') OR
    (owner_company_country = 'USA' AND cr.currency = 'USD') OR
    (owner_company_country = 'France' AND cr.currency = 'EUR')
GROUP BY owner_company, owner_company_country, month, cr.rate_to_gbp;
