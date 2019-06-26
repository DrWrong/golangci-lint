import gitlab

gl = gitlab.Gitlab('https://gitlab.p1staff.com', private_token="Exdyq6QekepCJMyQ1m9X")
# URL_PREFIX = 'https://gitlab.p1staff.com/api/v4'
# TOKEN = ""

def process_issuses(mr, report):
    diff = mr.diffs.list()[0]
    disccustions = {}
    for discussion in mr.discussions.list():
        for note in discussion.attributes['notes']:
            if 'position'in note:
                key = (note['position']['new_path'], note['position']['new_line'])
                disccustions[key] = discussion

    for issue in report['Issues']:
        key = (issue['Pos']['Filename'], issue['Pos']['Line'])
        body = "%s:%s" % (issue['FromLinter'], issue['Text'])
        if key not in disccustions:
            data = {
                'position': {
                    'base_sha': diff.base_commit_sha,
                    'start_sha': diff.start_commit_sha,
                    'head_sha': diff.head_commit_sha,
                    'position_type': 'text',
                    'new_path': issue['Pos']['Filename'],
                    'new_line': issue['Pos']['Line'],
                },
                'body': body,
            }
            print(data)
            resp = mr.discussions.create(data)
            print(resp)
        else:
            discussion = disccustions[key]
            found_body =  False
            for note in discussion.attributes['notes']:
                if note['body'] == body:
                    found_body = True
                    break
            if not found_body:
                discussion.notes.create({'body': body})
            else:
                print("Ignore duplicate")




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
