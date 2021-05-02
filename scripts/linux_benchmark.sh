#!/bin/bash

image_name_path=$1
out_images_folder=$2
folder_container=$3
out_image_name=$4

cd $out_images_folder
out_image_name=${out_image_name//./""}

mkdir -p $folder_container
cd $folder_container

convert $image_name_path -colorspace Gray 4-$out_image_name"_gray.png"

convert $image_name_path \
         -define histogram:unique-colors=false \
         histogram:3-$out_image_name"-histogram.png"

convert 3-$out_image_name"-histogram.png" -strip -resize 50% -separate ""%d-$out_image_name"-histogram".png