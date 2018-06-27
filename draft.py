
some_list = [2343, 323, 34254, 49, 595]
sorted_list = sorted(some_list, key=lambda x : x%10)
print(sorted_list)


def custom_compare(x, y):
    return x % 10 - y % 10


print(sorted(some_list, cmp=custom_compare))
