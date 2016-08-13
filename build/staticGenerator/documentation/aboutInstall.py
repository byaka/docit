# -*- coding: utf-8 -*-

result.name='How to install'
result.content="""

<h4>With pip</h4>

<p>Latest stable build can be simply installed with pip.</p>

<code>pip install flaskJSONRPCServer</code>

<h4>Manually</h4>

<ol>
    <li>Download the most recent tarball from the <a href="https://pypi.python.org/pypi/flaskJSONRPCServer">download page</a>.</li>
    <li>Unpack the tarball.</li>
    <li>Run <code>python setup.py install</code>.</li>
</ol>

<p>Note that the last command will automatically download and install setuptools if you don’t already have it installed. This requires a working Internet connection.</p>

<p>This will install <b>flaskJSONRPCServer</b> into your Python installation’s site-packages directory.</p>

<h4>Installing the development version</h4>

<ol>
    <li>Install Git</li>
    <li>Run <code>git clone git://github.com/byaka/flaskJSONRPCServer.git</code></li>
    <li>Run <code>cd flaskJSONRPCServer</code></li>
    <li>Run <code>pip install --editable</code>.</li>
</ol>

<h4>Gevent</h4>

<p>For production use strongly recommendet to install <a href="http://www.gevent.org/intro.html#installation-and-requirements">gevent backend</a> and switch all servers to use it by passing <code>\<gevent\></code> to constructor.</p>

<pre><code class="language-python">server=flaskJSONRPCServer(["127.0.0.1", "8080"], gevent=True)</code></pre>

"""
