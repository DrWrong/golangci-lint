import gitlab

gl = gitlab.Gitlab('https://gitlab.p1staff.com', private_token="Exdyq6QekepCJMyQ1m9X")
# URL_PREFIX = 'https://gitlab.p1staff.com/api/v4'
# TOKEN = ""

def process_issuses(mr, report):
    diff = mr.diffs.list()[0]
    for issue in report['Issues']:
        data = {
            'position': {
                'base_sha': diff.base_commit_sha,
                'start_sha': diff.start_commit_sha,
                'head_sha': diff.head_commit_sha,
                'position_type': 'text',
                'new_path': issue['Pos']['Filename'],
                'new_line': issue['Pos']['Line'],
            },
            'body': issue['Text'],
        }
        resp = mr.discussions.create(data)
        print(resp)


def merge_request_discussion(project_id, merge_request_iid, report):
    '''
    Disccussion issues
    '''
    if len(report['Issues']) <= 0:
        print("Do Not have any issues")
        return

    project = gl.projects.get(project_id)
    mr = project.mergerequests.get(merge_request_iid)
    process_issuses(mr, report)

def discussion_when_merge_requests(project_id, source_branch, report):
    if len(report['Issues']) <= 0:
        print("Do Not have any issues")
        return
    project = gl.projects.get(project_id)
    mrs = project.mergerequests.list(
        state= 'opened',
        source_branch= source_branch,
    )

    for mr in mrs:
        print(mr)
        process_issuses(mr, report)
