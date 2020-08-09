all : lint test

run :
	python3 turing.py

lint :
	pylint turing.py test.py

test :
	python3 -m unittest test.py

time : test

profile :
	python3 -m cProfile turing.py

clean :
	rm -rf yappi.* __pycache__

gen3 :
	python3 generate-3-state.py > 3-state-programs.txt
	wc -l 3-state-programs.txt
