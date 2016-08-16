# -*- coding: utf-8 -*-

result.name="Gevent, Async and server's performance"
result.content="""

<h2>About Gevent, Async and server's performance</h2>

<p>Some server’s methods (like JSON processing or compression) not supported greenlets switching while processing. It can be big performance problem on highload.</p>

<p>
I start to implement functionality to solve this. This functionality implemented in sub-package <a href="aboutExperimentalPackage.html">flaskJSONRPCServer.experimental</a>, and you can try to use it on your risk (actually this sub-package used by me on prodaction systems from 2015 year, but i want more specific testing, before it will moved from <b>experimental</b>).
</p>

<p>
    Another big problem - not any code compatible with greenlets. This problem can be separated to 3 others:

    <ol>
        <li> Incompatible C-python extensions, like <a href="https://docs.python.org/2/library/gzip.html">gzip</a>, that block greenlet-switching while processed. </li>
        <li> Incompatible IO operations, like <a href="https://github.com/PyMySQL/PyMySQL">PyMysql</a>. Even if it patched with gevent, it can brake all server <a href="https://github.com/PyMySQL/PyMySQL/issues/451">while receiving long data</a>.</li>
        <li> Simply long-executed python code without ability for switching greenlets. It's every logical or math code, like iterating objects or arithmetic operations. While it processed, all server wait for complition. </li>
    </ol>
</p>

<p>
    For solving first and second problem i create a <a href="module_flaskJSONRPCServer.html#module_flaskJSONRPCServer_public_method_method_public_callAsync">workaround</a>, that can be used like <code class="language-python">result=server.callAsync(targerFunction, args, kwargs)</code> and run given function asynchronously, without blocking server. It really works!
</p>

<p>
    But third problem more complicated. Only really working solution for solwing this is using <a href="aboutParallelBackend.html">parallel executing backend</a> for "heavy" dispatchers.
</p>


"""
