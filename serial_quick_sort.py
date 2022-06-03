def serial_quick_sort(array):
    """Sort the given array by using quicksort."""
    
    lower_values = [] # compared to pivot element
    equal_values = []
    larger_values = []

    # sort the values to the different buckets
    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if x < pivot:
                lower_values.append(x)
            elif x == pivot:
                equal_values.append(x)
            elif x > pivot:
                larger_values.append(x)
        
        # join the results
        return serial_quick_sort(lower_values) + equal_values + serial_quick_sort(larger_values)

    else:  
        return array
