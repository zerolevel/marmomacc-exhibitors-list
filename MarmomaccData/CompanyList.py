#Copyright [MohitDaga05@gmail.com] [Mohit Daga]
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.
import httplib2
from bs4 import BeautifulSoup


class CompanyList:
    """
    Creates an object for the Company List Ids which are included in category defined by categ_id
    Note: Constructor will make two http requests one for the count other for the list.
    :param categ_id Category Id of the type category.
    :param categ_name Category Name of the type Category
    """
    def __init__(self, categ_id, categ_name=None):
        self.categ_id = categ_id
        self.categ_name = categ_name
        self.count = self.__getCount()
        self.list = self.__getList()


    def __getCount(self):
        """
        returns the count of the Companies listed in a type category.
        """
        headers = {
            'Content-Type':'application/x-www-form-urlencoded'
        }
        http = httplib2.Http()
        url = "http://catalogo.marmomacc.it/ajax/getCountArticles.php"
        #Taken from  browser
        params = "jsonData%5BSezione%5D%5Btype%5D=WHERE&jsonData%5BSezione%5D%5Boperator%5D=%3D+'mar'&" \
                 + "jsonData%5BCodiceMerceologia%5D%5Btype%5D=AND&jsonData%5BCodiceMerceologia%5D%5Boperator%5D=LIKE+'"\
                 + str(self.categ_id) + "'&jsonData%5BORDER%5D%5Btype%5D=" \
                 + "&jsonData%5BORDER%5D%5Boperator%5D=BY+RagioneSociale&jsonData%5BLIMIT%5D%5Btype%5D=&" \
                 + "jsonData%5BLIMIT%5D%5Boperator%5D=0%2C20&idProduct=0&idChild=0&lingua=en"

        response, content = http.request(url, "POST", headers=headers, body=params)
        if response.status == 200:
            try:
                res = float(str(content))
                return res
            except ValueError:
                return -1

    def __getList(self, count=None):
        """
        returns list of the Companies listed in type type category.
        """
        if count is None:
            count = self.count
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        http = httplib2.Http()
        url = "http://catalogo.marmomacc.it/ajax/getArticles.php"
        #Taken from Network browser
        params = "jsonData%5BSezione%5D%5Btype%5D=WHERE&jsonData%5BSezione%5D%5Boperator%5D=%3D+'mar'&" \
                 "jsonData%5BCodiceMerceologia%5D%5Btype%5D=AND&jsonData%5BCodiceMerceologia%5D%5Boperator%5D=LIKE+'" \
                 + str(self.categ_id) + "'&jsonData%5BORDER%5D%5Btype%5D=&jsonData%5BORDER%5D%5Boperator%5D=BY+" \
                + "RagioneSociale&jsonData%5BLIMIT%5D%5Btype%5D=&jsonData%5BLIMIT%5D%5Boperator%5D=0%2C"+ \
                 str(count) + "&idProduct=0&idChild=0&lingua=en"
        
        response, content = http.request(url, "POST", headers=headers, body=params)
        if response.status == 200:
            #print content
            content = content.replace('\n', ' ').replace('\r', ' ')
            html = content.replace("'", '"')
            soup = BeautifulSoup(html)
            res = []
            for lis in soup.body.childGenerator():
                try :
                    index = lis.get("tabindex")
                    res.append(int(str(index)))
                except AttributeError:
                    pass
            return res
