#!/usr/bin/env python    
# -*- coding: utf-8 -*- 
import tarfile
import time
import argparse
import os
import sys

FUNC = lambda x,y : x or y

class tarTool(object):
    def  __init__(self, args):
        self.source = FUNC(args.tar_file, args.untar_file)
        print args,self.source
        self.filename = os.path.basename(self.source)
        self.target_dir = args.target_dir
        self.time = time.strftime('%Y%m%d-%H%M%S',time.localtime(time.time()))

    def tar_file(self):
		tarFile = tarfile.TarFile(self.target_dir + self.filename.split(".")[0] + self.time + ".tar.gz", "w")
		for root, cur_dir, files in os.walk(self.source):
			for f in files:
				fullpath = os.path.join(root, f)
				tarFile.add(fullpath)
		tarFile.close()
    
    def untar_file(self):
		unTarFile = tarfile.open(self.source)
        #unTarFile.extractall()
		names = unTarFile.getnames()
		for name in names:
			unTarFile.extract(name, path=self.target_dir)
		unTarFile.close()

if __name__ == '__main__':
    """
    copy tools for three means of copying file.
    """

    #input argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--tar_file", help = "the source file that the coper is from.")
    #parser.add_argument("-d", "--tar_dir", help = "the target file that the coper goes to.")
    parser.add_argument("-u", "--untar_file", help = "copy source file fully to target file.")
    parser.add_argument("-t", "--target_dir", help = "choose some lines to copy.")
    #parser.add_argument("-k", "--keywords_copy", help = "choose the keys words part to copy.")

    args = parser.parse_args()
    print args
#    # judge source and target are whether existed.
#    if not args.sourceFile or not args.targetDir:
#        print "-s xx and -t xx should be not empty"
#        sys.exit(1)
    
    # parse args and run.
    tt = tarTool(args)
    if args.tar_file:
        tt.tar_file()
    elif args.untar_file:
        tt.untar_file()
    else:
        print "miss action"
    sys.exit(0)

