@ECHO OFF

SET image_name_path=%1
SET out_images_folder=%2
SET folder_container=%3
SET out_image_name=%4

cd %out_images_folder%
SET out_image_name=%out_image_name:.=%

IF NOT EXIST %folder_container% (MKDIR %folder_container%)
CD %folder_container%

convert.exe %image_name_path% -define histogram:unique-colors=false histogram:"1-%out_image_name%-histogram.png"