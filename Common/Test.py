from Common.DB.DataAccess import DataAccess, dbType
from Common.DB.EnumType import DBType

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

def main():
    print("dfasdfsa")
    import stackless as sl
    sl.tasklet(print)("fgsdfgds")
    sl.run()
    getOrg()

if __name__ == '__main__':
    main()