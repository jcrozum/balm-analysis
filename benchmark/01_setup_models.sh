#!/bin/bash

# Start moving model files into the benchmark folder for further testing.

rm -rf models-easy
mkdir models-easy
mkdir models-easy/bbm-random
mkdir models-easy/random-nk2
mkdir models-easy/random-nk3
mkdir models-easy/random-ncf

rm -rf models-hard
mkdir models-hard
mkdir models-hard/bbm-random
mkdir models-hard/random-nk2
mkdir models-hard/random-nk3
mkdir models-hard/random-ncf
mkdir models-hard/random-dense

# BBM models 002, 004, 079, 083, 143, 145, 146, 151, 191, 192, 197, 204, 209, 210, and 211 are considered "hard".
cp ../models/bbm-bnet-inputs-random-128/002* models-hard/bbm-random
cp ../models/bbm-bnet-inputs-random-128/004* models-hard/bbm-random
cp ../models/bbm-bnet-inputs-random-128/079* models-hard/bbm-random
cp ../models/bbm-bnet-inputs-random-128/083* models-hard/bbm-random
cp ../models/bbm-bnet-inputs-random-128/143* models-hard/bbm-random
cp ../models/bbm-bnet-inputs-random-128/145* models-hard/bbm-random
cp ../models/bbm-bnet-inputs-random-128/146* models-hard/bbm-random
cp ../models/bbm-bnet-inputs-random-128/151* models-hard/bbm-random
cp ../models/bbm-bnet-inputs-random-128/191* models-hard/bbm-random
cp ../models/bbm-bnet-inputs-random-128/192* models-hard/bbm-random
cp ../models/bbm-bnet-inputs-random-128/197* models-hard/bbm-random
cp ../models/bbm-bnet-inputs-random-128/204* models-hard/bbm-random
cp ../models/bbm-bnet-inputs-random-128/209* models-hard/bbm-random
cp ../models/bbm-bnet-inputs-random-128/210* models-hard/bbm-random
cp ../models/bbm-bnet-inputs-random-128/211* models-hard/bbm-random

# Other BBM models are "easy".
cp ../models/bbm-bnet-inputs-random-128/* models-easy/bbm-random
rm models-easy/bbm-random/002*
rm models-easy/bbm-random/004*
rm models-easy/bbm-random/079*
rm models-easy/bbm-random/083*
rm models-easy/bbm-random/143*
rm models-easy/bbm-random/144* # Model 144 is completely ignored.
rm models-easy/bbm-random/145*
rm models-easy/bbm-random/146*
rm models-easy/bbm-random/151*
rm models-easy/bbm-random/191*
rm models-easy/bbm-random/192*
rm models-easy/bbm-random/197*
rm models-easy/bbm-random/204*
rm models-easy/bbm-random/209*
rm models-easy/bbm-random/210*
rm models-easy/bbm-random/211*

# Random models are considered easy if they have less than 160 variables.

cp ../models/random_nk2/n10_* models-easy/random-nk2
cp ../models/random_nk2/n20_* models-easy/random-nk2
cp ../models/random_nk2/n40_* models-easy/random-nk2
cp ../models/random_nk2/n80_* models-easy/random-nk2
cp ../models/random_nk2/n160_* models-hard/random-nk2
cp ../models/random_nk2/n320_* models-hard/random-nk2
cp ../models/random_nk2/n640_* models-hard/random-nk2
cp ../models/random_nk2/n1280_* models-hard/random-nk2
cp ../models/random_nk2/n2560_* models-hard/random-nk2

cp ../models/random_nk3/n10_* models-easy/random-nk3
cp ../models/random_nk3/n20_* models-easy/random-nk3
cp ../models/random_nk3/n40_* models-easy/random-nk3
cp ../models/random_nk3/n80_* models-easy/random-nk3
cp ../models/random_nk3/n160_* models-hard/random-nk3
cp ../models/random_nk3/n320_* models-hard/random-nk3
cp ../models/random_nk3/n640_* models-hard/random-nk3
cp ../models/random_nk3/n1280_* models-hard/random-nk3
cp ../models/random_nk3/n2560_* models-hard/random-nk3

cp ../models/random_ncf/n10_* models-easy/random-ncf
cp ../models/random_ncf/n20_* models-easy/random-ncf
cp ../models/random_ncf/n40_* models-easy/random-ncf
cp ../models/random_ncf/n80_* models-easy/random-ncf
cp ../models/random_ncf/n160_* models-hard/random-ncf
cp ../models/random_ncf/n320_* models-hard/random-ncf
cp ../models/random_ncf/n640_* models-hard/random-ncf
cp ../models/random_ncf/n1280_* models-hard/random-ncf
cp ../models/random_ncf/n2560_* models-hard/random-ncf

# All dense models are hard.
cp ../models/random_dense/* models-hard/random-dense