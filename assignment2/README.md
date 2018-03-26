# Assignment 2 README:

TODO:
 * Add compilation and execution instructions,
 * Disclose all collaborations and websites/resources you've consulted
 * Add test cases for bonus marks

### create_lms.py instructions
- to run the program, enter: `python3 create_lms.py [dir/to/test/] [output/dir/]`
    - the program will create `a2.db` in the specified output directory
    - must have trailing backslash when specifying directories
- assumptions:
    - the movies and New York Times articles are stored in different directories
    - only one set of test data will be used for each instance of the program

### print_lms.py instructions
- to run the program, enter: `python3 print_lms.py [path/to/data/]`
    - the MLE scores are rounded to 5 decimal places for readability, however they are stored in their entirety

### query_lms.py instructions
- to run the program, enter: `python3 query_lms.py [path/to/data] k [white-space separated query]`

### nb_classifier.py instructions
- to run the program, enter: 'python3 nb_classifier.py [path/to/train/data] [path/to/test/data]'
	- for example, enter: 'python3 nb_classifier.py trec-397/data/train/ trec-397/data/test/'
	- give this file approx. a minute to run.


 python3 nb_classifier.py trec-397/data/train/ trec-397/data/test/