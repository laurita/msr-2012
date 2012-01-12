# Data Mining Phun

## Data

    $ sqlite3 data/db.sqlite3 tables.sql
    $ python load_commits.py
    $ python load_bugs.py
    $ python mr.py # init_data
    $ python mr.py data/bugs_files.txt > data/paths_weights.txt
    $ awk '{print $1":"$2}' data/paths_weights.txt | sort -t : -k 2,2nr | tail -n +224

## Plots

    $ gnuplot

    reset
    n=100
    max=10
    min=0
    width=(max-min)/n
    hist(x,width)=width*floor(x/width)+width/2.0
    set term png
    set output "histogram.png"
    set xrange [min:max]
    set yrange [0:]
    set offset graph 0.05,0.05,0.05,0.0
    set xtics min,(max-min)/5,max
    set boxwidth width*0.9
    set style fill solid 0.5
    set tics out nomirror
    set xlabel "Path weights"
    set ylabel "Frequency"
    plot "gnuplot.data" u (hist($1,width)):(1.0) smooth freq w boxes lc rgb"green" notitle
