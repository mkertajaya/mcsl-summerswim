update v2_YEAR2012_AFT
set year_week =  CONCAT(cast(year as CHAR), '-', week),
	event_name = substring(event, POSITION('-' IN event)+2, 100)
where year_week is null



select *, CONCAT(cast(year as CHAR), '-', week) as 'year_week', substring(event, POSITION('-' IN event)+2, 100) as 'event_name'from v2_YEAR2012 vy 


select year_week, count(1) from v2_YEAR2012_AFT
group by year_week 
order by 1