from __future__ import annotations
import hashlib,json,re
from collections import defaultdict,deque
from typing import Any,Mapping
def stable(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def digest(v): return hashlib.sha256(stable(v).encode()).hexdigest()
class BusinessError(ValueError): pass

from referral_robot.persistence.run_store import process_fixture
def run(raw,database):
 p=raw.get('payload',raw); actions=[dict(x) for x in p.get('actions',[])]; context=dict(p.get('context',{})); cursor=int(p.get('cursor',0)); trace=[]; waiting=None
 for i,action in enumerate(actions[cursor:],cursor):
  kind=action.get('kind')
  if action.get('requires_approval') and not action.get('approved'): waiting={'index':i,'reason':'human approval required','action':action}; break
  if kind=='set': context[str(action['field'])]=action.get('value')
  elif kind=='copy': context[str(action['target'])]=context.get(str(action['source']))
  elif kind=='assert' and context.get(str(action['field']))!=action.get('value'): raise BusinessError('page contract assertion failed')
  elif kind=='receipt': context['receipt']=digest(action)[:16]
  elif kind not in {'assert'}: raise BusinessError(f'unsupported action {kind}')
  cursor=i+1; trace.append({'index':i,'kind':kind,'context_hash':digest(context)})
 result={'cursor':cursor,'context':context,'trace':trace,'waiting':waiting,'complete':cursor==len(actions),'checkpoint':digest([cursor,context])}
 stored=process_fixture(database,{'subject_id':str(p.get('referral_id','referral-demo')),'request_key':str(p.get('run_key','run-demo')),'payload':result})
 return {'automation':result,'stored':stored}
