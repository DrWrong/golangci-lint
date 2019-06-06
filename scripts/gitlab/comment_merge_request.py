import gitlab

gl = gitlab.Gitlab('https://gitlab.p1staff.com', private_token="Exdyq6QekepCJMyQ1m9X")
# URL_PREFIX = 'https://gitlab.p1staff.com/api/v4'
# TOKEN = ""

def merge_request_discussion(project_id, merge_request_iid, report):
    '''
    Disccussion issues
    '''
    if len(report['Issues']) <= 0:
        print("Do Not have any issues")

    project = gl.projects.get(project_id)
    mr = project.mergerequests.get(merge_request_iid)
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
        print(data)
        resp = mr.discussions.create(data)
        print(resp)
