# -*- coding: utf-8 -*-

result.name='MoreAsync'
result.content="""

<p>
Tricky implementations of some servers methods that add async executing. It very useful in Gevent backend. When server start some methods (like compression or hashing) with large data, it hang all server. It very big performance problem and this extension solve this. When <b>moreAsync</b> enabled, some jobs run in separate threads (greenlets) and main thread only wait for completing. And while wait, it can do another jobs.
<p>

<p>
For now <b>moreAsync</b> replaces this methods (server will use async variant of method, if some conditions happened):
<ul>
    <li><a href="module_flaskJSONRPCServer.html#module_flaskJSONRPCServer_private_method_method_private__compressGZIP"><code>_compressGZIP()</code></a> (input's size more then <i>1mb</i>)</li>
    <li><a href="module_flaskJSONRPCServer.html#module_flaskJSONRPCServer_private_method_method_private__uncompressGZIP"><code>_uncompressGZIP()</code></a> (input's size more then <i>1mb</i>)</li>
    <li><a href="module_flaskJSONRPCServer.html#module_flaskJSONRPCServer_private_method_method_private__sha256"><code>_sha256()</code></a> (input's size more then <i>100mb</i>)</li>
    <li><a href="module_flaskJSONRPCServer.html#module_flaskJSONRPCServer_private_method_method_private__sha1"><code>_sha1()</code></a> (input's size more then <i>100mb</i>)</li>
</ul>
<p>

<table class="table table-condensed"><tbody>
    <tr> <td><b>Perfomance issues</b></td> <td>None</td> </tr>
    <tr> <td><b>Testing</b></td> <td>Need more</td> </tr>
    <tr> <td><b>Broken functionality</b></td> <td>None</td> </tr>
</tbody></table>

"""
