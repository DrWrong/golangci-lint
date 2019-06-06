#!/bin/env python3
import argparse
import json

from gitlab_comment import comment_merge_request
from comment_merge_request import merge_request_discussion

parser = argparse.ArgumentParser(description='Gitlab merge rquest notes')
parser.add_argument("--project_id", dest="project_id", help="project id")
parser.add_argument("--source_branch", dest="source_branch", help="source branch")
parser.add_argument("--file", dest="file", help="source branch")
parser.add_argument("--merger_request_iid", dest="merge_request_iid", help="merge request iid")


args = parser.parse_args()
print("project id", args.project_id)
print("source branch", args.source_branch)
print("merger request iid", args.merge_request_iid)

source_branch = args.source_branch.replace('remotes/origin/', '')

with open(args.file, encoding="utf-8") as f:
    data = json.load(f)

if args.merge_request_iid:
    merge_request_discussion(args.project_id, args.merge_request_iid, data)
    exit(0)

comment_merge_request(args.project_id, source_branch, data)
