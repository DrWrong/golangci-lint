#!/usr/bin/env python3
from bottle import request, app, Bottle
import multiprocessing



PROJECT_TOKEN = {
    176: '1eb80e308b80e7b8927866e0712410',
    195: '016a134e4ca30c67d76c2cb7af5c05',
    629: '0025a83ff56ead3854b1e3b7e434c7',
}

app = Bottle()

@app.route("/", 'POST')
def webhook():
    print("going to process merge request", request, request.remote_addr)

    if request.get_header('X-Gitlab-Event') != 'Merge Request Hook':
        return "Not merge request"
    object_attributes = request.json['object_attributes']

    if object_attributes['state'] != 'opened':
        return "Not opened"
    print("going to trigger pipeline")
    import requests

    project_id = request.json['project']['id']
    param = {
        'variables[CI_MERGE_REQUEST_TARGET_BRANCH_NAME]': object_attributes['target_branch'],
        'variables[CI_MERGE_REQUEST_IID]': object_attributes['iid'],
        'variables[CI_TRIGGER]': 'mergeRequestWebhook',
        'ref': object_attributes['source_branch'],
        'token': PROJECT_TOKEN[project_id]
    }
    print("going to merge", param)
    resp = requests.post("https://gitlab.p1staff.com/api/v4/projects/%d/trigger/pipeline" % project_id, data = param)
    print(resp.text)


if __name__ == '__main__':
    print("going to start webhook server")
    app.run(server="gunicorn", host="0.0.0.0", port=8543,
            workers=multiprocessing.cpu_count() * 2 + 1,
            worker_class = 'gevent'
    )
