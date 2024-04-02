for dataset in sw stackoverflow wwc2019 synthea fincen
do
	for safety in True False
	do
		for assignment in random betweennessDesc betweennessAsc degreeDesc degreeAsc prDesc prAsc 
		do
			for users in 5 10 15 20 25 30 40 60 80 100
			do
				for answer in 0 0.25 0.5 0.75 1
				do					
					echo "Running $dataset $safety $assignment $users $answer"
					python3 envivorment.py $dataset $safety $assignment $users $answer						
				done
			done
		done
	done
done

