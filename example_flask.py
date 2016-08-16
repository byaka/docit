# -*- coding: utf-8 -*-
import sys
from docit.utils import *

from docit.generator import *
from docit.pydoc2api import *

if __name__=='__main__':
   path=os.path.dirname(os.path.realpath(sys.argv[0]))+'/'
   docitPath=path+'docit/'
   outputPath=path+'output/flask/'
   parentPath='/'.join(path.split('/')[:-2])+'/'
   # print path, docitPath, outputPath, parentPath, raw_input()
   # запускаем анализ родительского модуля. в большинстве случаев этого достаточно, дочерние модули будут подхватываться автоматически.
   api=pydoc2api('flask', '')
   # директива 'self.' захватит все, что импортировано из дочерних модулей внутрь родительского
   api=api.summary(moduleWhitelist=['self', 'self.'])
   #complete and saving documentation
   # добавляем счетчик GA
   toHead=""
   # записываем в отдельный файл внутренний индекс, построенный библиотекой. помогает при дебаге
   fileWrite(outputPath+'api.json', reprEx(api, indent=3, sortKeys=True))
   # конвертация из внутреннего индекса в html
   files=api2html(api,
      outputPath+'pages',
      docitPath+'build/template/simpleBootstrapWithToc.html',
      hLevel=1,
      toHead=toHead
   )
   print 'Documentation generated!'
   for name, path in files.items(): print '>>', path
