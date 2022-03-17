#import sys
#sys.path.insert(1,'lib')

import requests
import lxml.html






def explore_Version():

    value_str = ''
    
    url =  "https://astaroth.pythonanywhere.com/version"

    try:
    
        response = requests.get(url, stream=True)
        response.raw.decode_content = True
        tree = lxml.html.parse(response.raw)

        value_str = float(str(tree.xpath('/html/body/p/text()'))[2:-2])
        
        print("\nSearching Astaroth version:",value_str)

    except:

        print("\nWarning: Can't read Astaroth version number right now...")



    return value_str










if __name__ == '__main__':
    explore_Version()



