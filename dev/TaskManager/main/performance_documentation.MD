# Performance Documentation
Added by Elvira Forslund Widenroth elvfor-0.

django-seed has been used in order to fake data. 400+ users, 400+ organizations and 400+ projects has been used when
evaluating the performance. 
## Task 1: Many-to-Many

### Printing all organizations and their users

- Using `Objects.all()` + iterate through:
  - 809 queries in 111.51 ms.

- Using `Organization.objects.prefetch_related('users').all()`:
  - 4 queries in 4.39 ms

Conclusion: There's been a large improvement of the number of queries used and the performance has therefore improved a lot. 

## Task 2 Nested Queries

### Printing all Projects and their related Organization

- Using `Project.objects.all()` and iterate:
  - 408 queries in 48.12 ms

- Using `Project.objects.select_related('organization').all()`:
  - 3 queries in 1.26 ms

Conclusion: Same as previous, there's been a large improvement of the number of queries used and the performance has therefore improved a lot. 


## Task 3 Aggregation Queries

### Printing all organizations and their number of users

- Using `Objects.all()` + iterate through:
  - 806 queries in 126.26 ms

- Using `Organization.objects.annotate(user_count=Count('users'))`:
  - 806 queries in 94.05 ms

Conclusion: There has been no improvement of the number of queries used and the performance has therefore not been improved (the improved time is not relevant because the nr of queries is still the same).
It is possible an improvement can be seen if the database contains millions of data. 