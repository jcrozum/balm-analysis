import mtsNFVS as mt
import sys
import os
import time
import subprocess

start_time = time.time()

#print("Analyzing network . . .")
bn_file = sys.argv[1]
bn_name = bn_file.replace(".bnet", "")
an_file = "predata/" + bn_name + ".an"

mts_file = open("predata/" + bn_name + ".mts", "w")
std_file = open("predata/" + bn_name + ".std", "w")
result_file = open("results/" + bn_name + ".bnet", "w")

write_file_time = mt.compute_attractors("networks/" + bn_file, mts_file=mts_file, std_file=std_file, result_file=result_file)
mts_file.close()
std_file.close()
result_file.close()

try:
    subprocess.call(['java', '-jar', 'bioLQM.jar', "networks/" + bn_file, an_file])
    subprocess.call(['java', '-jar', 'mtsNFVS.jar', bn_file])
except Exception as e:
    print("Exception", e)

#print("Analysis complete.")

running_time = "%.2f" % (time.time() - start_time - write_file_time)
print ("Running time : " + running_time + " secs")

