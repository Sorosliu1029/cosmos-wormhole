#!/usr/bin/env sh

jupyter nbconvert index.ipynb \
  --TagRemovePreprocessor.enabled=True \
  --TagRemovePreprocessor.remove_cell_tags="['remove_cell']" \
  --no-prompt \
  --to html

sed -i '' 's/<pre>打开小宇宙/<pre style="line-height: 1;">打开小宇宙/g' index.html
