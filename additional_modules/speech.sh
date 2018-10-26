 echo "$1" | for a in `cat`; do V=$(((($RANDOM) % 100) - 40)); echo -n "<prosody pitch=\"+$V\">$a</prosody> " | sed 's/+-/-/'; done | espeak -ven+f3 -m -p 60 -s 180

