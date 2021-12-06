#!/bin/bash

mkdir -p tmp
mkdir -p output/lilypond
mkdir -p output/pdf

src/scripts/songbook.py -s src/settings.yaml

source=tmp/yidishe-folkslider.lytex

lilypond-book   \
    --latex-program=xelatex \
    --output=tmp \
    --include=output/lilypond/ \
    --include=../output/lilypond/ \
    $source
  f=${source##*/}
  cd tmp
  xelatex -halt-on-error ${f%.*}.tex
  cd ../
  mv tmp/${f%.*}.pdf output/pdf/${f%.*}.pdf
  echo
