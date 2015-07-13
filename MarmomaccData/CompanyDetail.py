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


class CompanyDetail:
    """
    Company Detail object, contains details of the company recieved from Marmomacc website
    """
    name = ""
    description = ""
    address = ""
    email = ""
    website = ""
    phone = ""
    fax = ""
    country = ""

    def __init__(self, cId):
        """
        Constructor for CompanyDetail.
        Note that the Constructor makes an HTTP request to marmomacc website to get the details of the company.
        :param cId: CompanyId
        """
        self.cId = cId
        self.__getDetails()

    def __getCompanyHTMLdata(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        http = httplib2.Http()
        url = "http://catalogo.marmomacc.it/ajax/getDetail.php"
        #Params Taken from Network option in browser
        #UrlEcnode not used(Why?)
        params = "idNews="+ str(self.cId) + "&evento=mar&mobiledevice=&tabletdevice=&lingua=it"
        response, content = http.request(url, "POST", headers=headers, body=params)
        if response.status == 200:
            return content
        else:
            return None

    def __getDetails(self, htmlData=None):
        if htmlData is None:
            htmlData = self.__getCompanyHTMLdata()

        soup = BeautifulSoup(htmlData)

        #Description of the company is embeded in the class "scrollerAttivita"
        self.description = soup.findAll("div", {"class": "scrollerAttivita"})[0].getText()
        self.description = self.description.replace("\n", " ").replace("\t", "").replace("\r", "")

        #Name is embeded in id "regionesociale"
        self.name = soup.findAll("div", {"id": "ragionesociale"})[0].getText()
        self.name = self.name.encode('utf8')

        #Details are embeded in class "scheda-blocco-indirizzi"
        div_contact_detail = soup.findAll("div", {"class": "scheda-blocco-indirizzi"})[0]
        details = div_contact_detail.findAll("p")
        i = 0
        flag = True
        last = ""
        for p in details:
            if flag:
                if str(p.a) != 'None':
                    flag = False
                    self.address = self.address[0:self.address.__len__()-1]
                    self.country = last.encode('utf8')
                else:
                    last = p.getText()
                    last = last.encode('utf8')
                    self.address = self.address+last + " ".encode('utf8')

            if not flag:
                increased = False
                if i == 0:
                    try:
                        email_detail = p.a.get("href")
                        self.email = email_detail.split(":")[1].encode('utf8')
                    except AttributeError:
                        #In case there is no data in the said space
                        i+=1
                        increased = True
                        pass
                if i == 1:
                    try:
                        self.website = p.a.get("href").encode('utf8')
                    except AttributeError:
                        i+=1
                        increased = True
                        pass
                if i == 2:
                    try:
                        self.phone = str(p.getText()).encode('utf8')
                    except AttributeError:
                        pass
                if i == 3:
                    try:
                        self.fax = str(p.getText()).encode('utf8')
                    except AttributeError:
                        pass
                if not increased:
                    i+=1

    def get_object(self):
        return {
            "name" : self.name,
            "description" : self.description,
            "address" : self.address,
            "email" : self.email,
            "website" : self.website,
            "phone" : self.phone,
            "fax" : self.fax,
            "category": [],
            "country": self.country,
            "_id": self.cId
        }