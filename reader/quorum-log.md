#quorum raft

three times 1000 transactions:
```
./tps.py 
versions: web3 4.2.0, py-solc: 2.1.0, solc 0.4.23+commit.124ca40d.Linux.gpp, testrpc 1.3.4, python 3.5.3 (default, Jan 19 2017, 14:11:04) [GCC 6.3.0 20170118]

Block  1  - waiting for something to happen

starting timer, at block 2 which has  1  transactions; at timecode 683.352769367
block 2 | new #TX   1 /   40 ms =  24.8 TPS_current | total: #TX    2 /  0.1 s =  17.6 TPS_average
block 3 | new #TX  51 /  436 ms = 117.0 TPS_current | total: #TX   53 /  0.6 s =  93.9 TPS_average
block 12 | new #TX  50 /  301 ms = 166.0 TPS_current | total: #TX  103 /  1.0 s = 105.1 TPS_average
block 18 | new #TX  62 /  355 ms = 174.8 TPS_current | total: #TX  165 /  1.4 s = 114.5 TPS_average
block 25 | new #TX  53 /  297 ms = 178.5 TPS_current | total: #TX  218 /  1.9 s = 116.4 TPS_average
block 31 | new #TX  58 /  347 ms = 167.0 TPS_current | total: #TX  276 /  2.3 s = 118.5 TPS_average
block 38 | new #TX  38 /  250 ms = 151.9 TPS_current | total: #TX  314 /  2.8 s = 113.1 TPS_average
block 42 | new #TX  53 /  301 ms = 176.2 TPS_current | total: #TX  367 /  3.2 s = 113.3 TPS_average
block 48 | new #TX  67 /  450 ms = 148.9 TPS_current | total: #TX  434 /  3.7 s = 118.2 TPS_average
block 56 | new #TX  59 /  349 ms = 169.2 TPS_current | total: #TX  493 /  4.1 s = 119.3 TPS_average
block 62 | new #TX  92 /  502 ms = 183.1 TPS_current | total: #TX  585 /  4.6 s = 126.4 TPS_average
block 72 | new #TX  63 /  398 ms = 158.4 TPS_current | total: #TX  648 /  5.1 s = 127.5 TPS_average
block 80 | new #TX  52 /  300 ms = 173.3 TPS_current | total: #TX  700 /  5.5 s = 126.2 TPS_average
block 86 | new #TX  51 /  376 ms = 135.6 TPS_current | total: #TX  751 /  6.0 s = 125.4 TPS_average
block 92 | new #TX 118 /  688 ms = 171.5 TPS_current | total: #TX  869 /  6.4 s = 135.4 TPS_average
block 106 | new #TX 131 /  738 ms = 177.6 TPS_current | total: #TX 1000 /  6.8 s = 146.3 TPS_average
^C KeyboardInterrupt


./tps.py 
versions: web3 4.2.0, py-solc: 2.1.0, solc 0.4.23+commit.124ca40d.Linux.gpp, testrpc 1.3.4, python 3.5.3 (default, Jan 19 2017, 14:11:04) [GCC 6.3.0 20170118]

Block  121  - waiting for something to happen

starting timer, at block 122 which has  1  transactions; at timecode 731.732917924
block 122 | new #TX   4 /   65 ms =  61.2 TPS_current | total: #TX    5 /  0.1 s =  54.4 TPS_average
block 124 | new #TX  66 /  330 ms = 200.1 TPS_current | total: #TX   71 /  0.6 s = 124.7 TPS_average
block 130 | new #TX  52 /  341 ms = 152.5 TPS_current | total: #TX  123 /  1.0 s = 125.0 TPS_average
block 137 | new #TX  34 /  178 ms = 190.6 TPS_current | total: #TX  157 /  1.5 s = 106.7 TPS_average
block 141 | new #TX  78 /  452 ms = 172.8 TPS_current | total: #TX  235 /  1.9 s = 122.9 TPS_average
block 150 | new #TX  62 /  349 ms = 177.5 TPS_current | total: #TX  297 /  2.4 s = 125.0 TPS_average
block 157 | new #TX  66 /  404 ms = 163.4 TPS_current | total: #TX  363 /  2.8 s = 127.4 TPS_average
block 165 | new #TX  42 /  246 ms = 170.9 TPS_current | total: #TX  405 /  3.3 s = 123.5 TPS_average
block 170 | new #TX  52 /  299 ms = 173.9 TPS_current | total: #TX  457 /  3.7 s = 123.3 TPS_average
block 175 | new #TX  79 /  512 ms = 154.3 TPS_current | total: #TX  536 /  4.1 s = 129.5 TPS_average
block 184 | new #TX  69 /  402 ms = 171.5 TPS_current | total: #TX  605 /  4.6 s = 131.5 TPS_average
block 192 | new #TX  78 /  448 ms = 174.0 TPS_current | total: #TX  683 /  5.1 s = 135.1 TPS_average
block 201 | new #TX  45 /  288 ms = 156.5 TPS_current | total: #TX  728 /  5.5 s = 132.8 TPS_average
block 207 | new #TX  68 /  401 ms = 169.4 TPS_current | total: #TX  796 /  5.9 s = 135.0 TPS_average
block 215 | new #TX 166 /  999 ms = 166.2 TPS_current | total: #TX  962 /  6.3 s = 151.7 TPS_average
block 234 | new #TX  38 /  307 ms = 123.8 TPS_current | total: #TX 1000 /  6.8 s = 148.0 TPS_average
^C KeyboardInterrupt


./tps.py 
versions: web3 4.2.0, py-solc: 2.1.0, solc 0.4.23+commit.124ca40d.Linux.gpp, testrpc 1.3.4, python 3.5.3 (default, Jan 19 2017, 14:11:04) [GCC 6.3.0 20170118]

Block  240  - waiting for something to happen

starting timer, at block 241 which has  2  transactions; at timecode 747.124872259
block 241 | new #TX   8 /   46 ms = 174.5 TPS_current | total: #TX   10 /  0.1 s =  71.3 TPS_average
block 242 | new #TX  62 /  356 ms = 174.4 TPS_current | total: #TX   72 /  0.6 s = 125.8 TPS_average
block 249 | new #TX  35 /  243 ms = 143.8 TPS_current | total: #TX  107 /  1.0 s = 103.3 TPS_average
block 254 | new #TX  67 /  408 ms = 164.4 TPS_current | total: #TX  174 /  1.5 s = 119.4 TPS_average
block 261 | new #TX  74 /  392 ms = 188.6 TPS_current | total: #TX  248 /  1.9 s = 131.9 TPS_average
block 268 | new #TX  90 /  602 ms = 149.6 TPS_current | total: #TX  338 /  2.4 s = 140.8 TPS_average
block 280 | new #TX  69 /  353 ms = 195.5 TPS_current | total: #TX  407 /  2.9 s = 142.7 TPS_average
block 287 | new #TX  48 /  256 ms = 187.3 TPS_current | total: #TX  455 /  3.3 s = 139.2 TPS_average
block 292 | new #TX  48 /  293 ms = 164.0 TPS_current | total: #TX  503 /  3.7 s = 135.9 TPS_average
block 298 | new #TX  40 /  247 ms = 162.1 TPS_current | total: #TX  543 /  4.1 s = 131.8 TPS_average
block 303 | new #TX  43 /  250 ms = 171.8 TPS_current | total: #TX  586 /  4.5 s = 129.2 TPS_average
block 308 | new #TX  78 /  451 ms = 173.0 TPS_current | total: #TX  664 /  5.0 s = 132.9 TPS_average
block 317 | new #TX  48 /  299 ms = 160.8 TPS_current | total: #TX  712 /  5.4 s = 131.3 TPS_average
block 323 | new #TX 119 /  751 ms = 158.4 TPS_current | total: #TX  831 /  6.0 s = 139.5 TPS_average
block 338 | new #TX 146 /  899 ms = 162.4 TPS_current | total: #TX  977 /  6.4 s = 152.9 TPS_average
block 356 | new #TX  23 /   51 ms = 447.4 TPS_current | total: #TX 1000 /  6.8 s = 146.9 TPS_average

```


