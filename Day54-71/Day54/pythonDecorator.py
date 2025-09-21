import time
# Python decorator - Syntaxtic Sugar

# Nested Funtions

def outside_function():
    print("I'm Outer Function.")

    def nested_function():
        print("I'm Inner Function.")
    
    return nested_function

inner_function = outside_function()
inner_function()


# Decorators

def delay_decorator(function):
    def wrapper_function(param1='a',param2='a',n:int=1,l:list=[0]):
        print(param1,"",param2)
        print(l)
        time.sleep(n)
        function()
    return wrapper_function

@delay_decorator
def say_hello():
    print("Hello!!")

say_hello("Hi","Hello",3,[1,2,3,4])

# same as - 
# decorated_function = delay_decorator(say_hello) 
# decorated_function("h","h2",1,[0,1,2]) - something wierd is happening but same ig. 

# Exercise
import time
current_time = time.time()
print(current_time) # seconds since Jan 1st, 1970 

# Write your code below 👇

def speed_calc_decorator(function):
  
  def wrapper_function():
      function()
      print(f"{function.__name__} run speed {time.time()-current_time}")
  return wrapper_function
    
@speed_calc_decorator
def fast_function():
  for i in range(1000000):
    i * i
        
@speed_calc_decorator
def slow_function():
  for i in range(10000000):
    i * i

fast_function()
slow_function()