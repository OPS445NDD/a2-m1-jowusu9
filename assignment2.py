#!/usr/bin/env python3

'''
OPS445 Assignment 2 - Winter 2023
Program: assignment2.py 
Author: "Jude Owusu"
The python code in this file is original work written by
"Jude Owusu". No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: Curerntly compeleting milestone one 

Date: 2026-07-18

'''

import argparse
import os
import sys

def parse_command_args() -> object:
    "Set up argparse here. Call this function inside main."
    parser = argparse.ArgumentParser(description="Memory Visualiser -- See Memory Usage Report with bar charts",epilog="Copyright 2023")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    # Create an entry for human-readable. Check the docs to make it a True/False option.
    parser.add_argument("program", type=str, nargs='?', help="if a program is specified, show memory use of all associated processes. Show only total use if not.")
    args = parser.parse_args()
    return args

def percent_to_graph(percent: float, length: int=20) -> str:
    "turns a percent 0.0 - 1.0 into a bar graph"
    #Scale the percent to a number of '#' symbols using the bar length.
    #round() ensures 0.65 * 20 = 13 hashes, not 12 (which int() would give) 
    num_hashes = round(percent * length)
    #Fill the remaining characters with spaces so the bar is always `length` wide
    return '#' * num_hashes + ' ' * (length - num_hashes)


def get_sys_mem() -> int:
    "return total system memory (used or available) in kB"
    #open the meminfo file to do this!
    with open('/proc/meminfo', 'r') as mem_file:
    #MemTotal is always the first line, so readline reads just what we need
            line = mem_file.readline()
    #Split()[1] grabs the number. format is "MemTotal:    15221204 kB"
            return int(line.split()[1])
    

def get_avail_mem() -> int:
    "return total memory that is currently available"
    # open the meminfo file to do this!
    mem_free = 0
    swap_free = 0

    #/proc/meminfo is a kernel file that exposes live system memory stats
    with open('/proc/meminfo', 'r') as mem_file:
                lines = mem_file.read().splitlines()
    for line in lines:
        #MemAvailable is the most accurate value on standard Linux return immediately
        if line.startswith('MemAvailable:'):
             return int(line.split()[1])
        #Save in case we need the WSL fallback
        elif line.startswith('MemFree:'):
            mem_free = int(line.split()[1])
        #Save in case we need the WSL fallback
        elif line.startswith('SwapFree:'):
            swap_free = int(line.split()[1])
        
        #MemAvailable is absent on WSL, so approximate with MemFree + SwapFree
    return mem_free + swap_free
    

def pids_of_prog(app_name: str) -> list:
    "given an app name, return all pids associated with app"
    # please use os.popen('pidof <app>') to do this!
    pass

def rss_mem_of_pid(proc_id: str) -> int:
    "given a process id, return the Resident memory used"
    # for a process, open the smaps file and return the total of each
    # Rss line.
    pass

def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str:
    "turn 1,024 into 1 MiB, for example"
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']  # iB indicates 1024
    suf_count = 0
    result = kibibytes 
    while result > 1024 and suf_count < len(suffixes):
        result /= 1024
        suf_count += 1
    str_result = f'{result:.{decimal_places}f} '
    str_result += suffixes[suf_count]
    return str_result

if __name__ == "__main__":
    args = parse_command_args()
    if not args.program:  # no program name specified — show total system memory usage
        total = get_sys_mem()
        avail = get_avail_mem()
        used = total - avail                    # memory in use = total minus what's available
        percent = used / total                  # fraction used, between 0.0 and 1.0
        bar = percent_to_graph(percent, args.length)
        percent_int = round(percent * 100)
        print(f"{'Memory':<15}[{bar} | {percent_int:>2}%] {used}/{total}")
    else:
        pass
