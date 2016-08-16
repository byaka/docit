# -*- coding: utf-8 -*-

# prepare attrs of magicVar
myapi=pydoc2api('flaskJSONRPCServer', 'flaskJSONRPCServer.aboutMagicVarForDispatcher')
attrs=dict2magic(iterate(lambda _, s, i:myapi.parseParam(s, i), myapi.docSplit(myapi.obj)[1]), recursive=True)
for p in attrs:
   if p.name!='call': continue
   p.type='object'
   p.descr+=' <a href="#aboutMagicVarForDispatcher__call">See this for more info</a>'
   break
attrs=params2html(attrs)
# prepare call's methods
call_methods=[]
#sleep
o=magicDict(api.tree.classes.flaskJSONRPCServer.tree.methods.private._sleep)
o.data=o.data.replace('_sleep(self, ', 'sleep(')
o.descr+=' Inherid from <a href="module_flaskJSONRPCServer.html#module_flaskJSONRPCServer_private_method_method_private__sleep">this method</a>.'
call_methods.append(obj2html(o, '', TOC()))
#log
o=magicDict(api.tree.classes.flaskJSONRPCServer.tree.methods.private._logger)
o.data=o.data.replace('_logger(self, ', 'log(')
o.descr+=' Inherid from <a href="module_flaskJSONRPCServer.html#module_flaskJSONRPCServer_private_method_method_private__logger">this method</a>.'
call_methods.append(obj2html(o, '', TOC()))
#lock
o=magicDict(api.tree.classes.flaskJSONRPCServer.tree.methods.public.lock)
o.data=o.data.replace('lock(self, ', 'lock(')
o.descr+=' Inherid from <a href="module_flaskJSONRPCServer.html#module_flaskJSONRPCServer_public_method_method_public_lock">this method</a>.'
o.params=dict2magic([s for s in o.params if s.name not in []], recursive=True)
call_methods.append(obj2html(o, '', TOC()))
#unlock
o=magicDict(api.tree.classes.flaskJSONRPCServer.tree.methods.public.unlock)
o.data=o.data.replace('unlock(self, ', 'unlock(')
o.descr+=' Inherid from <a href="module_flaskJSONRPCServer.html#module_flaskJSONRPCServer_public_method_method_public_unlock">this method</a>.'
o.params=dict2magic([s for s in o.params if s.name not in []], recursive=True)
call_methods.append(obj2html(o, '', TOC()))
#wait
o=magicDict(api.tree.classes.flaskJSONRPCServer.tree.methods.public.wait)
o.data=o.data.replace('wait(self, ', 'wait(')
o.data=o.data.replace('sleepMethod=None, ', '')
o.descr+=' Inherid from <a href="module_flaskJSONRPCServer.html#module_flaskJSONRPCServer_public_method_method_public_wait">this method</a>.'
o.params=dict2magic([s for s in o.params if s.name not in ['sleepMethod']], recursive=True)
call_methods.append(obj2html(o, '', TOC()))
#lockThis
o=magicDict(api.tree.classes.flaskJSONRPCServer.tree.methods.public.lock)
o.data=o.data.replace('lock(self, dispatcher=None', 'lockThis(')
o.descr=o.descr.replace('server or specific &lt;dispatcher&gt;', 'current dispatcher')
o.descr+=' Inherid from <a href="module_flaskJSONRPCServer.html#module_flaskJSONRPCServer_public_method_method_public_lock">this method</a>.'
o.params=dict2magic([s for s in o.params if s.name not in ['dispatcher']], recursive=True)
call_methods.append(obj2html(o, '', TOC()))
#unlockThis
o=magicDict(api.tree.classes.flaskJSONRPCServer.tree.methods.public.unlock)
o.data=o.data.replace('unlock(self, dispatcher=None, ', 'unlockThis(')
o.descr=o.descr.replace('server or specific &lt;dispatcher&gt;', 'current dispatcher')
o.descr+=' Inherid from <a href="module_flaskJSONRPCServer.html#module_flaskJSONRPCServer_public_method_method_public_unlock">this method</a>.'
o.params=dict2magic([s for s in o.params if s.name not in ['dispatcher']], recursive=True)
call_methods.append(obj2html(o, '', TOC()))
#waitThis
o=magicDict(api.tree.classes.flaskJSONRPCServer.tree.methods.public.wait)
o.data=o.data.replace('wait(self, dispatcher=None, sleepMethod=None, ', 'waitThis(')
o.descr=o.descr.replace('server or specific &lt;dispatcher&gt;', 'current dispatcher')
o.descr+=' Inherid from <a href="module_flaskJSONRPCServer.html#module_flaskJSONRPCServer_public_method_method_public_wait">this method</a>.'
o.params=dict2magic([s for s in o.params if s.name not in ['dispatcher', 'sleepMethod']], recursive=True)
call_methods.append(obj2html(o, '', TOC()))
#completed
call_methods=''.join(call_methods)
# name of section
result.name='MagicVar in Dispatchers'
# content
result.content="""

<h2>About MagicVar in Dispatchers</h2>

<p><b>MagicVar</b> is a variable, that will be passed to dispatcher, if dispatcher contain special magic parametr. Name of this parametr can be setted with <code>\<magicVarForDispatcher\></code> parametr, when you initialize server. By default it is "_connection". <b>MagicVar</b> will be passed like Object-Dict (you can access his attributes like <code>\<magicVar\>[key]</code> or like <code>\<magicVar\>.key</code>).</p>

<p>Example, how it's working by default.</p>

<pre><code class="language-python">def testDispatcher1(param1, param2, _connection=None):
   print 'IP:', _connection.ip
   if _connection.ip=='127.0.0.1': return 'Hello, localhost!'
   else: return 'Hello, '+_connection.ip

server=flaskJSONRPCServer(("0.0.0.0", 7001))
server.registerFunction(testDispatcher1, path='/api')
server.start()
</code></pre>

<p>Example, how to change name of <b>MagicVar</b>.</p>

<pre><code class="language-python">def testDispatcher1(param1, param2, magicVar=None):
   print 'IP:', magicVar.ip
   if magicVar.ip=='127.0.0.1': return 'Hello, localhost!'
   else: return 'Hello, '+magicVar.ip

server=flaskJSONRPCServer(("0.0.0.0", 7001), magicVarForDispatcher='magicVar')
server.registerFunction(testDispatcher1, path='/api')
server.start()
</code></pre>

<p>Object <b>MagicVar</b>, passed to dispatcher, will contain next attributes:</p>

%s

<p id="aboutMagicVarForDispatcher__call">
Special attribute <b>call</b> contains some methods, specially prepared for using from dispatchers.
</p>

%s

<p>Optionally, some execution-backends can add another methods to <b>call</b> attribute.</p>
"""%(attrs, call_methods)
