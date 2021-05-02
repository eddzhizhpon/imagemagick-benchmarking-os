@ECHO OFF

SET image_name_path=%1
SET out_images_folder=%2
SET folder_container=%3
SET out_image_name=%4

cd %out_images_folder%
SET out_image_name=%out_image_name:.=%

IF NOT EXIST %folder_container% (MKDIR %folder_container%)
CD %folder_container%

convert.exe "0-%out_image_name%_gray.png" -define histogram:unique-colors=false histogram:"2-%out_image_name%-histogram.png"