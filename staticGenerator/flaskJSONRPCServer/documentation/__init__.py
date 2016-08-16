# -*- coding: utf-8 -*-

result.name='Documentation'
result.content="""

<h1>Documentation Overview</h1>

<p>Welcome to the <b>flaskJSONRPCServer <i>%s</i></b> documentation.</p>

<p>
   <b>flaskJSONRPCServer</b> was started as a simple, powerful and highload-ready JSON-RPC server. Main goals is power functionality, ability for serving many WSGI-apps and servers in one program, defence from dead-connections (in some cases clients don't correctly closes connections and this causes to locked file-descriptors) and high perfomance.
</p>

"""%(api.version)
result.toc1Order=[
   'aboutArchitecture',
   'aboutMultipleServers',
   'aboutMagicVarForDispatcher',
   'aboutHotReloading',
   'aboutGeventAndAsync'
]
result.toc2Order=[
   'aboutInstall',
   'aboutQuickStart',
]
