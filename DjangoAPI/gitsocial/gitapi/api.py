from django.http import JsonResponse
from github import Github

g = Github('ebd026d4736c985826055cc7b1d8a5db1c6f26b3')

def contributor_to_dict(contributor):
    d = {}
    d['username'] = contributor.author.login
    d['name'] = contributor.author.name
    d['total'] = contributor.total
    last_week = contributor.weeks[0]
    d['last_week'] = { # TODO: Might be first week...
        
        'additions': last_week.a,
        'deletes' : last_week.d,
        'commits' : last_week.c,
        }
    return d

def get_lines_week(request, owner, repo, username):
    repo = g.get_repo(owner + '/' + repo)
    stats = repo.get_stats_contributors()
    json = {'success' : True}
    for contributor in stats:
        if contributor.author.login == username:
            data = contributor_to_dict(contributor)
            json['lines'] = data['last_week']['additions'] + data['last_week']['deletes']
            json['additions'] = data['last_week']['additions']
            json['deletes'] = data['last_week']['deletes']
            break
    else:
        json['success'] = False
        json['error']  = 'username not found'
            

    return JsonResponse(json, safe=False)

def get_commits_week(request, owner, repo, username):
    repo = g.get_repo(owner + '/' + repo)
    stats = repo.get_stats_contributors()
    json = {'success' : True}
    for contributor in stats:
        if contributor.author.login == username:
            json['commits'] = contributor_to_dict(contributor)['last_week']['commits']
            break
    else:
        json['success'] = False
        json['error']  = 'username not found'
            

    return JsonResponse(json, safe=False)

def get_leaderboard_commits_week(request, owner, repo):
    repo = g.get_repo(owner + '/' + repo)
    stats = repo.get_stats_contributors()
    json = {'success': True, 'contributors': []}
    for i, contributor in enumerate(stats): #Convert author objects to the username
        contributor_dict = contributor_to_dict(contributor)
        contributor_json = {}
        contributor_json['username'] = contributor_dict['username']
        contributor_json['name'] = contributor_dict['name']
        contributor_json['commits'] = contributor_dict['last_week']['commits']
        json['contributors'].append(contributor_json)

    json['contributors'].sort(key=lambda x: x['commits'], reverse=True)

    return JsonResponse(json, safe=False)