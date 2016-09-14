The main points on that task:

- The sample input provided with the task gives expected result.
- I tried to solve the task without any additional libraries, just plain Python.
- There aren't classes or objects inside, just tuples for simplicity.
- There is a quick-and-dirty test suite inside. It's compatible with PyTest. I
  added my own test runner system to not depend on PyTest library.
- Tested with Python 2.7

Example:

```
cat sample.txt | python mars.py
1 1 E
3 3 N LOST
2 3 S
```
