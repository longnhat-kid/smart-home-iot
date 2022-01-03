TIMEOUT_MS = 2000
LONG_SLEEP_MS = 60000

TIME_TO_CALL_AI = 30000

MAX_NUM_OF_TOTAL_ATTEMPTS = 5
MAX_NUM_OF_PARTIAL_ATTEMPTS = 3
MAX_NUM_OF_REMOVE_ATTEMPTS = 3

lastPayload = ''
lastFeedId = ''
lastSentOK = True
numOfAttempts = 0
numOfFailed = 0
waitForSubscribe = True

buffer = []