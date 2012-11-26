set terminal postscript eps enhanced monochrome "Helvetica" 15

set output "m1.eps"

set key top center outside

set ylabel 'SMAPE'
set xlabel 'Series'

set yrange[0:1]

set datafile separator ' '
set xrange[0:100]

set boxwidth 0.2
plot 'm1.dat' using ($1-0.3):2 title 'error without prediction' with boxes, \
     '' using 1:4 title 'prediction errpr' with boxes, \
     '' using ($1+0.3):3 title 'overall error' with boxes
