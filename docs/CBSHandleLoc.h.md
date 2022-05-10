# CBSHandleLoc.h

```c
#pragma once
#ifndef BOOST_PYTHON_STATIC_LIB
#define BOOST_PYTHON_STATIC_LIB
#endif
#include <MxHandlePool.h>
#include <boost/python.hpp>
#include "../mxdbvar/DbVar.h"
#include "superbsapi.h"
namespace superbsapi
{

	class CBSHandleLoc
	{
	public:
		CBSHandleLoc();
		~CBSHandleLoc();

	public:
		//CConfHandle* GetConfHandle();
		//int GetHandleType();


		//定位到一个主键，再用Treedb_ReopenSubKey在该主键下移动到不同子键，对其他主键上子键的操作得先用该函数跳到其他主键
		//Alloc得到的一定是一个有效的handle
		int GetHandleSize();
		int Treedb_Alloc(boost::python::str szHost, boost::python::str szFile, boost::python::str szMainKey, boost::python::str szMainKeyPwd = "", int nOption = -1, int nPort = 0);
		int Treedb_AllocEx(boost::python::str szHost, boost::python::str szFile, boost::python::str szMainKey, boost::python::str szSubKeyPath = "", boost::python::str szMainKeyPwd = "", int nOption = -1, int nPort = 0,
			bool bCreateMainKeyIfNotExist = false, bool bCreateFileIfNotExist = false, bool bCreateSubkeyIfNotExist = false, int nSubKeyFlag = BS_TRDB_FLAG_INDEXNODE);
		//所有打开子键的操作都是用该函数
		int Treedb_ReopenSubKey(boost::python::str szSubKeyPath, int nOFlag );
		
		//内部调用Treedb_ReopenSubKey打开子键，如果打开到子键的路径上有些键不存在，则会创建到子键的路径，并最后将子键打开
		int Treedb_ReopenSubKeyEx(boost::python::str szSubKeyPath, int nOFlag , bool bCreateSubkeyIfNotExist );
		int Treedb_ReopenMainKey(boost::python::str szSubKeyPath, int nOFlag, bool bCreateSubkeyIfNotExist, 
			boost::python::str  szMainKey, boost::python::str  szMainKeyPwd, boost::python::str  szFile);
		int Treedb_BeginTransaction();
		int Treedb_RollbackTransaction();
		int Treedb_CommitTransaction();
		static int Treedb_CreateFile(boost::python::str szHost, boost::python::str szNewFile, int nPort = 0);
		static  int Treedb_CreateMainKey(boost::python::str szHost, boost::python::str szFile, boost::python::str szMainKey, boost::python::str szMainKeyPwd = "", int nPort = 0);
		static int Treedb_CreateMainKey_EX(boost::python::str szHost, boost::python::str szFile, boost::python::str szMainKey, int nFlag, boost::python::str szMainKeyPwd, int nPort);
		int Treedb_RenameMainKey(boost::python::str szHost, boost::python::str szFile, boost::python::str szOldMainKey, boost::python::str szNewMainKey, boost::python::str szMainKeyPwd = "", int nPort = 0);
		int Treedb_DeleteMainKey(boost::python::str szHost, boost::python::str szFile, boost::python::str szMainKey, boost::python::str szMainKeyPwd = "", int nPort = 0);
		//获取所有主键名不需要handle，调用该函数之前不需要Alloc
		static int Treedb_GetAllMainKeyNames(boost::python::list& lstMainKeyNames, boost::python::str szHost, boost::python::str szFile, int nPort = 0);
		//int Treedb_OpenSubKey(boost::python::str szSubKeyPath,int nFlag=TRDB_OPKF_OPENEXIST);
		//直接在当前handle指向的键下面添加子键,若szSubKeyName为空，则数据库生成子键名通过szSubKeyName返回，否则用给出的子键名创建子键
		boost::python::tuple Treedb_InsertSubKey(boost::python::str szSubKeyName, int nFlag = BS_TRDB_FLAG_INDEXNODE);
		//先打开父键，再插入子键,若szNewSubKey为空，则数据库生成子键名通过szNewSubKey返回，否则用给出的子键名创建子键
		boost::python::tuple Treedb_AppendSubKey(boost::python::str szParentKeyPath, boost::python::str szNewSubKey, int nFlag = BS_TRDB_FLAG_INDEXNODE);
		int Treedb_DeleteSubKey(boost::python::str szSubKeyName);
		int Treedb_DeleteThisKey();
		int Treedb_QueryHandle(boost::python::str szMainKey, boost::python::str szSubKeyPath, boost::python::str szServer, unsigned int uFlag, boost::python::str szDFBFile, unsigned int uPort);
		int Treedb_RenameSubKey(boost::python::str szOldSubKeyName, boost::python::str szNewSubKeyName);
		//更改句柄指向键的名称(注意：不能更改主键)
		int Treedb_RenameThisKey(boost::python::str szNewKeyName);
		int Treedb_GetAllSubKeys(boost::python::list& lstSubKeys);
		//int Treedb_InsertProperty(boost::python::str szPropName, chen::VariableData& vData);
		//int Treedb_GetProperty(boost::python::str szPropName, chen::VariableData& vData);
		int Treedb_GetPropertyInt(boost::python::str szPropName, int nDefault);//返回结果为取得的int型属性
		boost::python::str Treedb_GetPropertyString(boost::python::str szPropName, boost::python::str szDefault);
		__int64 Treedb_GetPropertyInt64(boost::python::str szPropName, __int64 nDefault);
		float Treedb_GetPropertyFloat(boost::python::str szPropName, float fDefault);
		double Treedb_GetPropertyDouble(boost::python::str szPropName, double dDefault);
		int Treedb_EditProperty(boost::python::str szPropName, chen::VariableData& vData);
		int Treedb_GetAllPropertyNames(boost::python::list& lstPropNames);
		int Treedb_DeleteProperty(boost::python::str szPropName);
		int Treedb_DeleteAllProperty();
		int Treedb_RenameProperty(boost::python::str szOldPropName, boost::python::str szNewPropName);
		int Treedb_WriteKeyString(boost::python::str szPropName, boost::python::str szPropValue);
		int Treedb_WriteKeyInt(boost::python::str szPropName, int nPropValue);
		int Treedb_WriteKeyInt64(boost::python::str szPropName, __int64 n64PropValue);
		int Treedb_WriteKeyDouble(boost::python::str szPropName, double nPropValue);
		int Treedb_WriteKeyVariable(boost::python::str szPropName, boost::python::object obj, int FieldType);
		//int Treedb_SelectKeyPropertys(BSPROPERTYSET& lstProp);
		int Treedb_SelectKeyPropertys(boost::python::dict& lstProp);
		int Treedb_WriteMap(boost::python::dict& mapWrite);
		int Treedb_InsertProperty(boost::python::str szPropName, boost::python::object obj, int FieldType);
		boost::python::tuple Treedb_GetProperty(boost::python::str szPropName);
		boost::python::tuple Treedb_Query_Subkey_By_Condition(boost::python::list& lst, const char* sExpression, boost::python::list& lResult, ui64 uLimitCount, ui64 uFrom);
		//boost::python::object getObject();
		void GetBSHandle(bshandle& handle );
		boost::python::object GetConfHandle();

	public: //table
		int Tabledb_Alloc(boost::python::str szHost, boost::python::str szDbName, int nPort);
		int Tabledb_AllocEx(boost::python::str szHost, boost::python::str szDbName, int nPort, int nOpFlag, unsigned int uDBFlag);
		boost::python::tuple Tabledb_SelectRecordsByField(boost::python::str szTableName, ui32 uLimitCount, boost::python::str szField, int nCondition, boost::python::list& lCondi, boost::python::list& lResult);
		boost::python::tuple Tabledb_SelectRecords(boost::python::str szTableName, ui32 uLimitCount, boost::python::list& lResult);
		boost::python::tuple Tabledb_SelectRecordsByCTime(boost::python::str szTableName, ui32 uLimitCount, __int64 tBegin, __int64 tEnd, boost::python::list& lResult);
		boost::python::tuple Tabledb_Query(boost::python::str szSQL, boost::python::list& lResult);
		int Tabledb_ReopenDb(boost::python::str szDbName);
	public:
		CMxHandleLoc m_hd;

	};

}
```
