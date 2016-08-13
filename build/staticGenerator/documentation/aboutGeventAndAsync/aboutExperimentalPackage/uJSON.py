# -*- coding: utf-8 -*-

result.name='uJSON'
result.content="""

<p>
Extremely fast JSON-backend, based on <a href="https://github.com/esnme/ultrajson">UltraJSON</a> package, written in pure C with bindings for Python. Experimental package automatically use this backend, if it installed in system.
<p>

<p>
For now <b>uJSON</b> replaces this methods (server will use new variant of method by default):
<ul>
    <li><a href="module_flaskJSONRPCServer.html#module_flaskJSONRPCServer_private_method_method_private__parseJSON"><code>_parseJSON()</code></a></li>
    <li><a href="module_flaskJSONRPCServer.html#module_flaskJSONRPCServer_private_method_method_private__serializeJSON"><code>_serializeJSON()</code></a></li>
</ul>
<p>

<table class="table table-condensed"><tbody>
    <tr> <td><b>Perfomance issues</b></td> <td>None</td> </tr>
    <tr> <td><b>Testing</b></td> <td>Need more</td> </tr>
    <tr> <td><b>Broken functionality</b></td> <td>For now it not implements type-extending (<code>\<default\></code> param) and disabling escaping of non-ASCII characters ( <code>\<ensure_ascii\></code> param). Also it not support <code>long()</code> type and crash on them (see <a href="https://github.com/esnme/ultrajson/issues/99">this</a> issue).</td> </tr>
</tbody></table>

"""
