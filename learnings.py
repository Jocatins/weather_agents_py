# * to unpack lists

cat = ["white", 4, "cheese", "milk", 56]

name, legs, *chow = cat

print(name)
print(legs)

# * unpack a list as function arguments

def test(x,y,z):
    print(f'{x=} {y=} {z=}')
    
numbers = [2,4.3,8]
    
test(*numbers)

# zip() to iterate through 2 lists concurrently

items = ["baywatch", "the matrix", 'vampire-seasons', "callous"]
prices = [98,45,23, 8]
venues = ["stadium", "mainland", "gardens"]

# for f, p, v in zip(items, prices, venues):
#     print(f,p,v)
    
#  enumerate() to generate both index and value during iteration
# for index, item in enumerate(items):
#     print("enumerate",index, item)

# .sort() vs sorted()
ls = [3,6,2,1,6,3,2,4,9,89]
new = ls.sort()
new1 = sorted(ls)

# print("new",new)
print(ls)
print(f"sorted", new1)

#  .sort() with custom condition
sortLs = [45, 67, 54, 98]

# def condition(num):
#     return num % 10


# sortLs.sort(key=condition)
# Or Lambda function
sortLs.sort(key=lambda n: n % 10)

print(sortLs)

fruits = ['apple', 'orange', 'pear']
newFruits = [f.upper() for f in fruits if len(f)>=5]

# for fruit in fruits:
#     newFruits.append(fruit.upper())
    
print(newFruits)

# Tuples vs Lists

