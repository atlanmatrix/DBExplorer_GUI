# -*- coding: utf_8 -*-
import json
from mxsoft import *
from bsmiddle import *


def SendInfoToWeb(pSession, strRet, bChunk=False, nChunkTime=0, szContentType="text/html"):
    """
    :param LPWEINFO pSession:
    :param str strRet:
    :param bChunk:
    :param nChunkTime:
    :param szContentType:
    :return:
    """
    if None == pSession:
        print("Error Param : pSession = None !")
        return WE_MR.WE_MR_OK
    szTemp = strRet
    len_ = len(szTemp)
    if bChunk:
        if 0 == nChunkTime:
            HttpResponseHead = pSession.GetHttpResponseHead()
            HttpResponseHead.SetStatus(Http_respone_status.st_200_ok)
            HttpResponseHead.SetStatusDescription("OK")
            HttpResponseHead.SetContentType("text/event-stream")
            HttpResponseHead.SetTransferEncoding_Chunked()
            pSession.SendHeader()
        if -1 == nChunkTime:
            pSession.SendChunked(szTemp, 3)
        else:
            pSession.SendChunked(szTemp, 2)
    else:
        HttpResponseHead = pSession.GetHttpResponseHead()
        HttpResponseHead.SetStatus(Http_respone_status.st_200_ok)
        HttpResponseHead.SetStatusDescription("OK")
        szContentType += ";charset=UTF-8"
        HttpResponseHead.SetContentType(szContentType)
        if len_ > 0:
            if len_ > 1000:
                #  szTemp_ = bytes(szTemp,encoding='utf-8')
                pData = bytes(szTemp, encoding='utf-8')

                #  pData = pSession.CompressData(szTemp_, Http_content_encoding.ce_gzip)
                HttpResponseHead.SetContentLength(len(pData))
                #  HttpResponseHead.SetContentEncoding(Http_content_encoding.ce_gzip)
                pSession.SendHeader()
                pSession.SendData(pData)
            else:
                pData = bytes(szTemp, encoding='utf-8')
                len_ = len(pData)
                HttpResponseHead.SetContentLength(len_)
                pSession.SendHeader()
                pSession.SendData(szTemp)

    return WE_MR.WE_MR_OK


def SendSessionOutInfoToWebSession(pSession, callbackparam):
    """
    :param LPWEINFO pSession:
    :param str callbackparam:
    :return:
    """
    if None == pSession:
        print("Error Param : pSession = None !")
        return
    objetct = {"status": "SessionTimeOut"}
    stroutstring = json.dumps(objetct)
    if callbackparam != "":
        tempstr = callbackparam
        tempstr += "("
        tempstr += stroutstring
        tempstr += ")"
        stroutstring = tempstr

    SendInfoToWeb(pSession, stroutstring)


def SendInfoToWebBINHEX(pSession, pData, nLen):
    """
    :param LPWEINFO pSession:
    :param str pData:
    :param int nLen:
    :return:
    """
    if None == pSession:
        print("Error Param : pSession = None !")
        return WE_MR.WE_MR_OK

    if None == pData:
        print("Error Param : pData = None !")
        return WE_MR.WE_MR_OK

    HttpResponseHead = pSession.GetHttpResponseHead()
    HttpResponseHead.SetStatus(Http_respone_status.st_200_ok)
    HttpResponseHead.SetStatusDescription("OK")
    HttpResponseHead.SetContentType("application/mac-binhex40")
    HttpResponseHead.SetContentLength(nLen)
    pSession.SendHeader()
    pSession.SendData(pData)

    return WE_MR.WE_MR_OK


def SendInfoToWebExport(pSession, pData, fileName):
    """
    浏览器窗口下载
    :param pSession:
    :param pData:
    :return:
    """
    if None == pSession:
        print("Error Param : pSession = None !")
        return WE_MR.WE_MR_OK

    if None == pData:
        print("Error Param : pData = None !")
        return WE_MR.WE_MR_OK
    nLen = len(pData)
    HttpResponseHead = pSession.GetHttpResponseHead()
    HttpResponseHead.SetStatus(Http_respone_status.st_200_ok)
    HttpResponseHead.SetAddHead('Content-Transfer-Encoding', 'binary')
    HttpResponseHead.SetAddHead('Content-Type', 'application/force-download')
    HttpResponseHead.SetAddHead('Content-Type', 'application/octet-stream')
    HttpResponseHead.SetAddHead('Content-Type', 'application/download')
    HttpResponseHead.SetAddHead('Content-Disposition', 'inline;filename=' + fileName)
    HttpResponseHead.SetAddHead('Content-Transfer-Encoding', 'binary')
    HttpResponseHead.SetAddHead('Cache-Control', 'must-revalidate, post-check=0, pre-check=0')
    HttpResponseHead.SetAddHead('Pragma', 'no-cache')
    HttpResponseHead.SetStatusDescription("OK")
    HttpResponseHead.SetContentLength(nLen)
    pSession.SendHeader()
    pSession.SendData(pData)
    return WE_MR.WE_MR_OK


def SendErrorWebSession(pSession, szStatus, strError, callbackparam):
    """
    :param LPWEINFO pSession:
    :param str szStatus:
    :param str strError:
    :param str callbackparam:
    :return:
    """
    if None == pSession:
        print("Error Param : pSession = None !")
        return WE_MR.WE_MR_OK
    if szStatus == "":
        szStatus = "failed"
    objetct = {"status": szStatus, "errmsg": strError}
    stroutstring = json.dumps(objetct)
    if callbackparam != "":
        tempstr = callbackparam
        tempstr += "("
        tempstr += stroutstring
        tempstr += ")"
        stroutstring = tempstr

    return SendInfoToWeb(pSession, stroutstring)


def SendErrorAndShowErrorWebSessionInt(pSession, nRet, strError, szShowMsg, callbackparam):
    """
    :param LPWEINFO pSession:
    :param int nRet:
    :param str strError:
    :param str szShowMsg:
    :param str callbackparam:
    :return:
    """
    if None == pSession:
        print("Error Param : pSession = None !")
        return WE_MR.WE_MR_OK
    if 0 == nRet:
        szStatus = "success"
    else:
        szStatus = str(nRet)

    objetct = {
        "status": szStatus,
        "errmsg": strError,
        "showmsg": szShowMsg
    }
    stroutstring = json.dumps(objetct)
    if callbackparam != "":
        tempstr = callbackparam
        tempstr += "("
        tempstr += stroutstring
        tempstr += ")"
        stroutstring = tempstr

    return SendInfoToWeb(pSession, stroutstring)


def SendErrorAndShowErrorWebSessionStr(pSession, szStatus, strError, szShowMsg, callbackparam):
    """
    :param LPWEINFO pSession:
    :param str szStatus:
    :param str strError:
    :param str szShowMsg:
    :param str callbackparam:
    :return:
    """
    if None == pSession:
        print("Error Param : pSession = None !")
        return WE_MR.WE_MR_OK
    if szStatus == "":
        szStatus = "failed"
    objetct = {
        "status": szStatus,
        "errmsg": strError,
        "showmsg": szShowMsg
    }

    stroutstring = json.dumps(objetct)
    if callbackparam != "":
        tempstr = callbackparam
        tempstr += "("
        tempstr += stroutstring
        tempstr += ")"
        stroutstring = tempstr

    return SendInfoToWeb(pSession, stroutstring)


def SendSuccessWebSession(pSession, szStatus, strError, jData, callbackparam):
    """
    :param LPWEINFO pSession:
    :param str szStatus:
    :param str strError:
    :param dict|list jData:
    :param str callbackparam:
    :return:
    """
    if None == pSession:
        print("Error Param : pSession = None !")
        return WE_MR.WE_MR_OK
    if szStatus == "":
        szStatus = "failed"

    objetct = {
        "status": szStatus,
        "errmsg": strError,
        "showmsg": jData
    }

    stroutstring = json.dumps(objetct)
    if callbackparam != "":
        tempstr = callbackparam
        tempstr += "("
        tempstr += stroutstring
        tempstr += ")"
        stroutstring = tempstr

    return SendInfoToWeb(pSession, stroutstring)


def SendInfoToWebWithCallback(pSession, strCallback, strRet, bChunk=False, nChunkTime=0):
    """
    :param LPWEINFO pSession:
    :param str strCallback:
    :param str strRet:
    :param bool bChunk:
    :param int nChunkTime:
    :return int:
    """
    strCallback.strip()
    stroutstring = strRet
    if strCallback != "":
        tempstr = strCallback
        tempstr += "("
        tempstr += stroutstring
        tempstr += ")"
        stroutstring = tempstr

    return SendInfoToWeb(pSession, stroutstring, bChunk, nChunkTime)
