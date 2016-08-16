# -*- coding: utf-8 -*-

result.name='asyncJSON'
result.content="""

<p>
Pseudo-async implementation of JSON parser and dumper. It allow to switch context (switching to another greenlet or thread) every given number of seconds. This mean that if method proseccing so long, it will be paused and switched to another task. Useful on processing large data.
<p>

<p>
For now <b>asyncJSON</b> replaces this methods (server will use async variant of method, if some conditions happened):
<ul>
    <li><a href="module_flaskJSONRPCServer.html#module_flaskJSONRPCServer_private_method_method_private__parseJSON"><code>_parseJSON()</code></a> (input's size more then <i>1mb</i>)</li>
    <li><a href="module_flaskJSONRPCServer.html#module_flaskJSONRPCServer_private_method_method_private__serializeJSON"><code>_serializeJSON()</code></a> (input's size more then <i>1mb</i>)</li>
</ul>
<p>

<table class="table table-condensed"><tbody>
    <tr> <td><b>Perfomance issues</b></td> <td>3-5 times slower (than uJSON) on serialization and 10 times on parsing</td> </tr>
    <tr> <td><b>Testing</b></td> <td>Need more</td> </tr>
    <tr> <td><b>Broken functionality</b></td> <td>For now it not implements type-extending (<code>\<default\></code> param), disabling escaping of non-ASCII characters ( <code>\<ensure_ascii\></code> param) and checking circular reference (<code>\<check_circular\></code> param)</td> </tr>
</tbody></table>

<p>Also <b>asyncJSON</b> correctly supports <code>long()</code> type, so i planning to use it as fallback, when <a href="#uJSON">uJSON</a> crached. Progress of this task can be fineded <a href="https://github.com/byaka/flaskJSONRPCServer/issues/78">here</a> (in russian).</p>
"""
