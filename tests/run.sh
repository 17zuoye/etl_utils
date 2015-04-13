#!/usr/bin/env bash


for file1 in test.py
do
  echo "[test] $file1"
  python tests/$file1
done

rm -rf build dist etl_utils-info # clean tmp files
