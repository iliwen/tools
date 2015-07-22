import argparse
import sys
import os
import shutil
import logging
import linecache
import time
import re

class CopyTool:
    def __init__(self, args):
        
        if not os.path.exists(args.source_file):
            print >> sys.stderr,"Source file don't exist! Please check!"     
        if not os.path.exists(os.path.dirname(args.target_file)):
            os.mkdir(os.path.dirname(args.target_file))
            
        self.target_file = args.target_file
        self.source_file = args.source_file
        self.indexs = args.part_copy
        self.keywords = args.keywords_copy
        self.current_time = time.time()
    
    def full_copy(self):
        shutil.copy(self.source_file, self.target_file)

    def part_copy(self):
        """
        """
        try:
            firstLine,endLine = self.indexs.strip(" ").split(",")

            #fileRead = open(self.source_file, 'r') 
            fileWrite = open(self.target_file, 'w')

            for lineNum in range(int(firstLine), int(endLine), 1):
                fileWrite.write(linecache.getline(self.source_file, lineNum))
                print linecache.getline(self.source_file, lineNum)
            linecache.clear()

            #fileRead.close()
            fileWrite.close()
            print "part copy finish"
        except ValueError:
            print >> sys.stderr,"we need two int(type) params, firstLine and endLine."
            pass

    def keywords_copy(self):
        keywords = self.keywords.replace(',','|')

        fileRead = open(self.source_file, 'r')
        fileWrite = open(self.target_file, 'w')
        for line in fileRead:
            if re.match(keywords, line):
                fileWrite.write(line)

        fileRead.close()
        fileWrite.close()

if __name__ == '__main__':
    """
    copy tools for three means of copying file.
    """

    #input argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source_file", help = "the source file that the coper is from.")
    parser.add_argument("-t", "--target_file", help = "the target file that the coper goes to.")
    parser.add_argument("-f", "--full_copy", help = "copy source file fully to target file.", action = "store_true")
    parser.add_argument("-p", "--part_copy", help = "choose some lines to copy.")
    parser.add_argument("-k", "--keywords_copy", help = "choose the keys words part to copy.")

    args = parser.parse_args()

#    # judge source and target are whether existed.
#    if not args.sourceFile or not args.targetDir:
#        print "-s xx and -t xx should be not empty"
#        sys.exit(1)
    
    # parse args and run.
    ct = CopyTool(args)
    if args.full_copy:
        ct.full_copy()
    elif args.part_copy:
        ct.part_copy()
    elif args.keywords_copy:
        ct.keywords_copy()
    else:
        print "miss action"
    sys.exit(0)
