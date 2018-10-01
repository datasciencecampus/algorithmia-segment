#!/bin/bash
################################################################################
# Segmentation demo                                                            #
# ============================================================================ #
# ./run_all.sh                                                                 #
#                                                                              #
# Phil Stubbings, ONS Data Science Campus.                                     #
################################################################################

python3 example.py $KEY $SERVER test_images \
  "data://.my/test_images" "data://.algo/nocturne/segment/temp" result
python3 visualise.py test_images result visualise
