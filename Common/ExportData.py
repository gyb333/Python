import  pymysql as ps
from Common.DB.DataAccess import DataAccess
from Common import DataToExcel
import pandas as pd


def getOrg():
    da = DataAccess()
    cmdText = '''SELECT o.OrgID,o.OrgCode,o.OrgName,o.ParentOrgID 
                  FROM org o
                  where o.OrgType=%s'''
    params = (3)
    res = da.ExecuteNonQuery(cmdText, params)
    return  res


def getCustomer(orgID):
    da = DataAccess()
    cmdText = '''SELECT 'kds3' AS 来源系统, cb.CompBranchCodeSAP AS 户头SAP代码, cb.CompBranchName AS 户头名称,
  f.Code AS 客户编码,f.Name AS 客户名称,     
  REPLACE(SUBSTR(cust.StandardCustAttribute, INSTR(cust.StandardCustAttribute, '"CustChannelTypeName":') + 22, 
  INSTR(cust.StandardCustAttribute, '"CustChannel":') - INSTR(cust.StandardCustAttribute, '"CustChannelTypeName":') - 23), '"', '') AS 渠道类型, 
  REPLACE(SUBSTR(cust.StandardCustAttribute, 
  INSTR(cust.StandardCustAttribute, '"CustChannelName":') + 18, 
  INSTR(cust.StandardCustAttribute, '"CustArea":') - INSTR(cust.StandardCustAttribute, '"CustChannelName":') - 19), '"', '') AS 客户类型,
  rDic.省, rDic.市, rDic.`县/区`, rDic.`镇/街道`, rDic.村,
  p.Name AS 联系人, p.Mobile AS 联系电话
  FROM companycustomers cust
  INNER JOIN firms f ON cust.Id = f.Id
  INNER JOIN companybranch cb ON cust.CompanyBranchCompBranchID = cb.CompBranchID
  INNER JOIN distributor d on cb.DistributorID = d.DistributorID
  INNER JOIN orgdistributorcontractrelationship ship ON d.DistributorContractID = ship.DistributorContractID and ship.IsValid = 1
  LEFT JOIN firmcontacts fc on f.Id = fc.FirmId
  LEFT JOIN persons p on p.Id = fc.Id
  LEFT JOIN 
  (
SELECT r.Id, r.Name AS 省, '' AS 市, '' AS '县/区',  '' AS  '镇/街道', '' AS 村 FROM regions r where r.Level = 1 and r.IsValid = 1
  UNION ALL 
  SELECT r.Id, r1.Name AS 省, r.Name AS 市, '' AS '县/区',  '' AS  '镇/街道', '' AS 村 from regions r 
    LEFT JOIN regions r1 ON r.RegionId = r1.Id AND r1.IsValid = 1 AND r1.Level = 1
  WHERE r.Level = 2 AND r.IsValid = 1
    union all
 SELECT r.Id, r2.Name AS 省, r1.Name AS 市, r.Name AS '县/区',  '' AS  '镇/街道', '' AS 村 FROM regions r
    LEFT JOIN regions r1 ON r.RegionId = r1.Id AND r1.IsValid = 1  AND r1.Level = 2
    LEFT JOIN regions r2 ON r1.RegionId = r2.Id AND r2.IsValid = 1  AND r2.Level = 1
  WHERE r.Level = 3 AND r.IsValid = 1
   union all
 SELECT r.Id, r3.Name AS 省, r2.Name AS 市, r1.Name AS '县/区',  r.Name AS  '镇/街道', '' AS 村 FROM regions r
    LEFT JOIN regions r1 ON r.RegionId = r1.Id AND r1.IsValid = 1 AND r1.Level = 3
    LEFT JOIN regions r2 ON r1.RegionId = r2.Id AND r2.IsValid = 1 and r2.Level = 2
  LEFT JOIN regions r3 ON r2.RegionId = r3.Id AND r3.IsValid = 1 AND r3.Level = 1
  WHERE r.Level = 4 AND r.IsValid = 1
   union all
 SELECT r.Id, r4.Name AS 省, r3.Name AS 市, r2.Name AS '县/区',  r1.Name AS  '镇/街道', r.Name AS 村 FROM regions r
    LEFT JOIN regions r1 ON r.RegionId = r1.Id AND r1.IsValid = 1 AND r1.Level = 4
    LEFT JOIN regions r2 ON r1.RegionId = r2.Id AND r2.IsValid = 1 AND r2.Level = 3
  LEFT JOIN regions r3 ON r2.RegionId = r3.Id AND r3.IsValid = 1 AND r3.Level = 2
  LEFT JOIN regions r4 ON r3.RegionId = r4.Id AND r4.IsValid = 1 AND r4.Level = 1
  WHERE r.Level = 5 AND r.IsValid = 1
  ) rDic ON cust.RegionId = rDic.Id
WHERE ship.OrgID = %s AND ship.BussLineID = 100000042 AND cust.RegionId is NOT NULL;'''
    params = (orgID)
    res = da.ExecuteNonQuery(cmdText, params)
    return res

def test():
    Orgs = getOrg()
    print(Orgs['effect_row'])
    df = Orgs["rows"]

    print(df._stat_axis.values.tolist())  # 行名称
    print(df.columns.values.tolist())  # 列名称
    # 根据索引遍历df
    for indexs in df.index:
        print(df.loc[indexs].values[0:3])
        break

    for index, row in df.iterrows():
        print(row[0], row[2], row[3])
        break;

    for row in df.itertuples(index=True, name='Pandas'):
        print(getattr(row, 'OrgID'), getattr(row, 'OrgName'))


def main():
    Orgs=getOrg()
    print(Orgs['effect_row'])
    df = Orgs["rows"]
    # basePath="C:\\Users\\zhongduzhi\\Desktop\\各分公司数据\\"
    # for row in df.itertuples(index=True, name='Pandas'):
    #     orgID=getattr(row, 'OrgID')
    #     orgName=getattr(row, 'OrgName')
    #     data =getCustomer(orgID)
    #     filePath=basePath+orgName+".xlsx"
    #     DataToExcel.write_to_excel_with_openpyxl(data["rows"],data["heads"],filepath=filePath)



if __name__ == '__main__':
    main()
