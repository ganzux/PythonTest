import csv
from datetime import date
from datetime import datetime
import matplotlib.pyplot as plt
import random

random.seed(a=None)

date_format = "%d-%b-%y"

f1 = open("data.txt", "r") 
c1 = csv.reader(f1)

column_idx_0_based_start_date = 8
column_idx_0_based_end_date = 9
column_idx_0_based_estimated_duration = 0

# Array with the estimated durations of each row
durations = []
# Array with the real durations of each row
delta_durations = []

# Big Array to store the number of times every real duration is in the dataset 
number_of_durations = [None]*10000
# Big Array to store the sum of all real durations in the dataset
sum_delta_durations = [None]*10000
# Big Array to store the index of all real durations in the dataset
idx_delta_durations = [None]*10000

# Array to store the real durations after we have done the average
avg_delta_idx = []
# Array to store the average estimated durations 
avg_delta_durations = []

avg_counter = 0
sum = 0

#Difference between real and API estimated end-date
for log_row in c1:
	try:
		real_end_date = datetime.strptime(log_row[column_idx_0_based_end_date], date_format)
		real_start_date = datetime.strptime(log_row[column_idx_0_based_start_date], date_format)

		# The column number 4 contains the estimated duration in days
		estimated_duration = abs(int(log_row[column_idx_0_based_estimated_duration]))
        
		# Real duration of the claim.
		real_duration = real_end_date - real_start_date
		real_duration_in_days = abs(real_duration.days)

    # FAKE: add some days to the real duration
		estimated_duration = real_duration_in_days + randint(0,3)

		durations.append(estimated_duration)
		delta_durations.append(real_duration_in_days)

		avg_counter += abs(real_duration_in_days - estimated_duration)

		current_index = real_duration_in_days

    # times of durations per claim
		if number_of_durations[current_index] is None:
			number_of_durations[current_index] = 1
		else:
			number_of_durations[current_index] = number_of_durations[current_index] + 1

        # total of days per claim duration
		if sum_delta_durations[current_index] is None:
			sum_delta_durations[current_index] = abs(real_duration_in_days - estimated_duration)
		else:
			sum_delta_durations[current_index] = sum_delta_durations[current_index] + abs(real_duration_in_days - estimated_duration)

		idx_delta_durations[current_index] = current_index
		sum = sum + 1

	except ValueError:
		pass

for times, sumd, index in zip(number_of_durations, sum_delta_durations, idx_delta_durations):
	if (index >= 0 and index < 100 and number_of_durations[index] > 0):
		x = x + 1
		#print (number_of_durations[index])
		avg_delta_idx.append(index)
		avg_delta_durations.append(float(sumd) / times)

plt.plot(avg_delta_idx, avg_delta_durations, "ro")
plt.ylabel('Difference')
plt.xlabel('Claim Duration')
plt.show()

print "We can estimate with an average of ",float(avg_counter)/sum," days!!!!"
