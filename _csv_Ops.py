import csv




class csv_Ops():

    
    def __init__(self):

        self.object_ID = self
        #print(self.object_ID)




    def add_If_No_Duplicate_Record(self,value_to_find,in_column,return_column,search_limit):

        value_to_find_str = 'find_val=' + str(value_to_find)

        search_limit_str = 'limit=' + str(search_limit)

        in_column_str = 'match_col=' + str(in_column)

        return_column_str = 'return_col=' + str(return_column)

        get_matches = self.csv_ops.match_Last_CSV_Rows(file_path,in_column_str,find_val_str,return_column_str,limit_str)

        match_flag = get_matches[0]

        return_val = get_matches[1]

        if match_flag == 'NO_MATCH':
            append_to_csv = self.csv_ops.append_to_CSV(file_path,row)
            print('\n* No match in previous',limit,'rows, appending to CSV file:',file_path,'*')

        elif match_flag == 'MATCH':
            print('\n* This entry was previously recorded to the CSV file, skipping... *')

        print('\n//////////////////////////////////////////////////////////////////////\n\n')

        return match_flag

               




























    def append_to_CSV(self,file_name,row_array):

        data_row = [row_array]

        myFile = open(file_name,'a',newline='')

        with myFile:
            writer = csv.writer(myFile)
            writer.writerows(data_row)

        myFile.close()

        #print("\nData row appended to CSV file",file_name)

        



    def write_to_CSV(self,file_name,row_array):

        try:

            data_row = [row_array]

            myFile = open(file_name,'w',newline='')

            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(data_row)

            myFile.close()

        except:

            pass

        #print("\nData row written (destructive) to CSV file",file_name)


        



 

    def read_Last_CSV_Rows(self,file_name,limit):
       
        results_array = []

        #input variable str processing - convert line to int
        limit = int(str(limit).replace('limit=',''))

        with open(file_name, 'r') as f:

            if limit != 0:

                read_list = list(csv.reader(f))[-int(limit-1)-1:]

            else:

                read_list = list(csv.reader(f))

            #print("\nread_list:",read_list)
            
            row_length = len(read_list)

            #print("\nrow_length:",row_length)
            
            for row in read_list:

                #print(row)

                

                if row != [''] and row != [] and row != '' and len(row) > 0:

                    #print(row)
                
                    data = ', '.join(row)
                
                    row = [x.strip() for x in data.split(',')]
                
                    #print("\nRequested row:",row)
                
                    results_array.append(row)

            #example use
            #last_row = csv_ops.read_Last_CSV_Rows('csv/whales.csv','limit=5')

            #print("\nget last rows,results_array",results_array,len(results_array))

            f.close()

        return results_array
    





    def match_Last_CSV_Rows(self,file_name,match_col,find_val,return_col,limit):

        #uses 0,1,2 indexing from zero

        status = 'NO_MATCH'
        
        return_val = '' #if '' is returned nothing was matched

        #string clean-up ops
        limit = int(str(limit).replace('limit=',''))
        match_col = int(str(match_col).replace('match_col=',''))
        return_col = int(str(return_col).replace('return_col=',''))
        find_val = str(find_val).replace('find_val=','')
        
        get_rows = self.read_Last_CSV_Rows(file_name,limit)

        #print("\nget_rows:",get_rows)
        
        get_rows_length = len(get_rows)

        #print("\nScanning",limit,"rows for value:",find_val)

        for i in range(get_rows_length):

            #print("\nget_rows[i]",get_rows[i],len(get_rows[i]))

            if get_rows[i] != '' and get_rows[i] != [''] and get_rows[i] != [] and len(get_rows[i]) > 1:

                search_val = get_rows[i][match_col]

                #print("get_rows[i]",get_rows[i])

                if search_val == find_val:

                    status = 'MATCH'

                    return_val = get_rows[i][return_col]

                    #print("\nRow",str(i+1),"|",search_val,"| MATCH FOUND | Return value:",return_val)

                


        return status,return_val

            



    def match_Last_CSV_Rows_Enhanced(self,file_name,match_col,find_val,return_col,limit,reverse):

        #uses 0,1,2 indexing from zero

        status = 'NO_MATCH'
        
        return_val = '' #if '' is returned nothing was matched

        #string clean-up ops
        limit = int(str(limit).replace('limit=',''))
        match_col = int(str(match_col).replace('match_col=',''))
        return_col = int(str(return_col).replace('return_col=',''))
        find_val = str(find_val).replace('find_val=','')
        
        get_rows = self.read_Last_CSV_Rows(file_name,limit)

        if reverse == 1:
            get_rows.reverse()

        #print("\nget_rows:",get_rows)
        
        get_rows_length = len(get_rows)

        #print("\nScanning",limit,"rows for value:",find_val)

        for i in range(get_rows_length):

            #print("\nget_rows[i]",get_rows[i],len(get_rows[i]))

            if get_rows[i] != '' and get_rows[i] != [''] and get_rows[i] != [] and len(get_rows[i]) > 1:

                search_val = get_rows[i][match_col]

                #print("get_rows[i]",get_rows[i])

                if search_val == find_val:

                    status = 'MATCH'

                    return_val = get_rows[i][return_col]

                    #print("\nRow",str(i+1),"|",search_val,"| MATCH FOUND | Return value:",return_val)

                


        return status,return_val

            





    def find_Val_Row_Repl_Adj_Field(self,filename,file_total_cols,find_value,find_value_col,replace_with_val,replace_with_val_col):

        row_array = []

        with open(filename) as inf:
            reader = csv.reader(inf.readlines())

        with open(filename, 'w', newline='') as outf:
            writer = csv.writer(outf)

            for line in reader:

                if line != [] or line != '': #ignore blanks

                    

                    if str(line[find_value_col]) == str(find_value):

                        #create replace row
                        for i in range(file_total_cols):#4 is column number real
                            if i == replace_with_val_col:
                                row_array.append(replace_with_val)
                            else:
                                row_array.append(line[i])

                        writer.writerow(row_array)
                        break
                    else:
                        writer.writerow(line)

            writer.writerows(reader)
        




        



def check_Module():

    csv_ops = csv_Ops()

    #a = csv_ops.write_to_CSV('csv/test.csv', [1,2,3] )
    #print('a:',a)

    #b = csv_ops.append_to_CSV('csv/test.csv', [4,5,6] )
    #print('b:',b)

    #c = csv_ops.read_Last_CSV_Rows('csv/whales.csv','limit=2') 
##    #print('\nread_Last_CSV_Rows,limit=2:',c)
##
##    csv_file = 'csv/pos_data/pos_data_' + str(2) + '.csv'
##    last_row = csv_ops.read_Last_CSV_Rows(csv_file,2)[-1][0]
##
##    
##    #last_row = csv_ops.read_Last_CSV_Rows('csv/whale_data/whales.csv','limit=1')
##    print('\nread_Last_CSV_Rows:',last_row)
##


    #replace specific field
    #def find_Val_Row_Repl_Adj_Field(self,filename,total_col_num,find_value,find_value_col,replace_with_val,replace_with_val_col):
    #replace = csv_ops.find_Val_Row_Repl_Adj_Field('csv/test/test.csv',4,'16500',0,'17000',0)



    #row = [account_no,pair_symbol,start_time,entry_price,target_price,0,0,'ACTIVE']
    match_row = csv_ops.match_Last_CSV_Rows('csv/test/test.csv','match_col=2','find_val=12','return_col=0','limit=99') 
    print('\nmatch_Last_CSV_Rows,limit=12:',match_row)


if __name__ == '__main__':
    
    check_Module()  



