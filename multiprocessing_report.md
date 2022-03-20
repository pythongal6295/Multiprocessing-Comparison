Baseline data:

Running load_users.py before multiprocessing took 12.9599 seconds.
Running load_status_updates.py before multiprocessing took 586.0408 seconds.


Process and results:

To improve this performance, I used multiprocessing and queues to upload chunks of the csv files. The chunking was done by the pandas module. Below are my results for different chunk sizes and number of processes. 


Function	# of Processes	Chunk Size	Time to Process (seconds)

load_user	6		10		1.9418
load_status	6		10		203.8293

load_user	6		50		0.7679
load_status	6		50		12.4455

load_user	6		100		0.2060
load_status	6		100		6.4489

load_user	8		10		0.5585
load_status	8		10		59.9700

load_user	8		50		0.2743
load_status	8		50		12.3791

load_user	8		100		0.2374
load_status	8		100		6.5218



Summary of results

Using multiprocessing significantly sped up the upload of user and user status data to the MongoDB database. Even for the smallest amount of chunks and fewest amount of processes, multiprocessing was 85.0% faster for load_users() and 65.2% faster for load_status_updates(). As I increased the chunk size, the completion time dropped. This makes sense because there were fewer tasks the 6 cores had to cycle through. The completion time was also faster when I added 2 more processes for the 10 and 50 chunk sizes. There were more cores to work on the tasks in the queue, so the tasks were processed faster. There was little or no improvement when comparing the 100 chunk size runs. I think this may be because the time the two extra processes saved from an already short processing time did not outweigh the time it took to start up Python in those two extra cores. Chunking and multiprocessing can be very helpful tools to speed up long processing times.

*One problem I am still having with my code is that after the load_user and load_status_updates functions run, I am unable to search and find user_ids and status_ids that came from the csv files. I am wondering if since I am using object orientated programming for this database implementation that the MongoDB collections the user_collection and status_collection objects are using are not the same as the collections I set up when loading data from the csv files. It may also be that I am not actually adding the data to MongoDB. At this time I am not sure how to check if something was added to MongoDB except through the search menu options in my program. More investigation and debugging is necessary.

