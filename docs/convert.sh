#!/usr/bin/env sh

jupyter nbconvert index.ipynb \
  --TagRemovePreprocessor.enabled=True \
  --TagRemovePreprocessor.remove_cell_tags="['remove_cell']" \
  --no-prompt \
  --to html

perl -0777 -pe 's/互通(.*)二维码/互通<p style="line-height: 1;">$1<\/p>二维码/smg' index.html >out.html
sed -i '' 's/<title>index<\/title>/<title>cosmos-wormhole<\/title><link rel="icon" href=".\/logo.png" type="image\/x-icon">/g' out.html

mv out.html index.html
