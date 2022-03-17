import array

class Array_Functions():


    def __init__(self):
        pass



    def intersect(self,arr1,arr2):
        results = list(filter(lambda x: x in arr1, arr2)) 
        print(arr1,arr2,"Intersect",results)
        return results
      
    def difference(self,arr1,arr2):
        results = list(filter(lambda x: x not in arr1, arr2)) 
        #print("\n",arr1)
        #print("\n",arr2)
        print("\n Difference:",results)
        return results



    def remove_Duplicates(self,arr1):
        results = list(dict.fromkeys(arr1))
        print(results)
        return results

    def order_Numbers(self,arr1):
        results = sorted(arr1)
        print(results)
        return results

    def reverse(self,arr1):
        results = list(reversed(arr1))
        print(results)
        return results


        
    def symbol_Sep_To_Array(self,file_path,symbol,mode):

        results_array = []

        in_file = open(file_path,'r')
        
        for line in in_file:
            for num in line.strip().split(symbol):
                if mode == 'string':
                    results_array.append(num)
                elif mode == 'float':
                    results_array.append(float(num))

        print(results_array)
        
        return results_array




if __name__ == "__main__":

    man = Array_Functions()
    
    #arr1 = ['BTCUSDT','ETHUSDT','LTCUSDT','BNBUSDT','ADAUSDT']
    #arr2 = ['BTCUSDT','ETHUSDT','LTCUSDT','BNBUSDT']
    
    #find intersect
    #a = man.difference(arr2,arr1)

    b = man.symbol_Sep_To_Array("test.txt",",","float")[-1]

    print(b)

    #remove duplicates
    #b = man.remove_Duplicates(arr1)

    #c = man.order_Numbers(arr1)
    #d =  man.remove_Duplicates(c)
    #e = man.reverse(d)

    
