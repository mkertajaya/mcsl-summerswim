create table v2_YEAR2012_AFT as

select *, CONCAT(cast(year as CHAR), '-', week) as 'year_week', substring(event, POSITION('-' IN event)+2, 100) as 'event_name'from v2_YEAR2012 vy 
union all
select *, CONCAT(cast(year as CHAR), '-', week) as 'year_week', substring(event, POSITION('-' IN event)+2, 100) as 'event_name' from v2_YEAR2013 vy 
union all
select *, CONCAT(cast(year as CHAR), '-', week) as 'year_week', substring(event, POSITION('-' IN event)+2, 100) as 'event_name' from v2_YEAR2014 vy 
union all
select *, CONCAT(cast(year as CHAR), '-', week) as 'year_week', substring(event, POSITION('-' IN event)+2, 100) as 'event_name' from v2_YEAR2015 vy 
union all
select *, CONCAT(cast(year as CHAR), '-', week) as 'year_week', substring(event, POSITION('-' IN event)+2, 100) as 'event_name' from v2_YEAR2016 vy 
union all
select *, CONCAT(cast(year as CHAR), '-', week) as 'year_week', substring(event, POSITION('-' IN event)+2, 100) as 'event_name' from v2_YEAR2017 vy 
union all
select *, CONCAT(cast(year as CHAR), '-', week) as 'year_week', substring(event, POSITION('-' IN event)+2, 100) as 'event_name' from v2_YEAR2018 vy 
union all
select *, CONCAT(cast(year as CHAR), '-', week) as 'year_week', substring(event, POSITION('-' IN event)+2, 100) as 'event_name' from v2_YEAR2019 vy 
union all
select *, CONCAT(cast(year as CHAR), '-', week) as 'year_week', substring(event, POSITION('-' IN event)+2, 100) as 'event_name' from v2_YEAR2021 vy 
union all
select *, CONCAT(cast(year as CHAR), '-', week) as 'year_week', substring(event, POSITION('-' IN event)+2, 100) as 'event_name' from v2_YEAR2022 vy 

