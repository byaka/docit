# -*- coding: utf-8 -*-

result.name='Experimental package'
result.toc2Title='ToC of Experimental package'
result.content="""

<h2>About Experimental package</h2>

<p>This package contains experimental extensions for <b>flaskJSONRPCServer</b>. This mean that this extensions need more testing or they breaks some functionality.</p>

<p>For use provided patches, pass flag <code>\<experimental\></code> to server's constructor. Server will be automatically patched with optimal settings.</p>

<pre><code class="language-python">server=server=flaskJSONRPCServer(["127.0.0.1", "8080"], experimental=True)</code></pre>

<p>For now this package contain next patches.</a>

"""
result.toc2Order=[
   'moreAsync',
   'uJSON',
   'asyncJSON'
]
