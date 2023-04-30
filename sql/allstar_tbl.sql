CREATE TABLE ALLSTAR as
select * ,
substring(event, POSITION('-' IN event)+2, 100) as 'event_name',
case when q_time like '%:%' then CAST(SUBSTRING_INDEX(q_time,':',1) as DECIMAL(5,2))*60 + 
		CAST(SUBSTRING_INDEX(q_time,':',-1) as DECIMAL(5,2))
	else CAST(q_time as DECIMAL(5,2)) end as 'q_time_sec'
from `_ALLSTAR` a 
