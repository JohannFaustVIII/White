import datetime

def measure_time(label, func):
  print(f'Starting "{label}"')
  start = datetime.datetime.now().replace(microsecond=0)
  returned_val = func()
  end = datetime.datetime.now().replace(microsecond=0)
  print(f'"{label}" finished in {end-start}')
  return returned_val