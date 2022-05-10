# superbsapi.h

```c
#ifndef _SUPER_BSAPI_H_
#define _SUPER_BSAPI_H_

#ifndef BOOST_PYTHON_STATIC_LIB
#define BOOST_PYTHON_STATIC_LIB
#endif
#include <iostream>
#include <string>
#include "bsapi.h"
#include <boost/python.hpp>

namespace superbsapi
{

class bshandle{
public:
	bshandle();
	~bshandle();
	BSHANDLE& getHandle();
	void setHandle(BSHANDLE hd);
	bool closeHandle();
	boost::python::object getObject();
public:
	BSHANDLE m_hd;
};

//chen::VariableData convert(boost::python::object obj);
//boost::python::object convert(chen::VariableData rv);

bool close_handle(boost::python::object& hHandle);
//bool close_table_handle(bshandle& hHandle);
void set_default_port(unsigned short uPort);
void set_default_timeout(int uTimeOut);
void set_netio_type(int nType);
int handle_keep_live(boost::python::object&hHandle);

int mq_query_all_names(boost::python::list& lst, const std::string& strHostName, unsigned short uPort);
boost::python::tuple mq_open( const char* sName, const char* sPWD, unsigned int uOpenFlag,
			   unsigned int uMQFlag, const char* sHostName, unsigned short uPort=0);
int mq_reopen(boost::python::object&hHandle, const std::string& sName,const std::string& sPWD,unsigned int uOpenFlag,
				 unsigned int uMQFlag);
boost::python::tuple mq_push_binary(boost::python::object&hHandle,const std::string& pData,const char *sLabel,
									unsigned char nLevel=BS_MQ_COMMONPRIORITY);
boost::python::tuple mq_push(boost::python::object&hHandle, boost::python::object& obj, int nType, const char *sLabel,
							 int nLevel=BS_MQ_COMMONPRIORITY);
boost::python::tuple mq_pop_binary(boost::python::object&hHandle, unsigned int nTimer = 0,bool isPeek=false);
boost::python::tuple mq_pop(boost::python::object&hHandle, int nTimer = 0,bool isPeek=false);
boost::python::tuple mq_length(boost::python::object&hHandle);
int mq_clear(boost::python::object&hHandle);
int mq_delete(boost::python::object&hHandle);

int treedb_create_newfile(const char *sDBFile,const char *sHostName,unsigned short uPort);
int treedb_create_newfile_ex(const char* sDBFile, const char* sConfigName, const char* sHostName, unsigned short uPort);
int treedb_query_mainkeys(boost::python::list& lst, const char *sDBFile,const char *sHostName,
							 unsigned short uPort);
//int treedb_open(boost::python::object&hHandle,const char *sMainKey,const char *sSubKeyPath,const char *sPWD,unsigned int uFlag,
//				   const char *sDBFile,const char *sHostName,unsigned short uPort);
int treedb_reopen(boost::python::object&hHandle,const char *sMainKey,const char *sSubKeyPath,const char *sPWD,unsigned int uFlag,
					 const char *sDBFile);
int treedb_open_subkey(boost::python::object&hHandle,const char *sSubKeyPath,unsigned int uFlag);
int treedb_begin_transaction(boost::python::object&hHandle);
int treedb_commit_transaction(boost::python::object&hHandle);
int treedb_rollback_transaction(boost::python::object&hHandle);
int treedb_insert_subkey(boost::python::object&hHandle,const char *sSubKey,unsigned int uFlag);
boost::python::tuple treedb_insert_subkey_name(boost::python::object& hHandle, unsigned int uFlag);
boost::python::tuple treedb_insert_subkey_and_create_index(boost::python::object& hHandle, const char* sSubKey, unsigned int uFlag, boost::python::list& lst);
int treedb_create_index(boost::python::object& hHandle, boost::python::list& lst);
int treedb_delete_index(boost::python::object& hHandle, boost::python::list& lst);
int treedb_get_index_names(boost::python::object& hHandle, boost::python::list& lst);
boost::python::tuple treedb_query_subkey_by_condition(boost::python::object& hHandle, boost::python::list& lst, const char* sExpression, boost::python::list& lResult, ui64 uLimitCount, ui64 uFrom);
boost::python::tuple treedb_query_subkey_by_condition_ex(boost::python::object& hHandle, boost::python::list& lst, const char* sExpression, boost::python::list& lResult, ui64 uLimitCount, ui64 uFrom
	, boost::python::str sOrderBy, bool isDesc);
boost::python::tuple treedb_delete_subkey_by_condition(boost::python::object& hHandle, boost::python::list& lst, const char* sExpression);
boost::python::tuple treedb_edit_property_by_condition(boost::python::object& hHandle, boost::python::list& lst, const char* sExpression, const char* sPropertyName, boost::python::object oValue, int nValueType);
boost::python::tuple treedb_calculate_by_contition(boost::python::object& hHandle, boost::python::list& lst, const char* sExpression, int nCalcType, const char* sPropertyName);
int treedb_get_properties(boost::python::object& hHandle, boost::python::list& lst, boost::python::dict& dictProp);
int treedb_get_subkey_properties(boost::python::object& hHandle, boost::python::list& lKeyList, boost::python::list& lPropList, boost::python::dict& dictProp);
int treedb_delete_subkey(boost::python::object&hHandle,const char *sSubKey);
int treedb_delete_key(boost::python::object&hHandle);
int treedb_rename_subkey(boost::python::object&hHandle, const char *sOldKeyName, const char *sNewKeyName);
int treedb_rename_key(boost::python::object&hHandle,const char *sNewKeyName);
int treedb_get_subkeys(boost::python::object&hHandle, boost::python::list& lst);
int treedb_insert_property_binary(boost::python::object&hHandle,const char *sPropertyName, const std::string& pBuf,bool bOverWrite);
boost::python::tuple treedb_get_property_binary(boost::python::object&hHandle,const char *sPropertyName);
int treedb_insert_property(boost::python::object&hHandle,const char *sPropertyName, const boost::python::object& obj, int nValueType, bool bOverWrite);
int treedb_insert_propertys(boost::python::object& hHandle, boost::python::list& lst, bool bOverWrite);
boost::python::tuple treedb_get_property(boost::python::object&hHandle, const char *sPropertyName);
int treedb_edit_property_binary(boost::python::object&hHandle,const char *sPropertyName,const std::string& pBuf);
int treedb_edit_property(boost::python::object&hHandle,const char *sPropertyName,const boost::python::object& obj, int nValueType);
int treedb_get_all_property_names(boost::python::object&hHandle, boost::python::list& lst);
int treedb_get_all_propertys(boost::python::object& hHandle, boost::python::dict& dictProp);
int treedb_get_all_propertys_and_type(boost::python::object& hHandle, boost::python::list& lstProp);
int treedb_delete_property(boost::python::object&hHandle,const char *sPropertyName);
int treedb_delete_all_property(boost::python::object&hHandle);
int treedb_rename_property(boost::python::object&hHandle,const char *sOldPropertyName,const char *sNewPropertyName);
//boost::python::tuple treedb_insert_key_and_properties(boost::python::object& hHandle, 
//	std::string& szKeyName, int nFlag, boost::python::list& lst, bool bOverWrite);
boost::python::tuple treedb_insert_key_and_properties(boost::python::object& hHandle,
	const char* szKeyName, int nFlag, boost::python::list& lst, bool bOverWrite);
//int treedb_insert(boost::python::object& hHandle, const char* sPropertyName);
int treedb_get_dyn(boost::python::object& hHandle, boost::python::dict& dyn);
int treedb_get_dyn_and_lastrd(boost::python::object& hHandle,
	boost::python::dict& dyn, boost::python::dict& dictRec);
int treedb_get_lastrd(boost::python::object& hHandle, const char* sNamePre, int nCount,
	boost::python::list& lstRecord);


//--------------tabledb---------------------------------------
int tabledb_get_all_dbnames(boost::python::list& DBNameList, const char* sHostName, unsigned short uPort);
boost::python::tuple tabledb_open( const char* sDBName, const char* sUser, const char* sPWD, unsigned int uOFlag,
	unsigned int uDBFlag, const char* sHostName, unsigned short uPort);
int tabledb_rename(const char* sDBName, const char* sNewDBName, const char* sUser, const char* sPWD,
	const char* sHostName, unsigned short uPort);
boost::python::tuple tabledb_qurey_handle(boost::python::object& hHandle);
int tabledb_reopen(boost::python::object& hHandle, const char* sDBName, const char* sUser, const char* sPWD, unsigned int uOFlag,
	unsigned int uDBFlag);
int tabledb_begin_transaction(boost::python::object& hHandle);
int tabledb_commit_transaction(boost::python::object& hHandle);
int tabledb_rollback_transaction(boost::python::object& hHandle);
int tabledb_create_table(boost::python::object& hHandle, const char* sTableName, boost::python::list& lFieldList,
	unsigned int uFlag);
int tabledb_get_all_tablenames(boost::python::object& hHandle, boost::python::list& tableNameList);
int tabledb_delete_table(boost::python::object& hHandle, const char* sTableName, unsigned short uType);
int tabledb_rename_table(boost::python::object& hHandle, const char* sTableName, const char* sNewName);
int tabledb_get_fields(boost::python::object& hHandle, const char* sTableName, boost::python::list& lFieldList);
//int tabledb_insert_record(bshandle& hHandle, const char* sTableName, boost::python::list& lRecordValueList);
//boost::python::tuple tabledb_update_record_by_field(bshandle& hHandle, const char* sTableName, boost::python::list& lFieldList,
//	boost::python::list& lRecordValueList, const char* sCondField, boost::python::object& vFValue, boost::python::object& pEndValue,
//	unsigned char uCondition, unsigned char uOpFlag);
//boost::python::tuple tabledb_delete_record_by_field(bshandle& hHandle, const char* sTableName, const char* sCondField,
//	boost::python::object& vFValue, boost::python::object& pEndValue, unsigned char uCondition, unsigned char uOpFlag);
boost::python::tuple tabledb_delete_record_by_ctime(boost::python::object& hHandle, const char* sTableName, __int64 tBeginTime, __int64 pEndTime,
	unsigned char uCondition, unsigned char uOpFlag);
boost::python::tuple tabledb_get_record(boost::python::object& hHandle, const char* sTableName, unsigned int uCount, boost::python::object& hRecordSet);

//boost::python::tuple tabledb_get_record_by_field(bshandle& hHandle, const char* sTableName, const char* sCondField, unsigned int FieldType,
//	boost::python::object& vFValue, boost::python::object& pEndValue, unsigned char uCondition, unsigned char uOpFlag, unsigned int uLimitCount, bshandle& hRecordSet);
boost::python::tuple tabledb_get_record_by_field(boost::python::object& hHandle, const char* sTableName,
	const char* sCondField, int FieldType, boost::python::object& vFValue,
	boost::python::object& pEndValue, boost::python::object uCondition, boost::python::object uOpFlag,
	int uLimitCount, boost::python::object& hRecordSet);

boost::python::tuple tabledb_recordset_info(boost::python::object& hRecordSet, boost::python::list& lFieldList);
int tabledb_get_cursor(boost::python::object& hRecordSet, boost::python::object& hCursor);
boost::python::tuple tabledb_cursor_next(boost::python::object& hCursor, boost::python::dict& fvMap);
boost::python::tuple tabledb_cursor_pre(boost::python::object& hCursor, boost::python::dict& fvMap);
int tabledb_cursor_reset(boost::python::object& hCursor);
//int tabledb_get_dyn(bshandle& hHandle, const char* sTableName, boost::python::dict& dyn);
int tabledb_get_dyn(boost::python::object& hHandle, const char* sTableName, boost::python::dict& dyn);
//int tabledb_get_dyn_and_lastrd(bshandle& hHandle, const char* sTableName, boost::python::dict& dyn, boost::python::dict& fvMap);
int tabledb_get_dyn_and_lastrd(boost::python::object& hHandle, const char* sTableName, boost::python::dict& dyn, boost::python::dict& fvMap);
int parse_alert_data(const std::string& pData, boost::python::dict& dyn, boost::python::dict& fvMap);
/*int tabledb_get_all_dyn_table_state(bshandle& hHandle, const char* sGroupName, boost::python::dict& nStateMap,
	boost::python::dict& sStateMap, bool isQuickMode);*/
int tabledb_get_all_dyn_table_state(boost::python::object& hHandle, const char* sGroupName, boost::python::dict& nStateMap,
	boost::python::dict& sStateMap, bool isQuickMode);
//--------------------------------mxhandle------------------------------------------

//int treedb_open_subkey_handle(unsigned __int64& myhandle, const char* sSubKeyPath, unsigned int uFlag);
int treedb_open_subkey_handle(boost::python::object& myhandle, const char* sSubKeyPath, unsigned int uFlag);
//int treedb_open_handle(boost::python::object& myhandle, const char* sMainKey, const char* sSubKeyPath, const char* sPWD, unsigned int uFlag, const char* sDBFile, const char* sHostName, unsigned short uPort);
boost::python::tuple treedb_open_handle(const char* sMainKey, const char* sSubKeyPath, const char* sPWD, unsigned int uFlag, const char* sDBFile, const char* sHostName, unsigned short uPort);


// ----------------------------------aes------------------------------
boost::python::tuple EnterData1(const char* data);
boost::python::tuple EnterData2(const char* data);
boost::python::tuple EnterData1_ex(const char* key, const char* data);
boost::python::tuple EnterData2_ex(const char* key, const char* data);
// -----------------------------------file ---------------------------------
int FileTransferSaveDBProperty(boost::python::object& hHandle, boost::python::str szProperty, boost::python::str szFilePath);
int DBPropertyTransferSaveFile(boost::python::object& hHandle, boost::python::str szProperty, boost::python::str szFilePath);
boost::python::tuple BinExport(boost::python::str szDbFile, boost::python::str szMainKey, boost::python::str szSubKeyPath);
boost::python::tuple BinImport(boost::python::str szDbFile, boost::python::str szMainKey, boost::python::str szSubKeyPath, boost::python::str szPath);
boost::python::str web_decrypt(boost::python::str sStr, boost::python::str sPwd);
}












#endif // _SUPER_BSAPI_H_
```
