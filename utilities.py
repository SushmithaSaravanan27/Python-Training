import string_ops
import math_ops 
import file_ops 
string=input("enter the string:")
print(string_ops.removePunctuation(string))
print(string_ops.count_vowels(string))
num=list(map(int,input("Enter the number:").split()))
print(math_ops.mean(num))
print(math_ops.find_median(num))
file_name=input("Enter the filename:")
print(file_ops.read_file(file_name))
print(file_ops.write_file(file_name))
