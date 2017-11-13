
-- 1. What query would you run to get the total revenue for March of 2012?

SELECT SUM(billing.amount), charged_datetime
FROM billing
WHERE YEAR(charged_datetime) = 2012 AND MONTHNAME(charged_datetime) = "March";

-- 2. What query would you run to get total revenue collected from the client with an id of 2?

SELECT SUM(billing.amount), charged_datetime
FROM billing
JOIN clients ON clients.client_id = billing.client_id
WHERE clients.client_id = 2;

-- 3. What query would you run to get all the sites that client=10 owns?

SELECT sites.domain_name
FROM sites
JOIN clients ON clients.client_id = sites.client_id
WHERE clients.client_id = 10;

-- 4. What query would you run to get total # of sites created per month per year for the client with an id of 1? 
-- What about for client=20?

SELECT clients.client_id, COUNT(sites.domain_name) as number_of_websites, MONTHNAME(sites.created_datetime) as month_created, YEAR(sites.created_datetime) as year_created
FROM sites
JOIN clients ON clients.client_id = sites.client_id
WHERE clients.client_id = 1
GROUP BY month_created, year_created; -- the comma between the two columns is necesary to separate the grouping into PER month PER year

-- 5. What query would you run to get the total # of leads generated for each of the sites between January 1, 2011 to February 15, 2011?

SELECT sites.domain_name, COUNT(leads.leads_id) as number_of_leads, leads.registered_datetime
FROM sites
LEFT JOIN leads ON sites.site_id = leads.site_id
WHERE (leads.registered_datetime BETWEEN '2011-01-01' AND '2011-02-15')
GROUP BY sites.site_id;

-- 6. What query would you run to get a list of client names and the total # of leads we've generated for each of our clients between January 1, 2011 to December 31, 2011?

SELECT CONCAT(clients.first_name, " ", clients.last_name) as client_name, COUNT(leads.leads_id) as number_of_leads -- need the COUNT(leads.leads_id)
FROM clients
LEFT JOIN sites ON clients.client_id = sites.client_id
JOIN leads ON leads.site_id = sites.site_id
WHERE (leads.registered_datetime BETWEEN'2011-01-01' AND '2011-12-31')
GROUP BY clients.client_id;

-- 7. What query would you run to get a list of client names and the total # of leads we've generated for each client each month between months 1 - 6 of Year 2011?

SELECT CONCAT(clients.first_name, " ", clients.last_name) as client_name, COUNT(leads.leads_id) as number_of_leads, MONTHNAME(leads.registered_datetime) as month
FROM clients
LEFT JOIN sites ON clients.client_id = sites.client_id
JOIN leads ON leads.site_id = sites.site_id
WHERE (leads.registered_datetime BETWEEN'2011-01-01' AND '2011-6-31')
GROUP BY clients.client_id, month
ORDER by leads.registered_datetime;

-- alternate way of using the date format as month below:
SELECT CONCAT(clients.first_name, ' ', clients.last_name) AS client_name, COUNT(leads.leads_id) AS num_leads, DATE_FORMAT(leads.registered_datetime, '%M') AS 'month'
FROM clients
	LEFT JOIN sites ON clients.client_id = sites.client_id
    JOIN leads ON sites.site_id = leads.site_id
WHERE leads.registered_datetime BETWEEN '2011-01-01' AND '2011-06-30'
GROUP BY clients.client_id, MONTH(leads.registered_datetime)
ORDER BY MONTH(leads.registered_datetime);


-- 8. What query would you run to get a list of client names and the total # of leads we've generated for each of our clients' sites between January 1, 2011 to December 31, 2011? 
-- Order this query by client id.  

SELECT CONCAT(clients.first_name, " ", clients.last_name) as client_name, sites.domain_name, COUNT(leads.leads_id) as number_of_leads -- need the COUNT(leads.leads_id)
FROM clients
JOIN sites ON clients.client_id = sites.client_id
JOIN leads ON leads.site_id = sites.site_id
WHERE (leads.registered_datetime BETWEEN'2011-01-01' AND '2011-12-31')
GROUP BY sites.domain_name
ORDER BY clients.client_id

-- Come up with a second query that shows all the clients, the site name(s), and the total number of leads generated from each site for all time.

SELECT CONCAT(clients.first_name, " ", clients.last_name) as client_name, sites.domain_name, COUNT(leads.leads_id) as number_of_leads -- need the COUNT(leads.leads_id)
FROM clients
LEFT JOIN sites ON clients.client_id = sites.client_id
LEFT JOIN leads ON leads.site_id = sites.site_id
GROUP BY sites.domain_name
ORDER BY clients.client_id

-- 9. Write a single query that retrieves total revenue collected from each client for each month of the year. 
-- Order it by client id.

SELECT clients.client_id, SUM(billing.amount), DATE_FORMAT(charged_datetime, '%M') AS month, DATE_FORMAT(charged_datetime, '%Y') AS year 
FROM clients
JOIN billing ON billing.client_id = clients.client_id
GROUP BY clients.client_id, month, year

-- 10. Write a single query that retrieves all the sites that each client owns. 
-- Group the results so that each row shows a new client. 
-- It will become clearer when you add a new field called 'sites' that has all the sites that the client owns. 
-- (HINT: use GROUP_CONCAT)

SELECT clients.client_id, GROUP_CONCAT(sites.domain_name) as sites
FROM clients
LEFT JOIN sites ON clients.client_id = sites.client_id
GROUP BY clients.client_id



















