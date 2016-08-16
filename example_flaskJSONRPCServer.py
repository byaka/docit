# -*- coding: utf-8 -*-
import sys
from docit.utils import *

from docit.generator import *
from docit.pydoc2api import *

if __name__=='__main__':
   """
   Просто пример использования.
   """
   path=os.path.dirname(os.path.realpath(sys.argv[0]))+'/'
   docitPath=path+'docit/'
   outputPath=path+'output/flaskJSONRPCServer/'
   parentPath='/'.join(path.split('/')[:-2])+'/'
   # print path, docitPath, outputPath, parentPath, raw_input()
   # указываем дополнительные пути расположения модулей
   paths=[
      parentPath,
      parentPath+'flaskJSONRPCServer/',
      # parentPath+'flaskJSONRPCServer/flaskJSONRPCServer/servBackend/'
   ]
   sys.path=paths+sys.path
   # запускаем анализ родительского модуля. в большинстве случаев этого достаточно, дочерние модули будут подхватываться автоматически.
   api=pydoc2api('flaskJSONRPCServer', '')
   # директива 'self.' захватит все, что импортировано из дочерних модулей внутрь родительского
   api=api.summary(moduleWhitelist=['self', 'self.'])
   # модуль wsgiex не попадет в данную API, поскольку импортируется в runtime
   api2=pydoc2api('flaskJSONRPCServer.servBackend.wsgiex', '')
   api2=api2.summary(moduleWhitelist=['self', 'self.'])
   api2.name=api2.data='wsgiex'
   api.tree.modules['flaskJSONRPCServer.servBackend'].tree.modules['flaskJSONRPCServer.servBackend.useWsgiex'].tree.modules['wsgiex']=api2
   #complete and saving documentation
   # добавляем счетчик GA
   toHead="""
   <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

      ga('create', 'UA-64341792-3', 'auto');
      ga('send', 'pageview');
   </script>
   """
   # записываем в отдельный файл внутренний индекс, построенный библиотекой. помогает при дебаге
   fileWrite(outputPath+'api.json', reprEx(api, indent=3, sortKeys=True))
   # конвертация из внутреннего индекса в html
   files=api2html(api,
      outputPath+'pages',
      docitPath+'build/template/simpleBootstrapWithToc.html',
      staticGeneratorPath=path+'staticGenerator/flaskJSONRPCServer/',
      staticGeneratorName='Package flaskJSONRPCServer',
      hLevel=1,
      toHead=toHead
   )
   print 'Documentation generated!'
   for name, path in files.items(): print '>>', path
