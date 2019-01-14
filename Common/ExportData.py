from Common.DB.DataAccess import DataAccess, dbType
from Common.DB.EnumType import DBType
from Common import DataToExcel
from Common import FileUtil


def getOrg(orgID=None):
    da = DataAccess()
    if dbType == DBType.MYSQL:
        cmdText = '''SELECT o.OrgID,o.OrgCode,o.OrgName,o.ParentOrgID
                      FROM org o
                      where o.OrgType=%s'''
    elif dbType == DBType.SQLSERVER:
        cmdText = '''SELECT o.OrgID,o.OrgCode,o.OrgName,o.ParentID
                      FROM t_Org o
                      where o.OrgType=%s '''
    params = [3]
    if not orgID is None:
        cmdText += " AND o.OrgID=%s"
        params.append(orgID)
        print(params)
    res = da.ExecuteNonQuery(cmdText, tuple(params))
    return res


def getCustomer(orgID):
    da = DataAccess()
    if dbType == DBType.MYSQL:
        cmdText = '''SELECT 'kds3' AS 来源系统, cb.CompBranchCodeSAP AS 户头SAP代码, cb.CompBranchName AS 户头名称,
  f.Id AS 客户ID,f.Code AS 客户编码,f.Name AS 客户名称,     
  REPLACE(SUBSTR(cust.StandardCustAttribute, INSTR(cust.StandardCustAttribute, '"CustChannelTypeName":') + 22, 
  INSTR(cust.StandardCustAttribute, '"CustChannel":') - INSTR(cust.StandardCustAttribute, '"CustChannelTypeName":') - 23), '"', '') AS 渠道类型, 
  REPLACE(SUBSTR(cust.StandardCustAttribute, 
  INSTR(cust.StandardCustAttribute, '"CustChannelName":') + 18, 
  INSTR(cust.StandardCustAttribute, '"CustArea":') - INSTR(cust.StandardCustAttribute, '"CustChannelName":') - 19), '"', '') AS 客户类型,
  rDic.省, rDic.市, rDic.`县/区`, rDic.`镇/街道`, rDic.村,
  cust.Address AS 客户地址,
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
    WHERE ship.OrgID = %s AND ship.IsValid=1 AND ship.BussLineID = 100000042 AND cust.RegionId is NOT NULL;'''
        params = (orgID)
    elif dbType == DBType.SQLSERVER:
        cmdText = '''SELECT *
    FROM (
    SELECT
    'KDS2' AS 来源系统
    ,cb.CompBranchCode_SAP '户头sap代码'
    ,cb.CompBranchName AS '户头名称'
    ,tcb.CustID
    ,CustCode AS '客户编码'
    ,CustName AS '客户名称'
    ,tcct.CustChannelTypeName AS '渠道类型'
    ,tcc.CustChannelName AS '客户类型'
    ,provice.AreaName AS '省',city.AreaName AS '市',ta.AreaName AS '县/区','' AS '镇/街道','' AS '村'
    ,tce.DeliveryAddr AS '客户地址'
    ,tce.CustContact AS '联系人'
    ,tce.MobilePhone  AS '联系电话'
    FROM dbo.T_CustomerBase tcb
    INNER JOIN dbo.T_CustomerExt tce ON tcb.CustID=tce.CustID
    INNER JOIN dbo.t_CompanyBranch cb ON tcb.CompBranchID=cb.CompBranchID
    INNER JOIN dbo.t_CustomerChannel tcc ON tcb.CustChannelID=tcc.CustChannelID
    INNER JOIN dbo.t_CustomerChannelType tcct ON tcc.CustChannelTypeID=tcct.CustChannelTypeID
    INNER JOIN dbo.t_Area ta ON tcb.AreaID=ta.AreaID AND ta.AreaLevel=3
    INNER JOIN dbo.t_Area city ON ta.ParentID =city.AreaID AND city.AreaLevel=2
    INNER JOIN dbo.t_Area provice ON city.ParentID=provice.AreaID AND provice.AreaLevel=1
    INNER JOIN dbo.t_Distributor td ON cb.DistributorID=td.DistributorID
    INNER JOIN dbo.t_DistributorContract tdc ON td.DistributorContractID=tdc.DistributorContractID
    INNER JOIN dbo.t_Org org ON tdc.OrgBranchID=org.OrgID
    WHERE org.OrgID=%s AND tcb.Disabled=0 
    UNION
    SELECT
    'KDS2' AS 来源系统
    ,cb.CompBranchCode_SAP '户头sap代码'
    ,cb.CompBranchName AS '户头名称'
    ,tcb.CustID
    ,CustCode AS '客户编码'
    ,CustName AS '客户名称'
    ,tcct.CustChannelTypeName AS '渠道类型'
    ,tcc.CustChannelName AS '客户类型'
    ,provice.AreaName AS '省',city.AreaName AS '市',county.AreaName AS '县/区',ta.AreaName AS '镇/街道','' AS '村'
    ,tce.DeliveryAddr AS '客户地址'
    ,tce.CustContact AS '联系人'
    ,tce.MobilePhone  AS '联系电话'
    FROM dbo.T_CustomerBase tcb
    INNER JOIN dbo.T_CustomerExt tce ON tcb.CustID=tce.CustID
    INNER JOIN dbo.t_CompanyBranch cb ON tcb.CompBranchID=cb.CompBranchID
    INNER JOIN dbo.t_CustomerChannel tcc ON tcb.CustChannelID=tcc.CustChannelID
    INNER JOIN dbo.t_CustomerChannelType tcct ON tcc.CustChannelTypeID=tcct.CustChannelTypeID
    INNER JOIN dbo.t_Area ta  ON tcb.AreaID=ta.AreaID AND ta.AreaLevel=4
    INNER JOIN dbo.t_Area county ON ta.ParentID=county.AreaID AND county.AreaLevel=3
    INNER JOIN dbo.t_Area city ON county.ParentID =city.AreaID AND city.AreaLevel=2
    INNER JOIN dbo.t_Area provice ON city.ParentID=provice.AreaID AND provice.AreaLevel=1
    INNER JOIN dbo.t_Distributor td ON cb.DistributorID=td.DistributorID
    INNER JOIN dbo.t_DistributorContract tdc ON td.DistributorContractID=tdc.DistributorContractID
    INNER JOIN dbo.t_Org org ON tdc.OrgBranchID=org.OrgID
    WHERE org.OrgID=%s AND tcb.Disabled=0 
    UNION
    SELECT
    'KDS2' AS 来源系统
    ,cb.CompBranchCode_SAP '户头sap代码'
    ,cb.CompBranchName AS '户头名称'
    ,tcb.CustID
    ,CustCode AS '客户编码'
    ,CustName AS '客户名称'
    ,tcct.CustChannelTypeName AS '渠道类型'
    ,tcc.CustChannelName AS '客户类型'
    ,provice.AreaName AS '省',city.AreaName AS '市',county.AreaName AS '县/区',town.AreaName AS '镇/街道',ta.AreaName AS '村'
    ,tce.DeliveryAddr AS '客户地址'
    ,tce.CustContact AS '联系人'
    ,tce.MobilePhone  AS '联系电话'
    FROM dbo.T_CustomerBase tcb
    INNER JOIN dbo.T_CustomerExt tce ON tcb.CustID=tce.CustID
    INNER JOIN dbo.t_CompanyBranch cb ON tcb.CompBranchID=cb.CompBranchID
    INNER JOIN dbo.t_CustomerChannel tcc ON tcb.CustChannelID=tcc.CustChannelID
    INNER JOIN dbo.t_CustomerChannelType tcct ON tcc.CustChannelTypeID=tcct.CustChannelTypeID
    INNER JOIN dbo.t_Area ta  ON tcb.AreaID=ta.AreaID AND ta.AreaLevel=5
    INNER JOIN dbo.t_Area  town  ON ta.ParentID=town.AreaID AND town.AreaLevel=4
    INNER JOIN dbo.t_Area county ON town.ParentID=county.AreaID AND county.AreaLevel=3
    INNER JOIN dbo.t_Area city ON county.ParentID =city.AreaID AND city.AreaLevel=2
    INNER JOIN dbo.t_Area provice ON city.ParentID=provice.AreaID AND provice.AreaLevel=1
    INNER JOIN dbo.t_Distributor td ON cb.DistributorID=td.DistributorID
    INNER JOIN dbo.t_DistributorContract tdc ON td.DistributorContractID=tdc.DistributorContractID
    INNER JOIN dbo.t_Org org ON tdc.OrgBranchID=org.OrgID
    WHERE org.OrgID=%s AND tcb.Disabled=0 
    ) temp
    ORDER BY temp.CustID ASC
    '''
        params = (orgID, orgID, orgID)
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



from threading import Thread
def async(func):
    def wrapper(*args, **kwargs):
        thr = Thread(target = func, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

@async
def exec(orgID,filePath):
    data = getCustomer(orgID)
    DataToExcel.write_to_excel_with_openpyxl(data["rows"], data["heads"], filepath=filePath, pageSize=10000)


def tasklet(row,basePath):
    orgID = getattr(row, 'OrgID')
    orgName = getattr(row, 'OrgName')
    filePath = basePath + "\\" + orgName + ".xlsx"
    exec(orgID, filePath)

def export():
    Orgs = getOrg()
    print(Orgs['effect_row'])
    df = Orgs["rows"]
    basePath = FileUtil.get_desktop() + "\\分公司数据\\"
    if dbType == DBType.MYSQL:
        basePath += "KDS3"
    elif dbType == DBType.SQLSERVER:
        basePath += "KDS2"
    FileUtil.mk_Path(basePath)
    import stackless as sl
    for row in df.itertuples(index=True, name='Pandas'):
        sl.tasklet(tasklet)(row,basePath)
    sl.run()



def main():
    export()
    # basePath = FileUtil.get_desktop()+"\\分公司数据\\"
    # data = DataToExcel.read_excel_with_openpyxl(basePath + "test.xlsx")
    # # data=DataToExcel.read_excel(basePath+"test.xls")
    # print(data.columns)
    # print(basePath)


if __name__ == '__main__':
    main()
