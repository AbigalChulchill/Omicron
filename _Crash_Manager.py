from _Maths_Functions import *
from _txt_Ops import *
import glob 
import errno 
from playsound import playsound     

class Crash_Manager:

    def __init__(self):
        self.maths_functions = Maths_Functions(1)
        self.txt_ops = txt_Ops()
        self.folder_path = 'txt/clock_check/*.txt'
        self.busy_path = 'txt/busy/*.txt'
        self.files = glob.glob(self.folder_path)
        self.busy_files = glob.glob(self.busy_path)
        self.warning_seconds = 300
        self.busy_array = []
        #print("self.files:",self.files)

        
##    def login_Counter(self):
##        folder_count = self.maths_functions.count_Files(self.folder_path)[0]
##        return folder_count

    def check_Modules_Alive(self):

      
        current_time = int(time.time())
        print("Check Modules Alive | Current time:",current_time,"\n")

        #for i in range(self.login_Counter()):
            #time_value = self.txt_ops.quick_read_txt_file

        
        for name in self.files: 
            try: 
                with open(name) as f: 
                    #print(f)
                    read_file_contents = str(self.txt_ops.quick_read_txt_file(name))
                    unix_time = float(read_file_contents)
                    print(name,unix_time)
                    time_diff = current_time - unix_time
                    print("--time_diff",time_diff)
                    if time_diff > self.warning_seconds:


                        
                        #check backend timeout not due to position entry loop
                        for b_name in self.busy_files: 
                            try: 


                                with open(b_name) as b: 
                                    #print(f)
                                    read_file_contents = str(self.txt_ops.quick_read_txt_file(b_name))
                                    read_val = int(read_file_contents)
                                   
                                    self.busy_array.append(read_val)

                                


                            except IOError as exc: 
                                if exc.errno != errno.EISDIR: 
                                    raise


                        print(self.busy_array)     
                        if sum(self.busy_array) >= 1:
                            print("\nCrash Manager | Backend module timeout due to ongoing position entry, skipping...")
                        elif sum(self.busy_array) < 1:
                            print("\nCrash Manager | Error | An Omicron module has stopped working!")
                            playsound('audio/warning_module_down.wav')













                        
            except IOError as exc: 
                if exc.errno != errno.EISDIR: 
                    raise



            
if __name__==('__main__'):
    c = Crash_Manager()
    run_check = c.check_Modules_Alive()
    

        

