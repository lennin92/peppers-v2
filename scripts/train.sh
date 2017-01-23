#!/usr/bin/env bash

DOWNLOAD_PATH=""
CSV_PATH=""
VAL_CSV_PATH=""
LMDB_PATH=""
RESIZE_HEIGHT=256
RESIZE_WIDTH=256
TOOLS=""
SOLVER=""


echo "Downloading images"
$(python download-dataset.py $CSV_PATH $VAL_CSV_PATH $DOWNLOAD_PATH )


echo "Creating train lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    --shuffle \
    $DOWNLOAD_PATH \
    $CSV_PATH \
    $LMDB_PATH/train_lmdb

echo "Creating validation lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    --shuffle \
    $DOWNLOAD_PATH \
    $VAL_CSV_PATH \
    $LMDB_PATH/val_lmdb


echo "Training network (Press Ctrl+C to finish)..."
GLOG_logtostderr=1 $TOOLS/caffe \
    train \
    --solver $SOLVER

echo "Done"