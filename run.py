# -*- coding:utf-8 -*-
# author  : Fran_Chau
# datetime: 2019/3/11
import time
from getAllHtml import GetAllHtml
from getJS import GetJS
from getDataJson import GetDataJson
from renderJsGetHideContents import RenderJsGetHideContents
from extractData import ExtractData

if __name__ == '__main__':
    print('*' * 50)
    startTime = time.time()

    GetAllHtml().main()
    GetJS().main()
    GetDataJson().main()
    RenderJsGetHideContents().main()
    ExtractData().main()

    print("\n\n总耗时： ", time.time() - startTime)
    print('*' * 50)
