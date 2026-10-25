"""FlowMate starter API. Demo mode uses deterministic examples, not AI."""
import json
import os
import re
import sqlite3
import uuid
from datetime import date, timedelta
from pathlib import Path
from typing import Literal

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

load_dotenv()
AI_MODE = os.getenv('AI_MODE', 'mock').lower()
DB_PATH = os.getenv('DATABASE_PATH', str(Path(__file__).with_name('flowmate.sqlite3')))
app = FastAPI(title='FlowMate API', version='0.1.0')
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')], allow_credentials=False, allow_methods=['GET','POST','PATCH'], allow_headers=['Content-Type'])

class GenerateRequest(BaseModel):
    goal: str = Field(min_length=10, max_length=2000)
    deadline: date | None = None

class TaskPatch(BaseModel):
    status: Literal['todo','in_progress','done'] | None = None
    title: str | None = Field(default=None, min_length=1, max_length=180)
    description: str | None = Field(default=None, max_length=2000)
    priority: Literal['low','medium','high'] | None = None
    due_date: date | None = None

class ReplanRequest(BaseModel):
    instruction: str = Field(min_length=3, max_length=1000)

class ApplyRequest(BaseModel):
    proposal_id: str


def connect():
    conn=sqlite3.connect(DB_PATH)
    conn.row_factory=sqlite3.Row
    return conn

def init_db():
    with connect() as c:
        c.execute('CREATE TABLE IF NOT EXISTS projects (id TEXT PRIMARY KEY, payload TEXT NOT NULL)')
        c.execute('CREATE TABLE IF NOT EXISTS proposals (id TEXT PRIMARY KEY, project_id TEXT NOT NULL, payload TEXT NOT NULL)')
init_db()

def save_project(p):
    with connect() as c:
        c.execute('INSERT OR REPLACE INTO projects(id,payload) VALUES (?,?)',(p['project_id'],json.dumps(p)))

def get_project(project_id):
    with connect() as c:
        row=c.execute('SELECT payload FROM projects WHERE id=?',(project_id,)).fetchone()
    if not row: raise HTTPException(404,'Project not found')
    return json.loads(row['payload'])

def validate_plan(raw):
    if not isinstance(raw,dict) or not isinstance(raw.get('tasks'),list) or not raw['tasks']:
        raise ValueError('Model did not return a valid nonempty tasks list')
    tasks=[]
    for i,item in enumerate(raw['tasks'][:12]):
        if not isinstance(item,dict) or not str(item.get('title','')).strip():raise ValueError('Invalid task title')
        due=item.get('due_date')
        if due: date.fromisoformat(str(due))
        tasks.append({'id':f'task-{uuid.uuid4().hex[:12]}','title':str(item['title'])[:180],'description':str(item.get('description',''))[:2000], 'status':'todo','priority':item.get('priority') if item.get('priority') in ('low','medium','high') else 'medium','due_date':str(due) if due else None,'depends_on':[]})
    return {'title':str(raw.get('title','New project'))[:120],'summary':str(raw.get('summary',''))[:500],'tasks':tasks}

def mock_plan(goal,deadline):
    end=deadline or date.today()+timedelta(days=14)
    titles=[('Define success criteria','Write down what a successful result looks like.','high',10),('Confirm resources','Identify people, tools and budget needed.','high',8),('Prepare materials','Create the documents and materials required.','medium',5),('Review progress','Check blockers and adjust task priorities.','medium',3),('Deliver and evaluate','Complete the goal and review the outcome.','high',0)]
    return {'title':goal[:70].rstrip('.'),'summary':f'Demo plan for: {goal}','tasks':[{'title':t,'description':d,'priority':p,'due_date':(end-timedelta(days=offset)).isoformat()} for t,d,p,offset in titles]}

async def call_model(messages):
    key=os.getenv('NEBIUS_API_KEY','')
    base=os.getenv('NEBIUS_BASE_URL','').rstrip('/')
    model=os.getenv('NEBIUS_MODEL','')
    if not key or not base or not model:
        raise HTTPException(503,'Live mode needs NEBIUS_API_KEY, NEBIUS_BASE_URL and NEBIUS_MODEL in backend/.env')
    # Set NEBIUS_BASE_URL to the provider-documented OpenAI-compatible /v1 base URL.
    # Confirm your account's actual endpoint and NVIDIA open model ID in Nebius documentation.
    try:
        async with httpx.AsyncClient(timeout=70) as client:
            response=await client.post(f'{base}/chat/completions',headers={'Authorization':f'Bearer {key}'},json={'model':model,'messages':messages,'temperature':0.2,'response_format':{'type':'json_object'}})
            response.raise_for_status()
            result=response.json()['choices'][0]['message']['content']
            return json.loads(result)
    except (httpx.HTTPError,KeyError,IndexError,ValueError) as exc:
        raise HTTPException(502,f'Model request failed: {str(exc)[:240]}') from exc

@app.get('/health')
def health(): return {'status':'ok','mode':AI_MODE}

@app.post('/api/plans/generate')
async def generate(req:GenerateRequest):
    if AI_MODE=='mock': raw=mock_plan(req.goal,req.deadline)
    elif AI_MODE=='live':
        raw=await call_model([{'role':'system','content':'You are a project planning assistant. Return ONLY a JSON object with title, summary, tasks. Each task must have title, description, priority (low/medium/high), due_date (YYYY-MM-DD or null). Generate 5-10 realistic tasks, no external actions.'},{'role':'user','content':f'Goal: {req.goal}. Deadline: {req.deadline}. Today: {date.today().isoformat()}'}])
    else: raise HTTPException(500,'AI_MODE must be mock or live')
    try: validated=validate_plan(raw)
    except (ValueError,TypeError) as exc: raise HTTPException(502,f'Invalid plan returned: {exc}') from exc
    project={'project_id':str(uuid.uuid4()),**validated,'deadline':req.deadline.isoformat() if req.deadline else None,'mode':AI_MODE}
    save_project(project)
    return project

@app.get('/api/projects')
def projects():
    with connect() as c: rows=c.execute('SELECT payload FROM projects ORDER BY rowid DESC LIMIT 50').fetchall()
    return [json.loads(r['payload']) for r in rows]

@app.get('/api/projects/{project_id}')
def project(project_id:str): return get_project(project_id)

@app.patch('/api/tasks/{task_id}')
def update_task(task_id:str,patch:TaskPatch):
    with connect() as c: rows=c.execute('SELECT payload FROM projects').fetchall()
    for row in rows:
        p=json.loads(row['payload'])
        for task in p['tasks']:
            if task['id']==task_id:
                values=patch.model_dump(exclude_unset=True)
                if 'due_date' in values and values['due_date'] is not None:values['due_date']=values['due_date'].isoformat()
                task.update(values);save_project(p);return task
    raise HTTPException(404,'Task not found')

@app.post('/api/projects/{project_id}/replan')
async def replan(project_id:str,req:ReplanRequest):
    p=get_project(project_id)
    if AI_MODE=='mock':
        # Demo behavior: shift existing due dates earlier by five days; never pretend it is AI.
        shift=5
        match=re.search(r'(\d+)\s*days?',req.instruction.lower())
        if match:shift=min(int(match.group(1)),30)
        if 'later' in req.instruction.lower():shift=-shift
        changes=[{'task_id':t['id'],'old_due_date':t['due_date'],'new_due_date':(date.fromisoformat(t['due_date'])-timedelta(days=shift)).isoformat(),'reason':'Demo schedule adjustment'} for t in p['tasks'] if t['due_date']]
        summary='Demo proposal: adjust existing task dates. No AI call was made.'
    else:
        raw=await call_model([{'role':'system','content':'You are a project re-planning assistant. Return ONLY JSON with summary and changes array. Each change: task_id (must match existing task), new_due_date (YYYY-MM-DD or null), reason. Only suggest changes; never perform actions.'},{'role':'user','content':f'Project: {json.dumps(p)}. Requested change: {req.instruction}'}])
        if not isinstance(raw.get('changes'),list):raise HTTPException(502,'Invalid model proposal')
        task_map={t['id']:t for t in p['tasks']};changes=[]
        for c in raw['changes']:
            tid=c.get('task_id');new=c.get('new_due_date')
            if tid not in task_map:raise HTTPException(502,'Model proposed unknown task')
            if new:
                try:date.fromisoformat(str(new))
                except ValueError:raise HTTPException(502,'Model proposed invalid date')
            changes.append({'task_id':tid,'old_due_date':task_map[tid]['due_date'],'new_due_date':new,'reason':str(c.get('reason',''))[:300]})
        summary=str(raw.get('summary','Suggested changes'))[:500]
    proposal={'proposal_id':str(uuid.uuid4()),'project_id':project_id,'summary':summary,'changes':changes,'mode':AI_MODE}
    with connect() as c:c.execute('INSERT INTO proposals(id,project_id,payload) VALUES (?,?,?)',(proposal['proposal_id'],project_id,json.dumps(proposal)))
    return proposal

@app.post('/api/projects/{project_id}/apply-replan')
def apply_replan(project_id:str,req:ApplyRequest):
    p=get_project(project_id)
    with connect() as c:row=c.execute('SELECT payload FROM proposals WHERE id=? AND project_id=?',(req.proposal_id,project_id)).fetchone()
    if not row:raise HTTPException(404,'Proposal not found or already applied')
    proposal=json.loads(row['payload']);task_map={t['id']:t for t in p['tasks']}
    for change in proposal['changes']:
        task=task_map.get(change['task_id'])
        if not task or task['due_date']!=change['old_due_date']:raise HTTPException(409,'Project changed since proposal; create a new proposal')
    for change in proposal['changes']:task_map[change['task_id']]['due_date']=change['new_due_date']
    with connect() as c:
        c.execute('UPDATE projects SET payload=? WHERE id=?',(json.dumps(p),project_id))
        c.execute('DELETE FROM proposals WHERE id=?',(req.proposal_id,))
    return p
