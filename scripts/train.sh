#!/usr/bin/env bash

DOWNLOAD_PATH=""    # Direccion de carpeta donde se descargaran los PNG
CSV_PATH=""         # Direccion donde se guardara el csv para entrenar
VAL_CSV_PATH=""     # Direccion donde se guardara el csv de validacion
LMDB_PATH=""        # Direccion donde se almacenara el archivo lmdb
RESIZE_HEIGHT=256   # Cambio de altura (poner 0 para no cambiar)
RESIZE_WIDTH=256    # Cambio de anchura (poner 0 para no cambiar)
TOOLS=""            # Direcion donde estan los ejecutables de caffe
SOLVER=""           # Direccion del solver.prototxt (archivo de parametros de entrenamiento)


echo "Downloading images"
python download-dataset.py $CSV_PATH $VAL_CSV_PATH $DOWNLOAD_PATH


echo "Creating train lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset.bin \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    --shuffle \
    $DOWNLOAD_PATH \
    $CSV_PATH \
    $LMDB_PATH/train_lmdb

echo "Creating validation lmdb..."
GLOG_logtostderr=1 $TOOLS/convert_imageset.bin \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    --shuffle \
    $DOWNLOAD_PATH \
    $VAL_CSV_PATH \
    $LMDB_PATH/val_lmdb


echo "Training network (Press Ctrl+C to finish)..."
GLOG_logtostderr=1 $TOOLS/caffe.bin \
    train \
    --solver $SOLVER

echo "Done"