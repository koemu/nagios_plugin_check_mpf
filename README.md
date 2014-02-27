# check_mpf - Major page faults/sec check plugin for Nagios

- Copyright(C) 2014 Yuichiro SAITO (@koemu)

- This software is released under the MIT License, see LICENSE.txt.


## check_mpf とは？

ある時間(デフォルト:2秒)の間に発生した、Major Page Faults/s(以下、MPFs)の数を取得します。

その上で、一定以上のMPFsが発生したときに、Warning(デフォルト:100MPFs)またはCritical(でフォルト:1,000MPFs)を返します。

## なぜ Major Page Faults/s をチェックするのか？

アプリケーションがスワップアウトしたメモリページを読み込む際、Major Page Fault、すなわち二次記憶装置(HDD, SSD等)から物理メモリにページへロードする事象が発生します。これは、直接物理メモリからメモリページをロードする時よりも、何倍もコストがかかる処理となります。そのため、Major Page Faultが頻発するとCPUのiowaitが大きくなり、システム全体のパフォーマンスが劣化します。

そこで、MPFsをチェックする事で、パフォーマンス劣化の兆候を掴む事ができるようになります。

## Requirements

- OS: Linux Kernel 2.6.18 or above
- Python: 2.6 or 2.7

## Usage

- --version 本プログラムのバージョンを表示します。
- -h, --help コマンドラインのヘルプを表示します。
- -w \<pages\>, --warning=\<pages\> 指定した値以上のMPFsが発生した場合、Warningステータスを返します。デフォルトは100です。
- -c \<pages\>, --critical=\<pages\> 指定した値以上のMPFsが発生した場合、Criticalステータスを返します。デフォルトは1,000です。
- -i \<seconds\>, --interval=\<seconds\> MPFsをサンプリングする秒数を指定します。デフォルトは2秒です。
- -V, --verbose メッセージを詳細に表示します。デバッグ用です。

## changelog

* 2013-02 0.0.1 Initial release.

