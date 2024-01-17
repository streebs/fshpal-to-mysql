# TOOD: write tests to ensure the conversion of the data is correct
import re

def test_date(data):
    ismatch = re.match(r'^[0-9]+$', data)
    return True if ismatch else False

# tests for timei, timeo, timev to ensure they are in the correct format ^[0-2][0-9]:[0-5][0-9]$
def test_times(data):
    ismatch = re.match(r'^([0-1][0-9]|[2][0-3]):[0-5][0-9]$', data)
    return True if ismatch else False 
# tests for uvid to ensure it is in the correct format ^[0-9]{8}$
def test_uvid(data):
    ismatch = re.match(r'^[0-9]{8}$', data)
    return True if ismatch else False

#the following tests are for the name, center, and class columns to ensure they are not empty
# I have implemented these multiple times in the event that the criteria for these columns change
def test_name(data):
    ismatch = re.match(r'^.+$', data)
    return True if ismatch else False

def test_center(data):
    ismatch = re.match(r'^.+$', data)
    return True if ismatch else False

def test_class(data):
    ismatch = re.match(r'^.+$', data)
    return True if ismatch else False

def test_reason(data):
    ismatch = re.match(r'^.+$', data)
    return True if ismatch else False
