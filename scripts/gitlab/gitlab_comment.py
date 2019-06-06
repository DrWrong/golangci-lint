import requests

from  generate_comment_body import generate_comment_body
URL_PREFIX = 'https://gitlab.p1staff.com/api/v4'
TOKEN = "Exdyq6QekepCJMyQ1m9X"


def get_merge_requests(project_id, source_branch):
    '''
    get merge requests that start with source branch
    '''
    r = requests.get(
        URL_PREFIX + "/projects/%s/merge_requests" % (project_id),
        headers={
            'Private-Token': TOKEN,
        },
        params={
            'source_branch': source_branch,
            'state': 'opened',
        }
    )
    return r.json()


def comment_merge_request(project_id, source_branch, report):
    '''
    Run comment on merge rquests
    '''
    if len(report['Issues']) <= 0:
        print("Do Not have any issues")
        return
    merge_requests = get_merge_requests(project_id, source_branch)
    if len(merge_requests) <= 0:
        print("Do not found merge request from %s" % (source_branch))
        return

    body = generate_comment_body(report)

    for merge_request in merge_requests:
        merge_request_iid = merge_request['iid']
        print("Going to patch note on merge request %s" %  merge_request_iid)
        r = requests.post(
            URL_PREFIX + '/projects/%s/merge_requests/%d/notes' % (project_id, merge_request_iid),
            headers={
                'Private-Token': TOKEN,
            },
            data={
                'body': body,
            }

        )
        print("Add notes result:", r.status_code)
