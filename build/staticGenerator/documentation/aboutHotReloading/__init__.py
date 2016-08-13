# -*- coding: utf-8 -*-

result.name='Hot-Reloading'
result.content="""

<h2>About Hot-Reloading</h2>

<p>You can overload source of specific dispatchers without stopping by using <code>reload()</code> methor.</p>

<pre><code class="language-python">server.reload(data, clearOld=False)</code></pre>

<p>Flag <code>\<clearOld\></code> will remove all earlier existing dispatchers.</p>

<p>
This operation safe, if something goes wrong, lib restore previous source. While reloading, server stop processing requests, but not reject them. Server handle all requests, and when reloading completed, all handled requests will be processed. It also wait for completing processing requests before start reloading and you can pass <code>\<timeout\></code> for this waiting. Also you can pass <code>\<processingDispatcherCountMax\></code> and server will not wait for given number of processed requests.
</p>

<p>When reloading, you can change source, merge new variables with old and many more.</p>

<pre><code class="language-python">data=[
   {
      'dispatcher':'testForReload1',
      'scriptPath':server._getScriptPath(True),
      'isInstance':False,
      'overload':[
         {'globalVar1':globalVar1},
         callbackForManualOverload
      ],
      'path':'/api'
   }
]</code></pre>

<p>For now overloading supports for any dispatcher or several dispatchers separately (you can fully change all dispatcher's settings and of course source and variables).</p>

<p>
When you reload dispatcher and give path for file (of course it can be same file as "main"), this file imported. Then lib overloaded variables and attributes you give and replace old dispatcher with new from this module. If you give one path for several dispatchers, they all work in one imported file (in this case file will import one time only, not for every dispatcher).
</p>

<p>If you need to overload some objects, that not dispatchers but used in them, you simply can do this with callback.</p>

<pre><code class="language-python">def callbackForManualOverload(server, module, dispatcher):
   # overload globals also
   for k in dir(module):
      globals()[k]=getattr(module, k)</code></pre>

<p>This code overload all global variables and replace them with variables from just imported file.</p>

<p>In future i add simple method for reloading all source of server. Progress of this task can be fineded <a href="https://github.com/byaka/flaskJSONRPCServer/issues/49">here</a> (in russian).</p>

"""
