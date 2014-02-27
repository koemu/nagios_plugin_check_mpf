# -*- coding: utf-8 -*-

# ----------------------------------------------
# test_check_mpf.py
#
# Copyright(C) 2014 Yuichiro SAITO
# This software is released under the MIT License, see LICENSE.txt.
# ----------------------------------------------

import unittest
from check_mpf import _PageFault


#-----------------------------------------------

class TestSequenceFunctions(unittest.TestCase):

    #-----------------------------------------------

    def setUp( self ):
        self.pf_before = "pgmajfault 0"
        self.pf_after  = "pgmajfault 200"
        pass

    #-----------------------------------------------

    def test_paramCheck_OK_1( self ):
        """
        矛盾しないチェック
        """
        pf = _PageFault()
        ret = pf.setWarning( 10 )
        self.assertEqual( ret, _PageFault.STATE_OK )
        ret = pf.setCritical( 100 )
        self.assertEqual( ret, _PageFault.STATE_OK )

    #-----------------------------------------------

    def test_paramCheck_Unknown_1( self ):
        """
        矛盾チェック %
        """
        pf = _PageFault()
        ret = pf.setWarning( 100 )
        self.assertEqual( ret, _PageFault.STATE_OK )
        ret = pf.setCritical( 10 )
        self.assertEqual( ret, _PageFault.STATE_UNKNOWN )

    #-----------------------------------------------

    def test_paramCheck_Unknown_2( self ):
        """
        矛盾チェック %
        """
        pf = _PageFault()
        ret = pf.setCritical( 10 )
        self.assertEqual( ret, _PageFault.STATE_OK )
        ret = pf.setWarning( 100 )
        self.assertEqual( ret, _PageFault.STATE_UNKNOWN )

    #-----------------------------------------------

    def test_validCheck_OK_1( self ):
        """
        バリデーション 正常チェック
        """
        pf = _PageFault()
        pf.setCritical( 1000 )
        pf.setWarning( 101 )
        self.assertEqual( pf.checkMajorPageFaluts( self.pf_before, self.pf_after ), _PageFault.STATE_OK )

    #-----------------------------------------------

    def test_validCheck_Warning( self ):
        """
        バリデーション Warningチェック
        """
        pf = _PageFault()
        pf.setCritical( 1000 )
        pf.setWarning( 100 )
        self.assertEqual( pf.checkMajorPageFaluts( self.pf_before, self.pf_after ), _PageFault.STATE_WARNING )

    #-----------------------------------------------

    def test_validCheck_Critical( self ):
        """
        バリデーション Criticalチェック
        """
        pf = _PageFault()
        pf.setCritical( 100 )
        pf.setWarning( 10 )
        self.assertEqual( pf.checkMajorPageFaluts( self.pf_before, self.pf_after ), _PageFault.STATE_CRITICAL )

    #-----------------------------------------------

    def test_validCheck_WarningOnly( self ):
        """
        バリデーション Warning Onlyチェック
        """
        pf = _PageFault()
        pf.setWarning( 100 )
        self.assertEqual( pf.checkMajorPageFaluts( self.pf_before, self.pf_after ), _PageFault.STATE_WARNING )

    #-----------------------------------------------

    def test_validCheck_CriticalOnly( self ):
        """
        バリデーション Critical Onlyチェック
        """
        pf = _PageFault()
        pf.setCritical( 100 )
        self.assertEqual( pf.checkMajorPageFaluts( self.pf_before, self.pf_after ), _PageFault.STATE_CRITICAL )

    #-----------------------------------------------
        
    #-----------------------------------------------

#-----------------------------------------------

if __name__ == '__main__':
    unittest.main()

#-----------------------------------------------
