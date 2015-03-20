#!/bin/bash

FILES_1=conf_history_QT/*pdf

mkdir movie_images
for f in $FILES_1
do
	filename=$(basename "$f")
	sips -s format jpeg "conf_history_QT/$filename" --out "conf_history_QT/$filename.jpg"
	sips -s format jpeg "conf_history_QA/$filename" --out "conf_history_QA/$filename.jpg"
	sips -s format jpeg "conf_history_QTQA/$filename" --out "conf_history_QTQA/$filename.jpg"

	montage "conf_history_QT/$filename.jpg" "conf_history_QA/$filename.jpg" "conf_history_QTQA/$filename.jpg" \
	-geometry -40-40-40-40 -tile 2x2 "movie_images/$filename.jpg"
	
done

rm conf_history_QT/*.jpg
rm conf_history_QA/*.jpg
rm conf_history_QTQA/*.jpg