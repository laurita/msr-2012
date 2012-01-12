# connect to SQLite DB
drv <- dbDriver("SQLite")
tfile <- tempfile()
con <- dbConnect(drv, dbname = '/Users/laura/Sandbox/msr-2012/data/db.sqlite3')

# get counts of comments and their frequencies in a bug (for a histogram)
comment_frequencies <- dbGetQuery(con, "select counts, count(counts) frequencies
from
(select bug_id, count(bug_id) counts
from comments
group by bug_id)
group by counts
order by counts;")

# make a histogram of number of comments in a bug
plot(comment_frequencies[,1], comment_frequencies[,2], type="s", xlab= "Number of comments in a bug", ylab="Frequency of such bugs")

# resolving time of a bug
resolving_times <- dbGetQuery(con, "select julianday(closed_on) - julianday(opened_date)
from bugs where closed_on not null")

# resolving time statistics
min(resolving_times)
max(resolving_times)
colMeans(resolving_times)

# make list numeric
res_times <- resolving_times[[1]]

# histogram of bug resolving times
hist(res_times, breaks=28,main="",xlab="Resolving time in days")

# comments counts and resolving times
times_comments <- dbGetQuery(con, "select count(bugs.bug_id) counts, julianday(closed_on) - julianday(opened_date) time
from comments, bugs
where bugs.bug_id = comments.bug_id and closed_on not null
group by bugs.bug_id;")

# plot comments counts vs resolving times
plot(times_comments[,1], times_comments[,2], xlab="Number of comments", ylab="Resolving time")

# general linear model
glm.linear <- glm(times_comments[,2] ~ times_comments[,1])
summary(glm.linear)
glm.linear.resids <- residuals(glm.linear)
hist(glm.linear.resids)
glm.linear.preds <- fitted.values(glm.linear)
plot(glm.linear.preds, glm.linear.resids)

# comment density(per day) and resolving times
density_time <- dbGetQuery(con, "select count(bugs.bug_id)/(julianday(closed_on) - julianday(opened_date)) density, julianday(closed_on) - julianday(opened_date) time
from comments, bugs
where bugs.bug_id = comments.bug_id and closed_on not null
group by bugs.bug_id;")

# comment density(per week) and resolving times
density_time <- dbGetQuery(con, "select 7*count(bugs.bug_id)/(julianday(closed_on) - julianday(opened_date)) density, julianday(closed_on) - julianday(opened_date) time
from comments, bugs
where bugs.bug_id = comments.bug_id and closed_on not null
group by bugs.bug_id;")

# plot comment density vs resolving time
plot(density_time[,1], density_time[,2], xlab="Comments per week", ylab="Resolving time")

# general linear model
glm.linear <- glm(density_time[,2] ~ density_time[,1])
summary(glm.linear)

# line fitting glm
lines(density_time[,1], 73.028560+-0.004710*density_time[,1])

























