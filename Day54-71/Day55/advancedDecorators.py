#Decorators for Day55.py for bold, underline and emphasis.
import functools
 
class TextDecorators:

    @staticmethod
    def make_bold(function):
        @functools.wraps(function)
        def wrapper():
            return f"<b>{function()}</b>"
        return wrapper
    
    @staticmethod
    def make_underline(function):
        @functools.wraps(function)
        def wrapper():
            return f"<u>{function()}</u>"
        return wrapper
    
    @staticmethod
    def make_emphasis(function):
        @functools.wraps(function)
        def wrapper():
            return f"<em>{function()}</em>"
        return wrapper
    
class HighLowGame:

    @staticmethod
    def checker(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            guess,answer = function(*args,**kwargs)
            if not answer:
                return '0'
            if guess<answer:
                return  "<h1>Too Low!!</h1>" \
                        "<img src='https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif'>" \
                        f"<h1>{answer}</h1>"
            elif guess>answer:
                return  "<h1>Too High!!</h1>" \
                        "<img src='https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif'>" \
                        f"<h1>{answer}</h1>"
            else:
                return  "<h1>Congrats You got it right</h1>" \
                        "<imh src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif'>" \
                        "<a href='http://127.0.0.1:5000/'>Click Here to Reset the Game.</a>" \
                        f"<h1>{answer}</h1>"
        return wrapper

# # Concentional Decorators
# import functools

# class TextDecorators: # Better class name
    
#     @staticmethod
#     def tag_decorator_factory(tag_name): # A factory that takes the tag
#         def decorator(function):
#             @functools.wraps(function) # CRITICAL IMPROVEMENT
#             def wrapper(*args, **kwargs):
#                 result = function(*args, **kwargs)
#                 return f"<{tag_name}>{result}</{tag_name}>"
#             return wrapper
#         return decorator

# # Usage:
# decorate = TextDecorators()

# @decorate.tag_decorator_factory('b')
# def greet():
#     return "Hello"

# print(greet.__name__) # Output: greet (because of @functools.wraps)
# print(greet())        # Output: <b>Hello</b>

# Exercise
# import functools
# # TODO: Create the logging_decorator() function 👇
# def logging_decorator(function):
#     @functools.wraps(function)
#     def wrapper(*args):
#         print(f"You called {function.__name__}{args}")
#         result = function(*args)
#         print(f"It returned: {result}")
#         return result
#     return wrapper

# # TODO: Use the decorator 👇
# @logging_decorator
# def a_function(*args):
#     return sum(args)
    
# a_function(1,2,3)

# more Exercise

# class User:
#     def __init__(self, name):
#         self.name = name
#         self.is_logged_in = False

# def is_authenticated_decorator(function):
#     def wrapper(*args, **kwargs):
#         if args[0].is_logged_in == True:
#             function(args[0])
#     return wrapper

# @is_authenticated_decorator
# def create_blog_post(user):
#     print(f"This is {user.name}'s new blog post.")

# new_user = User("angela")
# new_user.is_logged_in = True
# create_blog_post(new_user)