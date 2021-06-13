# https://docs.python-guide.org/writing/tests/
# https://realpython.com/python-testing/#testing-your-code
# https://blog.j-labs.pl/2019/02/Pytest-why-its-more-popular-than-unittest -> Pytest comes with a possibility to run tests parallelly by multiple processes using pytest-xdist.

# py.tests for unit tests
# something for smoke test where we get the bot to put a message like
# the ones coming from github (or not, we don't want to interfere with a bot instance running, we may just mock the message)
# then we do the entire flow until jenkins, where there will be an empty job just for this test, to ensure it receives the message
# and runs the job. The job will only track changes in this folder triggers/gitbot (probably) and will run. Then jenkins somehow replies
# back to the bot and we assert receiving that confirmation the job ran and finish the test

import pytest
