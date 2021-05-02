#!/bin/bash

image_name_path=$1
out_images_folder=$2
folder_container=$3
out_image_name=$4

cd $out_images_folder
out_image_name=${out_image_name//./""}

mkdir -p $folder_container
cd $folder_container

convert $image_name_path \
         -define histogram:unique-colors=false \
         histogram:1-$out_image_name"-histogram.png"