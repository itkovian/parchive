#!/usr/bin/env python
# -*- coding: latin-1 -*-
##
# Copyright 2019-2019 Ghent University
#
# This file is part of parchive.
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://www.vscentrum.be),
# the Flemish Research Foundation (FWO) (http://www.fwo.be/en)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# All rights reserved.
#
##
"""
Script to archive Slurm jobscripts and job environments.

@author: Andy Georges (Ghent University)
"""
import argparse
import multiprocessing
import inotify.adapters
import os
import time
import shutil
import sys

from inotify.constants import IN_CREATE
from collections import namedtuple

from time import sleep

JobInfo = namedtuple("JobInfo", ["path", "current"])

def worker(path, queue, i):

    print("worker %d watching %s" % (i, path))
    ntfy = inotify.adapters.Inotify()
    ntfy.add_watch(path, mask=IN_CREATE)

    while True:
        #print("worker %d" % i)
        for event in ntfy.event_gen(yield_nones=False, timeout_s=1):
            print("worker %d got an event: %s" % (i, event))
            try:
                (_, type_names, path, filename) = event
                if 'IN_ISDIR' in type_names and filename.startswith('job.'):
                    queue.put(JobInfo(path="%s/%s" % (path, filename), current=time.time()))
                    print("Event queued")
            except Exception as e:
                print("Caught exception %s" % e)

    print("worker %d done" % i)


def processor(queue, archive):

    print("I am a processor")
    while True:
        j = queue.get(True)


        try:
            print("got item")
            now = time.time()
            if now - j.current < 2:
                time.sleep(2)
        except Exception as e:
            print("Oops, processing error: %s", e)

        script_path = os.path.join(j.path, "script")
        environment_path = os.path.join(j.path, "environment")
        job_name = os.path.basename(j.path)

        for (f, s) in [(script_path, "script"), (environment_path, "environment")]:
            print("looking for %s" % f)
            if os.path.exists(f):
                print("file found at %s" % f)
                shutil.copyfile(f, os.path.join(archive, "%s_%s" % (job_name, s)))



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Slurm job script archival tool", prog="parchive")
    parser.add_argument("-a", "--archive", help="Location of the job scripts' archive.")
    parser.add_argument("-s", "--spool", help="Location of the Slurm StateSaveLocation (where the job hash dirs are kept).")
    parser.add_argument("-p", "--period", help="Archive under a YYYY subdirectory (yearly), YYYYMM (monthly), or YYYYMMDD (daily).")
    parser.add_argument("-l", "--logfile", help="Log file name.")

    args = parser.parse_args()

    pool = multiprocessing.Pool(processes=12)
    print("pool created")
    m = multiprocessing.Manager()
    q = m.Queue()
    p = pool.apply_async(processor, (q, "/tmp/archive"))
    print("processor created")
    workers = [pool.apply_async(worker, ("/tmp/slurm/hash.%d" % i, q, i)) for i in range(0,10)]
    print("workers created: %s" % workers)

    p.get()