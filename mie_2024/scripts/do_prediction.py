# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 13:44:16 2024

@author: ellio
"""

import sys, datetime, subprocess, platform, os
from user_input import user_input
when = str(datetime.datetime.now())[:17].replace(' ', '_').replace(':', '.')

welcome = '''This program combs through results of program1 (or any other directory containing .fasta files) and automates product prediction by antiSMASH.
Product prediction may take considerable time - antiSMASH will supply reporting on product prediction status automatically. Please take care when providing input and output folder paths.'''

error_message = '''As a start to interpreting the auto-generated error message, some common issues include:
    - command line arguments entered out of order
    - improperly converted file paths for your operating system
    - improperly written outputs of program 1
    - failure to set a conda environment with access to antiSMASH
    - issues with your antiSMASH installation.'''

def close_out(error, step):
    print('Something went wrong. Please see auto-generated error information below:')
    print(type(error).__name__, "-", error)
    print('Step impacted: ', step)
    print(error_message)
    sys.exit()

def user_info(when):
    print('Input/Output Information', '-'*(os.get_terminal_size()[0]-25))
    #PATH IN
    convert_path = user_input(name='convert_path',
                              prompt='Would you like to utilize path conversion?',
                              gate_type='preference',
                              ).value_received
    
    path_in = input('Full path to folder containing .fasta files: ')
    if convert_path == True:
        path_in = WL_conversion(path_in)
    if os.path.exists(path_in) == False:
        print('File/path not found. Please check the location of your file/path and try again.')
        sys.exit()
    
    #PATH OUT
    path_out = input('Full output path: ')
    if convert_path == True:
        path_out = WL_conversion(path_out)
    if os.path.exists(path_out) == False:
        print('File/path not found. Please check the location of your file/path and try again.')
        sys.exit()
    return path_in, path_out

def WL_conversion(path):
    linux_path = '/mnt/' + path.replace('C:', 'c').replace("\\", "'/'")
    return linux_path

def prepare(path_in, path_out):
    
    p1 = path_in.split('/')[-1]
    p2 = f'{p1}---{when}p2'
    
    try:
        files = str(subprocess.check_output(['ls', path_in])).strip('b\'').split('\\n')[:-1]
        files = [f for f in files if '.fasta' in f]
        print('Found', len(files), 'results from program1 to run.')
    except Exception as error:
        close_out(error, 'Accessing .fasta outputs from you unix system or virtual machine via your 2nd argument.')
    
    try:    
        subprocess.call(['mkdir', f'{path_out}/{p2}'])
    except Exception as error:
        close_out(error, 'Creating a new path to a folder interpretable by your unix system or virtual machine using your 3rd argument.')
    print(f'New folder created: {path_out}/{p2}\n')
    return files, p2

def run(files, path_in, path_out,  p2):
    for file in files:
        income = path_in + '/' + file
        outgo = path_out + '/' + p2 + '/' + file.strip('.fasta')
        print('\nRunning antiSMASH for', file)
        subprocess.call(['antismash', income,
                        '--genefinding-tool', 'prodigal',
                        '--output-dir', outgo])
    print('\nProduct prediction completed.')
    
def main(welcome, when):
    
    if input('Press (W) to see a welcome message, To continue, press any other key. ').lower() == 'w':
        print('-'*os.get_terminal_size()[0])
        print(welcome)
        print('Please ensure all system and environment information is as expected before continuing.')
        print('\tOperating system: ', platform.system())
        print('\tWorking directory: ', os.getcwd())
        if 'CONDA_PREFIX' in os.environ.keys():
            print('\tPython environment: ', os.environ['CONDA_PREFIX'])
    else:
        pass
    path_in, path_out = user_info(when)
    files, p2 = prepare(path_in, path_out)
    run(files, path_in, path_out, p2)
    
if __name__ == "__main__":
    main(welcome, when)
    