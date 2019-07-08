# -*- coding: utf-8 -*-
import sys, os, cgi, urllib
from utils import *

from pydoc2api import *
try:
   from commonmark import commonmark as _markdown
except ImportError:
   print 'WARNING: No module `commonmark`, markdown support disabled'
   def _markdown(data, *args, **kwargs):
      return data

class TOC:
   def __init__(self, root=None, collapsed=False):
      self.root=root or ''
      self.data=[]
      self.collapsed=collapsed

   def add(self, s, collapsed=False):
      if(isString(s) or isNum(s)): s=TOC(s, collapsed=collapsed)
      self.data.append(s)
      return s

   def toHtml(self, active='', listType='ul', listClass='', itemClass='', listClassOnlyRoot='', root=True):
      tmpl_list='<%(listType)s class="%(listClass)s"> %(content)s </%(listType)s>'
      tmpl_item='<li class="%(itemClass)s"> %(content)s </li> '
      resTree=''
      for s in self.data:
         resTree+=s.toHtml(active=active, listType=listType, listClass=listClass, itemClass=itemClass, root=False)
      if resTree:
         s=' collapsed' if self.collapsed else ''
         resTree=tmpl_list%{'listType':listType, 'listClass':listClass+s, 'content':resTree}
      res=tmpl_item%{'itemClass':itemClass+(' active' if self.root==active else ''), 'content':self.root+resTree}
      if root:
         res=tmpl_list%{'listType':listType, 'listClass':listClass+' '+listClassOnlyRoot, 'content':res}
      return res

def objEscape(o):
   if isArray(o):
      for k, v in enumerate(o):
         if isString(v): o[k]=cgi.escape(v)
         elif isArray(v): o[k]=objEscape(v)
         elif isDict(v): o[k]=objEscape(v)
   elif isDict(o):
      for k, v in o.items():
         if isString(v): o[k]=cgi.escape(v)
         elif isArray(v): o[k]=objEscape(v)
         elif isDict(v): o[k]=objEscape(v)
   return o

def typeBeauty(data):
   data=data.replace(',', '|')
   data=' | '.join(s.strip() for s in data.split('|') if s.strip())
   return data

def markdown2html(data):
   return encode_utf8(_markdown(decode_utf8(data)))

def params2html(o):
   res=''
   for o2 in o:
      o2.type=typeBeauty(o2.type)
      o2.descr=markdown2html(o2.descr)
      res+='<tr> <td><strong>%(name)s</strong></td> <td><code>%(type)s</code></td> <td><samp>%(descr)s</samp></td> </tr>'%o2
   if res:
      res='<table class="table table-condensed table-hover table-striped"><tbody> %s </tbody></table>'%res
   return res

def obj2html(o, type, toc, prefix='', hLevel=4):
   type2color={
      'class':'warning',
      'method_public':'primary',
      'method_private':'primary',
      'method_special':'primary',
      'method_undoc':'default',
      'function_private':'success',
      'function_public':'success',
      'function_special':'success',
      'function_undoc':'default',
   }
   o['type2']=type
   o['prefix']=prefix
   o['navName']=((prefix+'_') if prefix else '')+o.name
   o['navName']=sha256(o['navName'])
   o['color']=type2color.get(type, 'default')
   o['h1']='h'+str(hLevel)
   o['h2']='h'+str(hLevel+1)
   o['h3']='h'+str(hLevel+2)
   o['h4']='h'+str(hLevel+3)
   tocCurrent=toc.add('<a href="#%(navName)s" class="btn btn-default btn-xs">%(name)s</a>'%o)
   res=''
   # section
   res+='<div class="callout callout-%(color)s"> <%(h1)s id="%(navName)s"> <span class="label label-%(color)s">%(type2)s</span> <code class="language-python">%(data)s</code> <a class="headerlink text-%(color)s" href="#%(navName)s" title="Permalink to %(name)s">¶</a> </%(h1)s>'%o
   # description
   if o.descr:
      o.descr=markdown2html(o.descr)
      res+='<%(h2)s id="%(navName)s___descr" class="text-muted">Description <a class="headerlink text-muted" href="#%(navName)s___descr" title="Permalink to %(name)s\' description">¶</a> </%(h2)s>'%o
      res+='<pre>%(descr)s</pre>'%o
   # attention
   if o.attention:
      for s in o.attention:
         s['data']=markdown2html(s['data'])
      res+='<%(h2)s id="%(navName)s___example" class="text-danger"><span>Attention</span> <a class="headerlink text-danger" href="#%(navName)s___attention" title="Permalink to %(name)s\' attention">¶</a> </%(h2)s>'%o
      res+='\n<hr>'.join(['<b><i>%(title)s</i></b><pre class="bg-danger">%(data)s</pre>'%s for s in o.attention])
   if o.note:
      for s in o.note:
         s['data']=markdown2html(s['data'])
      res+='<%(h2)s id="%(navName)s___note" class="text-muted"><span>Note</span> <a class="headerlink text-muted" href="#%(navName)s___attention" title="Permalink to %(name)s\' note">¶</a> </%(h2)s>'%o
      res+='\n<hr>'.join(['<b><i>%(title)s</i></b><pre class="bg-info">%(data)s</pre>'%s for s in o.note])
   # parametrs
   s=params2html(o.params)
   if s:
      res+=('<%(h2)s id="%(navName)s___params" class="text-muted">Parametrs <a class="headerlink text-muted" href="#%(navName)s___params" title="Permalink to %(name)s\' parametrs">¶</a> </%(h2)s>'%o)+s
   # returned value
   if o['return']:
      o['return'].descr=markdown2html(o['return'].descr)
      o['return'].type=typeBeauty(o['return'].type)
      res+='<%(h2)s id="%(navName)s___return" class="text-muted">Return <a class="headerlink text-muted" href="#%(navName)s___return" title="Permalink to %(name)s\' returned value">¶</a> </%(h2)s>'%o
      res+='<code>%(type)s</code> <samp>%(descr)s</samp>'%o['return']
   # example
   if o.example:
      res+='<%(h2)s id="%(navName)s___example" class="text-muted">Example <a class="headerlink text-muted" href="#%(navName)s___example" title="Permalink to %(name)s\' example">¶</a> </%(h2)s>'%o
      res+='\n<hr>'.join(['<b><i>%(title)s</i></b><pre><code class="language-%(type)s">%(data)s</code></pre>'%s for s in o.example])
   if o.tree:
      # methods
      fSetts=dict2magic([
         {'type':'public', 'prefix':'public', 'prefix2':'Public', 'color':'primary', 'collapse':False},
         {'type':'private', 'prefix':'private', 'prefix2':'Private', 'color':'primary', 'collapse':True},
         {'type':'special', 'prefix':'special', 'prefix2':'Special', 'color':'primary', 'collapse':True},
         {'type':'undoc', 'prefix':'undoc', 'prefix2':'Un-documented', 'color':'default', 'collapse':True}
      ], True)
      for fSett in fSetts:
         resTree=''
         tocTree=TOC(('<a href="#'+fSett.prefix+'MethodsSection_%(navName)s" class="btn btn-default btn-xs">'+fSett.prefix2+' methods</a>')%o, collapsed=fSett.collapse)
         for k2 in o.tree.methods[fSett.prefix+'Order']:
            if k2 not in o.tree.methods[fSett.prefix]:
               print '! Method %s missed in tree'%k2
               continue
            o2=o.tree.methods[fSett.prefix][k2]
            resTree+=obj2html(o2, 'method_'+fSett.prefix, tocTree, prefix=o.navName+'_m'+fSett.prefix)
         if resTree:
            tocCurrent.add(tocTree)
            res+=(('<section style="margin-top: 20px;" id="'+fSett.prefix+'MethodsSection_%(navName)s"> <button class="btn btn-'+fSett.color+'" type="button" data-toggle="collapse" data-target="#'+fSett.prefix+'Methods_%(navName)s"> '+fSett.prefix2+' methods of %(type2)s %(name)s</button> <div class="collapse '+('' if fSett.collapse else 'in')+'" id="'+fSett.prefix+'Methods_%(navName)s">')%o)+resTree+'</div> </section>'
   res+='</div>'
   return res

def module2html(o, toc, template, prefix='', hLevel=1, root=False):
   o['prefix']=prefix
   o['navName']=((prefix+'_') if prefix else '')+'module_'+o.name.replace('.', '__')
   o['h1']='h'+str(hLevel)
   o['h2']='h'+str(hLevel+1)
   o['h3']='h'+str(hLevel+2)
   o['h4']='h'+str(hLevel+3)
   if not o.version: o['versionFull']=''
   else:
      o['versionFull']='%(version)s'%o
      if o.ver_sub: o['versionFull']+='.%(ver_sub)s'%o
      o['versionFull']='<small><span class="label label-default"> %(versionFull)s </span></small>'%o
   active='<a href="%(navName)s.html" class="btn btn-default btn-xs">%(name)s</a>'%o
   if root:
      tocTreeM=toc
      toc.root=active
   else:
      tocTreeM=toc.add(active)
   resMap={}
   tocCurrent=TOC('<a href="#%(navName)s" class="btn btn-default btn-xs"> Module %(data)s</a>'%o)
   res=''
   res+='<%(h1)s id="%(navName)s"> <span class="label label-danger">module</span> %(data)s %(versionFull)s </%(h1)s>'%o
   # description
   if o.descr:
      res+='<%(h2)s id="%(navName)s___descr" class="text-muted">Description <a class="headerlink text-muted" href="#%(navName)s___descr" title="Permalink to %(name)s\' description">¶</a> </%(h2)s>'%o
      res+='<pre><code>%(descr)s</code></pre>'%o
   # example
   if o.example:
      res+='<%(h2)s id="%(navName)s___example" class="text-muted">Example <a class="headerlink text-muted" href="#%(navName)s___example" title="Permalink to %(name)s\' example">¶</a> </%(h2)s>'%o
      res+='\n'.join(['<pre><code class="language-python">%s</code></pre>'%s for s in o.example])
   # classes
   tocTree=TOC('<a href="#classesSection_%(navName)s" class="btn btn-default btn-xs">Classes</a>'%o)
   resTree=''
   for k2 in o.tree.classesOrder:
      if k2 not in o.tree.classes:
         print '! Class %s missed in tree'%k2
         continue
      o2=o.tree.classes[k2]
      resTree+=obj2html(o2, 'class', tocTree, hLevel=hLevel+2, prefix=o.navName+'_c')
   if resTree:
      tocCurrent.add(tocTree)
      res+=('<section style="margin-top: 20px;" id="classesSection_%(navName)s"> <button class="btn btn-warning" type="button" data-toggle="collapse" data-target="#classes_%(navName)s"> Classes of module %(name)s</button> <div class="collapse in" id="classes_%(navName)s">'%o)+resTree+'</div> </section>'
   # functions
   fSetts=dict2magic([
      {'type':'public', 'prefix':'public', 'prefix2':'Public', 'color':'success', 'collapse':False},
      {'type':'private', 'prefix':'private', 'prefix2':'Private', 'color':'success', 'collapse':True},
      {'type':'special', 'prefix':'special', 'prefix2':'Special', 'color':'success', 'collapse':True},
      {'type':'undoc', 'prefix':'undoc', 'prefix2':'Un-documented', 'color':'default', 'collapse':True}
   ], True)
   for fSett in fSetts:
      tocTree=TOC(('<a href="#'+fSett.prefix+'FunctionsSection_%(navName)s" class="btn btn-default btn-xs">'+fSett.prefix2+' functions</a>')%o, collapsed=fSett.collapse)
      resTree=''
      for k2 in o.tree.methods[fSett.prefix+'Order']:
         if k2 not in o.tree.methods[fSett.prefix]:
            print '! Method %s missed in tree'%k2
            continue
         o2=o.tree.methods[fSett.prefix][k2]
         resTree+=obj2html(o2, 'function_'+fSett.prefix, tocTree, hLevel=hLevel+2, prefix=o.navName+'_f'+fSett.prefix)
      if resTree:
         tocCurrent.add(tocTree)
         res+=(('<section style="margin-top: 20px;" id="'+fSett.prefix+'FunctionsSection_%(navName)s"> <button class="btn btn-'+fSett.color+'" type="button" data-toggle="collapse" data-target="#'+fSett.prefix+'Functions_%(navName)s"> '+fSett.prefix2+' functions of module %(name)s</button> <div class="collapse '+('' if fSett.collapse else 'in')+'" id="'+fSett.prefix+'Functions_%(navName)s">')%o)+resTree+'</div> </section>'
   # modules
   resTree={}
   for k2, o2 in o.tree.modules.items():
      resTree.update(module2html(o2, tocTreeM, template, hLevel=hLevel))
   if resTree.keys():
      resMap.update(resTree)
   # build
   res=template%{'content':res, 'name':o.name, 'toc2':tocCurrent.toHtml(), 'toc2Title':'ToC of Module'}
   resMap[o.navName]={'active':active, 'html':res}
   return resMap

def staticGenerator(path, structure, originalTOC, template, api, newTOC=None, newTocOrder=None):
   newTOC=newTOC or TOC('<span class="btn btn-default btn-xs">%s</span>'%'root')
   chapterArr=pathList(path, alsoFiles=False, alsoDirs=True)
   # ordering
   if newTocOrder:
      chapterArr.sort(key=lambda x: oGet(newTocOrder, os.path.splitext(os.path.basename(x))[0], default=float('inf')))
   for chapterPath in chapterArr:
      if '__init__.py' not in pathList(chapterPath, fullPath=False): continue
      n=os.path.splitext(os.path.basename(chapterPath))[0]
      nowTOC=TOC('')
      nowTOC=newTOC.add('')
      #create scope
      scope=dict(globals())
      scope['api']=api
      scope['template']=template
      scope['originalTOC']=originalTOC
      scope['newTOC']=newTOC
      scope['nowTOC']=nowTOC
      scope['result']=magicDict({
         'navName':n, 'name':'', 'content':'',
         'toc1Title':'', 'toc2Title':'', 'toc1Order':None, 'toc2Order':None,
         'toc1Active_template':'<a href="%(navName)s.html" class="btn btn-default btn-xs">%(name)s</a>'
      })
      #exec chapter's code
      code=fileGet(chapterPath+'/__init__.py')
      eval(compile(code, '<string>', 'exec'), scope)
      scope['chapterResult']=scope['result']
      #sections
      contentTree=[]
      sectionArr=pathList(chapterPath)
      # ordering
      if scope['chapterResult'].toc2Order:
         sectionArr.sort(key=lambda x: oGet(scope['chapterResult'].toc2Order, os.path.splitext(os.path.basename(x))[0], default=float('inf')))
      for f in sectionArr:
         n2=os.path.splitext(os.path.basename(f))[0]
         if n2=='__init__': continue
         scope['result']=magicDict({
            'navName':n2, 'name':'', 'content':''
         })
         #exec section's code
         code=fileGet(f)
         eval(compile(code, '<string>', 'exec'), scope)
         scope['result'].content=scope['result'].content.replace('\<', '&lt;')
         scope['result'].content=scope['result'].content.replace('\>', '&gt;')
         scope['result'].content=scope['result'].content.replace('%', '%%')
         contentTree.append(scope['result'])
      template=scope['template']
      originalTOC=scope['originalTOC']
      newTOC=scope['newTOC']
      nowTOC=scope['nowTOC']
      res=scope['chapterResult']
      if len(contentTree):
         #generate section's content and TOC
         res.toc2=TOC('<a class="btn btn-default btn-xs">%s</a>'%res.name)
         for o in contentTree:
            res.content+='<h3 id="%(navName)s" class="">%(name)s <a class="headerlink" href="#%(navName)s" title="Permalink to %(name)s\'">¶</a> </h3> <section> %(content)s </section>'%o
            res.toc2.add('<a href="#%(navName)s" class="btn btn-default btn-xs">%(name)s</a>'%o)
         res.toc2=res.toc2.toHtml(res.toc2.root)
      else: res.toc2=''
      #finalize content
      res.content=res.content.replace('\<', '&lt;')
      res.content=res.content.replace('\>', '&gt;')
      res.content=res.content.replace('%', '%%')
      res.active=res.toc1Active_template%res
      res.html=template%res
      nowTOC.root=res.active
      structure[res.navName]=res
      # sub-chapters
      structure, _=staticGenerator(chapterPath, structure, None, template, api, newTOC=nowTOC, newTocOrder=res.toc1Order)
   if originalTOC: originalTOC.add(newTOC) #newTOC.add(originalTOC)
   return structure, newTOC

def api2html(api, path, template, staticGeneratorPath=None, staticGeneratorName=None, hLevel=1, cbBeforeSaving=None, toHead=None):
   template=fileGet(template)
   api=objEscape(api)
   tocCurrent=TOC()
   resMap={}
   resMap.update(module2html(api, tocCurrent, template, hLevel=hLevel+1, root=True))
   # static generator
   if staticGeneratorPath:
      s=None if staticGeneratorName is None else TOC('<span class="btn btn-default btn-xs">%s</span>'%staticGeneratorName)
      resMap, tocCurrent=staticGenerator(staticGeneratorPath, resMap, tocCurrent, template, api, newTOC=s)
   # callback before saving
   if isFunction(cbBeforeSaving):
      resMap, tocCurrent=cbBeforeSaving(resMap, tocCurrent, template, api)
   # saving
   for name, v in resMap.items():
      html=v['html']%{'toc1':tocCurrent.toHtml(v['active']), 'toc1Title':'ToC of Package', 'head':toHead or ''}
      p='%s/%s.html'%(path, name)
      resMap[name]=p
      fileWrite(p, html)
   return resMap

if __name__=='__main__': pass
