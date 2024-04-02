for dataset in sw stackoverflow wwwc2019 synthea fincen
do
	for safety in True False
	do
		for mode in 'label' 'delete' 'update' 'number'
		do	
            echo "Running $dataset $safety $mode"
			python3 preferred_environment.py $dataset $safety $mode				
			
		done
	done
done



