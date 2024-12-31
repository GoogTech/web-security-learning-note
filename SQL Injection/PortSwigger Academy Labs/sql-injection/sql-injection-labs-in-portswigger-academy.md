# Examples of SQL injection

## Retrieving hidden data

1. ✅ Lab : SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

   https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data

## Subverting application logic

2. ✅ Lab : SQL injection vulnerability allowing login bypass

   https://portswigger.net/web-security/sql-injection/lab-login-bypass

## SQL injection in different contexts

3. Lab : SQL injection with filter bypass via XML encoding

   https://portswigger.net/web-security/sql-injection/lab-sql-injection-with-filter-bypass-via-xml-encoding

# Examining the database

## Querying the database type and version

4. Lab : SQL injection attack, querying the database type and version on Oracle

   https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-oracle

5. Lab : SQL injection attack, querying the database type and version on MySQL and Microsoft

   https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-mysql-microsoft

## Listing the contents of the database

6. Lab : SQL injection attack, listing the database contents on non-Oracle databases

   https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-non-oracle

7. Lab: SQL injection attack, listing the database contents on Oracle

   https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-oracle

# UNION attacks

## Determining the number of columns required

8. ✅ Lab : SQL injection UNION attack, determining the number of columns returned by the query

https://portswigger.net/web-security/sql-injection/union-attacks/lab-determine-number-of-columns

## Finding columns with a useful data type

9. ✅ Lab : SQL injection UNION attack, finding a column containing text

   https://portswigger.net/web-security/sql-injection/union-attacks/lab-find-column-containing-text

## Using a SQL injection UNION attack to retrieve interesting data

10. ✅ Lab : SQL injection UNION attack, retrieving data from other tables

    https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-data-from-other-tables

## Retrieving multiple values within a single column

11. Lab : SQL injection UNION attack, retrieving multiple values in a single column

    https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-multiple-values-in-single-column

# Blind SQL injection

## Exploiting blind SQL injection by triggering conditional responses

12. ✅⭐️ Lab: Blind SQL injection with conditional responses

https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses

## Error-based SQL injection

#### Exploiting blind SQL injection by triggering conditional errors

13. ✅ Lab: Blind SQL injection with conditional errors

https://portswigger.net/web-security/sql-injection/blind/lab-conditional-errors

#### Extracting sensitive data via verbose SQL error messages

14. ✅ Lab: Visible error-based SQL injection

https://portswigger.net/web-security/sql-injection/blind/lab-sql-injection-visible-error-based

## Exploiting blind SQL injection by triggering time delays

15. ✅ Lab: Visible error-based SQL injection

https://portswigger.net/web-security/sql-injection/blind/lab-time-delays

16. ✅⭐️ Lab: Blind SQL injection with time delays and information retrieval

https://portswigger.net/web-security/sql-injection/blind/lab-time-delays-info-retrieval

## Exploiting blind SQL injection using out-of-band (OAST) techniques

17. （`BurpSuite Pro`）Lab: Blind SQL injection with out-of-band interaction

https://portswigger.net/web-security/sql-injection/blind/lab-out-of-band

18. （`BurpSuite Pro`）Lab: Blind SQL injection with out-of-band data exfiltration

https://portswigger.net/web-security/sql-injection/blind/lab-out-of-band-data-exfiltration
