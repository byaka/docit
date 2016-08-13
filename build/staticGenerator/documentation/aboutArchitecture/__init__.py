# -*- coding: utf-8 -*-

result.name="Server's architecture"
result.content="""

<h2>About Server's architecture</h2>

<p>Architecture of server is pretty simple and follow Unix-way. Every component process only one specific task. Every component can be changed, and if it support input and output format correctly, server will work correctly.</p>

<p>
<img style="position: relative; margin-left: 10%; margin-right: 10%; width: 80%; height: auto;" src="../img/server_architecture.svg" alt="server's architecture">
</p>

<p>
As you can see, only part of server, that know about JSON-format is <b>JSON-backend</b>. If you change it, your server can support any another protocol.
</p>

<p>
Same think with <b>Execution-backend</b>, if we create another (and it correctly cupport input and output format), server will use it without changing source. For example, in this way works <a href="aboutParallelBackend.html"><b>Parallel-backend</b></a>, that execute dispatchers in separate processes.
</p>

"""
