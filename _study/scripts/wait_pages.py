"""Let the existing branch-based Pages deployment finish before replacing it."""
import os,json,time,urllib.request
repo=os.environ['GITHUB_REPOSITORY'];sha=os.environ['GITHUB_SHA']
url=f'https://api.github.com/repos/{repo}/actions/runs?head_sha={sha}&per_page=100'
for attempt in range(80):
 request=urllib.request.Request(url,headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json'})
 with urllib.request.urlopen(request,timeout=30) as response: runs=json.load(response)['workflow_runs']
 pages=[r for r in runs if r['path']=='dynamic/pages/pages-build-deployment']
 if pages and all(r['status']=='completed' for r in pages):
  if any(r['conclusion']!='success' for r in pages):raise SystemExit('Existing Pages build failed; keep its deployment unchanged.')
  print('Existing Pages deployment completed.');break
 time.sleep(10)
else: raise SystemExit('Timed out waiting for existing Pages deployment.')
