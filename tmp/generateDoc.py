# -*- coding: utf-8 -*-
import sys, time
sys.path.append('/var/python/libs/')
sys.path.append('/var/python/')
sys.path.append('/home/python/libs/')
sys.path.append('/home/python/')

from functionsex import *
import docit

SCREENDESK_API_WRAPPING_ENABLED=False  # disabling wrapping becouse it hides args
from screendesk import api as screendeskApi

def generateLib(api, buildPath, outputPath):
   ignoreClasses=['ApiAuth']
   files={}
   mainTemplate=fileGet(buildPath+'libs/template/api_main.js')
   classTemplate=fileGet(buildPath+'libs/template/api_class.js')
   methodTemplate=fileGet(buildPath+'libs/template/api_method.js')
   methodInfoParamTemplate=fileGet(buildPath+'libs/template/api_method_info_param.txt')
   data=[]
   for ck in api.tree.classesOrder:
      if ck in ignoreClasses: continue
      c=api.tree.classes[ck]
      cReal=getattr(screendeskApi, c._name)
      className=screendeskApi.convPathForFlatMap(cReal)
      if className.endswith('.'): className=className[:-1]
      if className.startswith('.'): className=className[1:]
      tArr1={'className':className}
      data.append(classTemplate%tArr1)
      #
      for mk in c.tree.methods.publicOrder:
         m=c.tree.methods.public[mk]
         _infoParams=[]
         _params=[]
         m.directive={o['type']:o['data'] for o in m.directive}
         if m.params:
            _infoParams.append('')  #this allows to skip empty param's section in output
            _nameLongest=max(len(o['name']) for o in m.params)
            _typeLongest=max(len(o['type']) for o in m.params)
            for o in m.params:
               oo={
                  'typeSpacing':' '*(_typeLongest-len(o['type'])),
                  'nameSpacing':' '*(_nameLongest-len(o['name'])),
               }
               oo.update(o)
               oo['type']=oo['type'].lower()
               _params.append(oo['name'])
               _infoParams.append((methodInfoParamTemplate%oo).rstrip())
         #
         argsOrder=[k for k in m.argsRaw.order if k not in ('self', 'cls', '_conn')]
         argsDef={k:v for k,v in m.argsRaw.defValue.iteritems() if k not in ('self', 'cls', '_conn')}
         for k in argsDef:
            if argsDef[k] is NULL: argsDef[k]=None
         argsDef=json.dumps(argsDef)
         argsMap={k:i for i,k in enumerate(argsOrder)}
         tArr1.update({
            'methodName':m.name,
            'methodDescr':m.descr,
            'methodInfoParams':'\n'.join(_infoParams),
            'methodInfoReturns':'',
            'methodParams':', '.join(_params),
            'methodParamsDef':argsDef,
            'methodParamsOrder':argsOrder,
            'methodParamsMap':argsMap,
         })
         #
         tArr2=[o.data for o in m.example if o._isFakeResponse]
         for i in xrange(1, 6):
            if i-1<len(tArr2):
               s=tArr2[i-1].replace('\n', '\n      ').replace(' \n', '\n')
            else: s='""'
            tArr1['methodResponseExample%s'%i]=s
         #
         s=m.directive.get('genLib_replace', methodTemplate)
         data.append(s%tArr1+'\n')
      data.append('')
   data='\n'.join(data)
   data=mainTemplate%{'api':data}
   files['api']=data
   for n, d in files.iteritems():
      p=outputPath+'libs/'+n+'.js'
      fileWrite(p, d)
      files[n]=p
   return files

def prepMethodForDocs(o):
   o.data=o.data.replace('(self', '(')
   o.data=o.data.replace(', _conn=None', '')
   o.data=o.data.replace('(, ', '(')
   #
   tArr, o.example=o.example, []
   for oo in tArr:
      if oo.type=='fake_response_hide':
         oo._isFakeResponse=True
         continue
      elif oo.type in ('json', 'badjson', 'fake_response'):
         try:
            s=json.loads(oo.code) if oo.type=='json' else eval(oo.code)
            s=json.dumps(s, indent=3)
            oo.code=s
         except Exception: pass
         oo._isFakeResponse=(oo.type=='fake_response')
         oo.type='json'
      o.example.append(oo)

def main():
   buildPath='/home/python/justAnotherLiveChat/build/'
   outputPath='/home/python/justAnotherLiveChat/dist/'
   docitPath=getScriptPath(f=docit.__file__)+'/'
   ignoreClasses=['ApiBase', 'ApiWrapper']
   ignoreFuncsType=['private', 'public', 'special', 'undoc']

   api=docit.pydoc2api(screendeskApi).summary(moduleWhitelist=['self'])  #['self', 'self.']
   # sort like in sources
   #! этот код нужно перенести в docit дополнив поддержку
   # https://julien.danjou.info/blog/2015/python-ast-checking-method-declaration
   import ast
   api._ast=ast.parse(fileGet(api.file))
   tArr1={}
   for oo in ast.walk(api._ast):
      if not isinstance(oo, ast.ClassDef): continue
      if oo.name not in api.tree.classes: continue
      tArr1[oo.name]=oo.lineno
      tArr2={}
      for oo2 in oo.body:
         if not isinstance(oo2, ast.FunctionDef): continue
         if oo2.name not in api.tree.classes[oo.name].tree.methods.public: continue
         tArr2[oo2.name]=oo2.lineno
      api.tree.classes[oo.name].tree.methods.publicOrder.sort(key=lambda k: tArr2[k])
   api.tree.classesOrder.sort(key=lambda k: tArr1[k])
   # prepare api
   for k in ignoreClasses:
      del api.tree.classes[k]
      api.tree.classesOrder.remove(k)
   for k in ignoreFuncsType:
      api.tree.methods[k]={}
      api.tree.methods[k+'Order']=[]
   #
   for c in api.tree.classes.itervalues():
      c.data, c._data=c._obj.path, c.data
      c.name, c._name=c._obj.path, c.name
      c['return'], c._return='', c['return']
      #
      c.tree.methods.special={}
      c.tree.methods.specialOrder=[]
      c.tree.methods.private={}
      c.tree.methods.privateOrder=[]
      #
      for m in c.tree.methods.public.itervalues(): prepMethodForDocs(m)
   fileWrite(outputPath+'docs/api.json', reprEx(api, indent=3, sortKeys=True))
   files=docit.api2html(api, outputPath+'docs/pages', buildPath+'docs/template/simpleBootstrapWithToc.html', hLevel=1)
   files.update(generateLib(api, buildPath, outputPath))
   print 'Done!'
   for name, path in files.items():
      print '>>', path

if __name__=='__main__':
   main()
