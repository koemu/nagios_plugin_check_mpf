#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------
# check_mpf
# Major Page Faultの発生状況をチェックします
#
# Copyright(C) 2014 Yuichiro SAITO
# This software is released under the MIT License, see LICENSE.txt.
# ----------------------------------------------

import sys
import os
import time
import commands
import logging
import logging.config
from optparse import OptionParser

#-----------------------------------------------
# Global Variables
#-----------------------------------------------
LOG_FORMAT      = '%(levelname)s\t%(asctime)s\t%(name)s\t%(funcName)s\t"%(message)s"'
PROGRAM_VERSION = "0.0.1"


#-----------------------------------------------
# Private Class: _PageFault
#-----------------------------------------------
class _PageFault:
    """
    Private Class _PageFault
    """

    # クラス変数
    STATE_OK        = 0
    STATE_WARNING   = 1
    STATE_CRITICAL  = 2
    STATE_UNKNOWN   = 3
    STATE_DEPENDENT = 4

    #-----------------------------------------------

    def __init__( self, check_interval = 2 ):
        """
        Constractor
        """
        self.log = logging.getLogger( self.__class__.__name__ )

        self.log.debug( "START" )

        self.warning        = 0
        self.critical       = 0
        self.interval       = check_interval

        self.log.debug( "END" )

    #-----------------------------------------------

    def __del__( self ):
        """
        Destructor
        """
        self.log.debug( "START" )
        pass
        self.log.debug( "END" )

    #-----------------------------------------------

    def _printWarning( self, msg ):
        """
        Warningを出力し、返り値を設定します。
        """
        print "WARNING: %s" % msg
        
        return self.STATE_WARNING

    #-----------------------------------------------

    def _printCritical( self, msg ):
        """
        Criticalを出力し、返り値を設定します。
        """
        print "CRITICAL: %s" % msg
        
        return self.STATE_CRITICAL

    #-----------------------------------------------

    def _printUnknown( self, msg ):
        """
        Unknownを出力し、返り値を設定します。
        """
        print "UNKNOWN: %s" % msg
        
        return self.STATE_UNKNOWN

    #-----------------------------------------------

    def _getVmstat( self, proc_vmstat = None ):
        """
        /proc/vmstatを取得します
        @return 回数を返します
        """
        self.log.debug( "START" )

        if proc_vmstat is None:
            proc_vmstat = commands.getoutput( 'cat /proc/vmstat' )
        vmstat = self._parseVmstat( proc_vmstat )

        self.log.debug( "END" )

        return vmstat

    #-----------------------------------------------

    def _parseVmstat( self, vm_info ):
        """
        /proc/vmstat をパースします
        @param mem_info /proc/vmstatの内容を入力します
        @return dictにパースした状態を返します。なお、単位はKiBです。
        """
        self.log.debug( "START" )

        lines = vm_info.split( "\n" )
        result = {}

        for line in lines:
            columns = line.split( " " )
            result[ columns[0] ] = int( columns[1].strip() )
        self.log.debug( result )

        self.log.debug( "END" )

        return result

    #-----------------------------------------------

    def _isValidThreshold( self ):
        """
        閾値の関係に異常が無いかを評価します
        @return ステータスを返します
        """
        self.log.debug( "START" )

        if self.warning == 0 or self.critical == 0:
            # まだ値が設定されていないので評価しない
            pass
        elif self.warning > self.critical:
            return self._printUnknown( "Critical value should be more than warning value." )

        self.log.debug( "END" )

        return self.STATE_OK

    #-----------------------------------------------

    def setWarning( self, warning ):
        """
        warning値をセットします
        @param warning warning値をセットします
        """
        self.log.debug( "START" )

        self.warning = warning

        ret = self._isValidThreshold()
        if ret != self.STATE_OK:
            self.log.debug( "EXIT" )
            return ret

        self.log.debug( "END" )

        return self.STATE_OK

    #-----------------------------------------------

    def setCritical( self, critical ):
        """
        critical値をセットします
        @param critical critical値をセットします
        """
        self.log.debug( "START" )

        self.critical = critical

        ret = self._isValidThreshold()
        if ret != self.STATE_OK:
            self.log.debug( "EXIT" )
            return ret

        self.log.debug( "END" )

        return self.STATE_OK

    #-----------------------------------------------

    def checkMajorPageFaluts( self, before_proc = None, after_proc = None ):
        """
        閾値を評価します
        @return Nagiosの規則に沿った結果を返します
        """
        self.log.debug( "START" )

        # 評価
        before_vmstat = self._getVmstat( before_proc )
        time.sleep( self.interval )
        after_vmstat = self._getVmstat( after_proc )
        page_faults_per_sec = ( ( after_vmstat[ "pgmajfault" ] - before_vmstat[ "pgmajfault" ] ) * 1.0 ) / self.interval

        # 値で評価
        if self.critical > 0 and self.critical <= page_faults_per_sec:
            return self._printCritical( "Many major page faults occurred (%.2f faults/sec)." % page_faults_per_sec )
        elif self.warning > 0 and self.warning <= page_faults_per_sec:
            return self._printWarning( "Many major page faults occurred (%.2f faults/sec)." % page_faults_per_sec )

        print "OK (%.2f faults/sec)." % page_faults_per_sec

        self.log.debug( "END" )

        return self.STATE_OK


#-----------------------------------------------
# Main
#-----------------------------------------------

def main():
    """
    Main
    """

    # 引数のパース
    usage   = "Usage: %prog [option ...]"
    version ="%%prog %s\nCopyright (C) Yuichiro SAITO." % ( PROGRAM_VERSION )
    parser  = OptionParser( usage = usage, version = version )
    parser.add_option("-w", "--warning",
                      type="int",
                      dest="warning",
                      metavar="<pages>",
                      default=100,
                      help="Exit with WARNING status if more than major page faults per sec. Default value is 100.")
    parser.add_option("-c", "--critical",
                      type="int",
                      dest="critical",
                      metavar="<pages>",
                      default=1000,
                      help="Exit with CRITICAL status if more than major page faults per sec. Default value is 1000.")
    parser.add_option("-i", "--interval",
                      type="int",
                      dest="interval",
                      metavar="<seconds>",
                      default=2,
                      help="Check interval. Default value is 2 (sec).")
    parser.add_option("-V", "--verbose",
                      action="store_true",
                      dest="verbose",
                      default=False,
                      help="Verbose mode. (For debug only)")
    ( options, args ) = parser.parse_args()
    prog_name = parser.get_prog_name()

    if options.verbose:
        logging.basicConfig( level=logging.DEBUG, format = LOG_FORMAT )
    else:
        logging.basicConfig( level=logging.WARNING, format = LOG_FORMAT )

    logging.debug( "START" )

    # 評価を実施
    pf = _PageFault( options.interval )
    ret = pf.setWarning( options.warning )
    if ret != _PageFault.STATE_OK:
        logging.debug( "EXIT" )
        return ret
    ret = pf.setCritical( options.critical )
    if ret != _PageFault.STATE_OK:
        logging.debug( "EXIT" )
        return ret
    ret = pf.checkMajorPageFaluts()
    if ret != _PageFault.STATE_OK:
        logging.debug( "EXIT" )
        return ret

    logging.debug( "END" )

#-----------------------------------------------

if __name__ == '__main__':
    sys.exit( main() )

