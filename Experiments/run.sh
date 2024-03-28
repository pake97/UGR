for dataset in sw stackoverflow wwwc2019 synthea fincen
do
	for safety in True 
	do
		for assignment in random betweennessDesc betweennessAsc degreeDesc degreeAsc prDesc prAsc 
		do
			for users in 20
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

