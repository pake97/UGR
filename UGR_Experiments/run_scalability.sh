for dataset in synthea synthea50 synthea75 synthea100 synthea150
do
	for safety in True 
	do
		for assignment in random degreeAsc  
		do
			for users in 5 10 15 20 25 30 40 60 80 100
			do
				for answer in 1
				do					
					echo "Running $dataset $safety $assignment $users $answer"
					python3 envivorment6.py $dataset $safety $assignment $users $answer						
				done
			done
		done
	done
done

