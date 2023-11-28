def get_max_two(nums):
    # Base case: if the array has only one element, return it as the largest and -∞ as second largest
    if len(nums) == 1:
        return (nums[0], float('-inf'))
    
    # Base case: if the array has two elements, return the larger as the largest and the smaller as the second largest
    if len(nums) == 2:
        return (max(nums), min(nums))
    
    # Divide the array into two halves
    mid = len(nums) // 2
    left = nums[:mid]
    right = nums[mid:]
    
    # Conquer: Recursively find the largest and second largest on each half
    (left_max, left_second) = get_max_two(left)
    (right_max, right_second) = get_max_two(right)
    
    # Combine: Find the largest and second largest from the pairs returned by the recursive calls
    if left_max > right_max:
        overall_max = left_max
        overall_second = max(left_second, right_max)
    else:
        overall_max = right_max
        overall_second = max(right_second, left_max)
    
    return (overall_max, overall_second)


print(get_max_two([1,4,5,3,6,12,34,2,4,1]))