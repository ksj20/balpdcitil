# Read from json file and run some etl jobs for each key, value in it using multiprocessing
# 
# Caution: add following string as `test.json` to same folder as app/ folder before build
# {"test1": "value1", "test2": ["value2", "value3", "value4"], "test3": [1, 2, 3, 4, 5, 6, 6, 7, 8, 9], "test4": [{"subtest1": "subvalue1", "subtest2": "subvalue2"}, {"subtest3": "subvalue2", "subtest4": "subvalue2"}, {"subtest5": "subvalue2", "subtest6": "subvalue2"}, {"subtest7": "subvalue2", "subtest8": "subvalue2"}]}
# 
# Caution: replace this file's contents into app/__init__.py and build, then test 

import json
import multiprocessing

def process_data(key_value, pipe):
    # Do the job for the key-value pair
    result = None
    if key_value[0] == "test1":
      result = key_value[1].replace("value", "first")
    elif key_value[0] == "test2":
      result = list(map(lambda x: x.replace("value", "first"), key_value[1]))
    elif key_value[0] == "test3":
      result = list(map(lambda x: x*3, key_value[1]))
    elif key_value[0] == "test4":
      result = list(map(lambda x: json.dumps(x), key_value[1]))
        
    # Send the key and result back to the parent process
    pipe.send((key_value[0], result))
    pipe.close()


def handler(event, context):
  with open('app/test.json', 'r') as f:
      json_data = json.load(f)
  
  key_values = [(k, v) for k, v in json_data.items()]
  
  # Create a list of processes, one for each key-value pair
  processes = []
  for key_value in key_values:
      parent_conn, child_conn = multiprocessing.Pipe()
      p = multiprocessing.Process(target=process_data, args=(key_value, child_conn))
      processes.append((p, parent_conn))
      p.start()
  
  # Collect the results from the child processes
  results = {}
  for p, parent_conn in processes:
      key, value = parent_conn.recv()
      results[key] = value

  # Return the results
  return {
      'statusCode': 200,
      'body': json.dumps(results)
  }
