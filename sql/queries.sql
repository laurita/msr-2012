-- max number of comments in one bug
select max(counts) 
from 
    (select bug_id, count(bug_id) counts
    from comments
    group by bug_id);
-- 25

-- min number of comments in one bug
select min(counts) 
from 
    (select bug_id, count(bug_id) counts
    from comments
    group by bug_id);
-- 1

-- average number of comments in one bug
select avg(counts) 
from 
    (select bug_id, count(bug_id) counts
    from comments
    group by bug_id);
-- 4.5228714524207

-- comment frequencies in a bug
select counts, count(counts) frequencies
from
(select bug_id, count(bug_id) counts
from comments
group by bug_id)
group by counts
order by frequencies desc;

1|4755
2|3074
3|1915
4|1257
5|817
25|685
6|574
7|389
8|276
9|219
10|198
11|156
12|96
13|91
14|80
15|61
17|53
19|49
16|47
20|40
18|36
22|32
21|26
23|26
24|23

select 0.95*sum(frequencies)
from
(select counts, count(counts) frequencies
from
(select bug_id, count(bug_id) counts
from comments
group by bug_id)
group by counts);

-- time from opening until closing the bug (in days)
select bug_id, opened_date, closed_on, julianday(closed_on) - julianday(opened_date)
from bugs
limit 20;

1|2007-11-12 16:02:55|2008-01-08 21:56:22|57.2454513888806
2|2007-11-12 16:34:14|2008-01-08 22:19:59|57.2401041667908
3|2007-11-12 20:31:43|2008-01-08 23:06:17|57.107337962836
4|2007-11-12 22:42:05|2008-01-08 23:07:54|57.0179282408208
5|2007-11-12 22:46:48|2008-01-08 23:08:30|57.0150694441982
6|2007-11-12 23:18:54|2008-02-28 23:22:43|108.002650462557
7|2007-11-13 02:32:35|2008-01-08 23:14:13|56.8622453706339
8|2007-11-13 06:05:31|2008-01-08 23:18:41|56.7174768517725
9|2007-11-15 22:56:56|2008-01-08 23:14:20|54.0120833334513
10|2007-11-18 14:41:38|2008-01-08 23:15:23|51.3567708334886
11|2007-11-20 15:47:48|2008-01-12 09:25:03|52.7342013888992
12|2007-11-20 21:03:44|2008-05-08 21:42:52|170.027175926138
13|2007-11-22 01:36:02|2009-02-06 14:28:54|442.536712962668
14|2007-11-22 05:36:12|2008-03-09 11:12:04|108.233240740839
15|2007-11-22 21:56:51|2009-11-23 18:21:54|731.85072916653
16|2008-01-03 19:03:28|2009-01-29 13:54:59|391.785775463097
17|2008-01-12 09:28:55|2008-01-12 09:29:12|0.00019675912335515
18|2008-01-12 09:29:32|2008-01-12 10:26:29|0.0395486112684011
19|2008-01-12 10:26:46|2008-01-12 10:27:26|0.000462962780147791
20|2008-01-14 22:17:24|2008-01-14 22:19:03|0.00114583317190409

-- just the bug_id's and times
select julianday(closed_on) - julianday(opened_date)
from bugs 
where closed_on not null;

-- average time required to solve the bug (in days). If the bug is not yet closed, the case is not counted, because avg counts only non-NULL cases.
select avg(julianday(closed_on)-julianday(opened_date))
from bugs;
72.4401653204619

-- resolving time vs. comments

select bugs.bug_id, count(bugs.bug_id) counts, julianday(closed_on) - julianday(opened_date) time
    from comments, bugs
    where bugs.bug_id = comments.bug_id and closed_on not null
    group by bugs.bug_id;

-- comment density vs. resolving time
select bugs.bug_id, count(bugs.bug_id)/(julianday(closed_on) - julianday(opened_date)) density, julianday(closed_on) - julianday(opened_date) time
    from comments, bugs
    where bugs.bug_id = comments.bug_id and closed_on not null
    group by bugs.bug_id;

-- time zones
select tz/60 from commits;









-------------------------------------------------------------------------------------------

-- COMMITS' INFO

-- number of commits
select count(*) from commits;


































