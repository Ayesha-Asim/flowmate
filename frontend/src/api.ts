export type Status = 'todo' | 'in_progress' | 'done';
export type Priority = 'low' | 'medium' | 'high';
export type Task = {id:string; title:string; description:string; status:Status; priority:Priority; due_date:string|null; depends_on:string[]};
export type Project = {project_id:string;title:string;summary:string;deadline:string|null;tasks:Task[];mode:string};
export type ReplanChange = {task_id:string;old_due_date:string|null;new_due_date:string|null;reason:string};
export type ReplanProposal = {proposal_id:string;project_id:string;summary:string;changes:ReplanChange[];mode:string};
const base=(import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/,'');
async function request<T>(path:string,options?:RequestInit):Promise<T>{
 const response=await fetch(base+path,{...options,headers:{'Content-Type':'application/json',...(options?.headers||{})}});
 if(!response.ok){let message=`Request failed (${response.status})`;try{const data=await response.json();message=typeof data.detail==='string'?data.detail:JSON.stringify(data.detail||data)}catch{}throw new Error(message)}
 return response.json();
}
export const api={
 health:()=>request<{status:string;mode:string}>('/health'),
 generate:(goal:string,deadline:string|null)=>request<Project>('/api/plans/generate',{method:'POST',body:JSON.stringify({goal,deadline})}),
 projects:()=>request<Project[]>('/api/projects'),
 project:(id:string)=>request<Project>(`/api/projects/${id}`),
 updateTask:(id:string,patch:Partial<Task>)=>request<Task>(`/api/tasks/${id}`,{method:'PATCH',body:JSON.stringify(patch)}),
 replan:(id:string,instruction:string)=>request<ReplanProposal>(`/api/projects/${id}/replan`,{method:'POST',body:JSON.stringify({instruction})}),
 applyReplan:(id:string,proposal_id:string)=>request<Project>(`/api/projects/${id}/apply-replan`,{method:'POST',body:JSON.stringify({proposal_id})})
};
