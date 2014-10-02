#! /usr/bin/env python2

import argparse
import os
import shlex
import subprocess

import option

def download(path_list, work_path):
    for path in path_list:
        save_path = os.path.join(work_path, os.path.basename(path))
        cmd ='curl -s %s -o %s' %(path, save_path)
        try:
            retcode = subprocess.call(shlex.split(cmd))
            if retcode != 0:
                print "Error download - %s" % path
                break
        except OSError as e:
            print 'Execution failed:', e

        print 'Download %s done.' %save_path


def upload(path_list):
    url_list = []
    for path in path_list:
        cmd = 'curl --upload-file %s https://transfer.sh/%s' %(path, os.path.basename(path))
        try:
            url = subprocess.check_output(shlex.split(cmd))
            url_list.append(url)
        except OSError as e:
            print 'Execution failed:', e

    if not url_list:
        return
    print 'Now you can download file(s) by the following url(s):'
    for url in url_list:
        print url,

def main():
    parser = argparse.ArgumentParser()
    option.add_options(parser)

    opts = option.Option()
    parser.parse_args(namespace=opts)

    if opts.upload_path:
        upload(opts.upload_path)

    if opts.download_path:
        download(opts.download_path, opts.work_path)

if __name__ == '__main__':
    main()
