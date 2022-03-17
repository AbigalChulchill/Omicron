import re
import os
from os import walk
from ast import literal_eval
import fileinput

class txt_Ops():



    

    def quick_read_txt_file(self,file_path):

        input_str = ''
        return_str = ''

        if os.path.exists(file_path):
            try:
                with open (file_path, "r") as f:
                    input_str = str(f.readlines())
                return_str = input_str[2:-2]
                #print('Read from text file:',return_str)
            except:
                print("\nQuick Read | Unknown error: Unable to read file! (File already open?)\n")
        else:
            print("\nQuick Read | Error: File path does not exist for operation.\n")

        return return_str




    def delete_Blank_Lines(self,file_path):
        for line in fileinput.FileInput(file_path,inplace=1):
            if line.rstrip():
                print(line)

    def quick_write_txt_file(self,file_path,val_to_write):
        if os.path.exists(file_path):
            try:
                with open(file_path, "w") as myfile:
                    myfile.write(str(val_to_write))
                    myfile.close()
            except:
                print("\nQuick Write | Error: Unable to write to file!\n")
        else:
            print("\nQuick Write | Error: File path does not exist for operation!\n")


    def quick_write_txt_file_plus(self,file_path,val_to_write):
        try:
            with open(file_path, "w+") as myfile:
                myfile.write(str(val_to_write))
                myfile.close()
        except:
            print("\nQuick Write | Error: Unable to write to file!\n")

    def create_dict_from_txt(self,file_path,split_symbol):
        dictionary = {}
        if os.path.exists(file_path):
            try:
                with open (file_path, "r") as hfile:
                    sp = hfile.read()
                lines = sp.split("\n")
                for line in lines:
                    if line != "" and line != "\n":
                        parts = line.split(split_symbol)
                        dictionary[parts[0]] = parts[1]
                #print("\nCreate Dict | Success: Created dictionary from text file",dictionary,"\n")
            except:
                print("\nReplace Line | Error: Unknown issue, please check dictionary split symbol is correct.\n")
        else:
            print("\nCreate Dict | Error: File path does not exist for operation!\n")
        return dictionary





    def replace_Specific_Line(self,file_path,line_number,line_content):
        read_lock = 0
        read_lock_str = self.quick_read_txt_file('txt/settings/replace_line_lock.txt')
        try:
            read_lock = int(read_lock_str)
        except:
            read_lock = 1
        if read_lock == 0:
            write_lock = self.quick_write_txt_file('txt/settings/replace_line_lock.txt',1)
            old_line = ''
            if os.path.exists(file_path):
                try:
                    with open (file_path, "r") as f:
                        get_all = f.readlines()
                    with open(file_path,'w') as f:
                        for i,line in enumerate(get_all,1):            
                            if i == int(line_number):
                                old_line = line.replace("\n", "")
                                f.writelines(str(line_content) + '\n')
                            else:
                                f.writelines(line)
                    release_lock = self.quick_write_txt_file('txt/settings/replace_line_lock.txt',0)
                    #print("\nReplace Line | Success: Line",line_number,"with value [" + old_line +\
                          #"] has been replaced with [" + line_content + ']\n')
                except:
                    #print("\nReplace Line | Error: Unknown issue while attempting to replace line.\n")
                    release_lock = self.quick_write_txt_file('txt/settings/replace_line_lock.txt',0)
            else:
                #print("\nReplace Line | Error: File path does not exist for operation.\n")
                release_lock = self.quick_write_txt_file('txt/settings/replace_line_lock.txt',0)
        else:
            #print("\nReplace Line | Error: File appears to be locked!\n")
            pass


    def quick_append_txt_file(self,file_path,val_to_write):
        if os.path.exists(file_path):
            try:
                with open(file_path, "a+") as myfile:
                    myfile.write(str(val_to_write))
                    myfile.close()
            except:
                print("\nQuick Append | Error: Unable to append to file!\n")
        else:
            pass
            #print("\nQuick Append | Error: File path does not exist for operation.\n")
      




    def txt_total_comma_values(self,file_path):

        floats_total = float(0.00)

        in_file = open(file_path, 'r')
        
        for line in in_file:
            
            float_counter = 0
            
            for num in line.strip().split(','):
                
                float_counter += float(str(num))
                
            floats_total = ("%d\n" % float_counter)

        return floats_total



    

    def txt_count_pos_neg(self,ignore_limit):

        if ignore_limit == 0:

            ignore_limit = ignore_limit + 999999999

            

        file_path = 'txt/global_pnl.txt'

        losses_array=[]
        wins_array=[]

        wins = 0
        losses = 0
        stale_mate = 0

        average_win = 0
        average_loss = 0

        ratio=0

        in_file = open(file_path, 'r')
        
        
        for line in in_file:
            
            #float_counter = 0
            
            for num in line.strip().split(','):
                
                #float_counter += float(num)

                if float(num) < 0:

                    losses += 1

                    losses_array.append(float(num))

                elif float(num) > 0 and float(num) < ignore_limit: #1000 to prevent acc add

                    wins += 1

                    wins_array.append(float(num))

        no_of_wins = len(wins_array )

        no_of_losses = len(losses_array )

        if len(wins_array) > 0 and len(losses_array) > 0:

            average_win = float("%.2f"%(   sum(wins_array)/len(wins_array )    ))

            average_loss = float("%.2f"%(   abs(sum(losses_array)/len(losses_array )  )  ))

            total_win_amount = float("%.2f"%(  sum(wins_array)  ))

            total_loss_amount = float("%.2f"%( abs( sum(losses_array) ) ))

            ratio = float("%.2f"%( total_win_amount/total_loss_amount))

            print("\nNumber of wins:",no_of_wins)
            print("\nNumber of losses:",no_of_losses)
            print("\n---")
            print("\nTotal win amount: $",total_win_amount)
            print("\nTotal loss amount: $",total_loss_amount)
            print("\n---")
            print("\nAverage win amount: $",average_win)
            print("\nAverage loss amount: $",average_loss)
            print("\n---")
            print("\nTaking into account weighting, You win",ratio,"times more often than losing.")


        elif len(wins_array) > 0 and len(losses_array) == 0:

            ratio = 100

        elif len(wins_array) == 0 and len(losses_array) > 0:

            ratio = -1

        else:

            print("\nNot enough data to analyze win/loss ratio...")

        print(wins_array)

        return total_win_amount,total_loss_amount,ratio,average_win,average_loss




    def find_Digit_Before_Dot(self,input_float):

        input_str = str(input_float)

        for i in range(len(input_str)):

            if input_str[i] == '.':

                #print("\nFound a dot:",input_str[i-1]+input_str[i],"\n")

                return input_str[i-1]





    def find_Two_Digits_Before_Dot(self,input_float):

        input_str = str(input_float)

        for i in range(len(input_str)):

            if input_str[i] == '.':

                value_1 = str(input_str[i-1])
                value_2 = str(input_str[i-2])

                value_comb = value_2 + value_1

                return value_comb





    def find_Chars_Before_Symbol(self,input_str,symbol_to_find,how_may_chars):

        for i in range(len(input_str)):

            if input_str[i] == symbol_to_find:

                return_str = input_str[(i-how_may_chars):i]
                
                #print("\nFound char:",symbol_to_find,"| Previous",how_may_chars,"chars:",return_str,"\n")

                return return_str
        


        
    def read_commas_into_array(self,file_path,num_switch):

        results_array = []

        float_counter = 0

        in_file = open(file_path, 'r')
        
        for line in in_file:
            
            
            
            for num in line.strip().split(','):
                
                float_counter += 1

                if num_switch == 1:

                    results_array.append(float(num))

                elif num_switch == 3:

                    results_array.append(int(num))

                else:

                    results_array.append(num)

        #print("\nRead",float_counter,"results into an array.")
                
            

        return results_array





    def get_Array_From_Txt_Dict(self,file_path,cell_id,separator_symbol):
        read_array = []
        read_dict = {}
        if os.path.isfile(file_path):
            read_dict = self.create_dict_from_txt(file_path,separator_symbol)
            try:
                read_array = literal_eval(read_dict[cell_id])
            except:
                print("\nError: Literal eval read issue.")
            read_array_length = len(read_array)
            if read_array_length > 0:
                print("\nReading array from txt dict:\n")
                for i in range(read_array_length):
                    print("Array item " + str(i+1) + ":",read_array[i])
            else:
                print("\nWarning: Array contains no elements...")
        else:
            print("\nError: File does not exist!")
        return read_array







    def find_All_Numbers_Dots(self,source_string):

        new_str = ''
 
        get_digits = re.findall(r"([0-9.]*[0-9]+)",source_string)

        for i in range( len(get_digits) ):
            new_str = new_str+str(get_digits[i])

        final_val = float(new_str)

        return final_val



def check_Module():
    
    txt_ops = txt_Ops()

    txt_ops.delete_Blank_Lines('txt/ethaddy2.txt')





if __name__==('__main__'):
    check_Module()




