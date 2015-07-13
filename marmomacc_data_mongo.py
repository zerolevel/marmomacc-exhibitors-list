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
from pymongo import MongoClient
import MarmomaccData as MD




def main():
    db = MongoClient().marmomaccdata
    file = open("resources/categoryList.csv")
    data = file.read().split("\n")
    file.close()
    companiesList = [] ##Companies whose values have already been recieved
    for ds in data:
        d = ds.split("?")
        category = {
            "categId": d[0],
            "categName": d[1],
            "parentCategory": d[2]
        }
        companyList = MD.CompanyList(category["categId"])
        for cId in companyList.list:
            if cId not in companiesList:
                companyDetail = MD.CompanyDetail(cId)
                db.data.insert(companyDetail.get_object())
            db.data.update({"_id": cId}, {"$push": {"category": category}})
            companiesList.append(cId)


if __name__ == '__main__':
    main()