# -*- coding: utf-8 -*-

result.name='Quick start'
result.content="""

<p>Start using <b>flaskJSONRPCServer</b> is really simple!</p>

<p>
First of all, you need ability to send json-rpc requests to server. You can do it with different ways, for example:

<ul>
    <li>Using special library (like <a href="https://github.com/tcalmant/jsonrpclib">jsonrpclib</a>) and Python Interpreter.</li>
    <li>Send request via <a href="https://curl.haxx.se/">cURL</a> in correct <a href="http://www.jsonrpc.org/specification#examples">format</a></li>
    <li>Any another way.</li>
</ul>
</p>

<p>
After this you can simply run one of examples, included to package.

<pre><code>python -m flaskJSONRPCServer -x simple.py</code></pre>

And send first request (for example <code>{"jsonrpc": "2.0", "method": "echo", "params": ['Hello world!'], "id": 1}</code>).
</p>

<p>Sources of all included examples can be finded <a href="https://github.com/byaka/flaskJSONRPCServer/tree/master/flaskJSONRPCServer/example">here</a>.</p>

"""
