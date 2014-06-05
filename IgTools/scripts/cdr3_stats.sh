#!/bin/bash

#####################################################################
### input argument parsing

usageStr="Usage: `basename $0` [-n int (full-seq)] [-c int (cdr3)] [-v int (Vgene)] [-j int (Jgene)] [filename] (-h for help) (-d to print file headers)"
if (($# == 0)); then
	echo $usageStr;
	exit $E_OPTERROR;
fi


while getopts ":n:c:v:j:dh" opt; do
  case $opt in
    h)
      echo "$usageStr
      
Compile CDR3 stats for sequences in a data set.
Data file is tab-delimited and must contain CDR3, V-gene, J-gene,
  and (optionally) NT/AA full-length sequences. Header is assumed.

Input arguments:
  -d  print each header field & its index.
Required arguments (if -d not set):
  -n  <column #> index of full-length seq col (NT or AA) for
       filtering to 2+ reads. Set this to 0 to skip filtering or
       if it's already done.
  -c  <column #> index of CDR3 col (AA)
  -v  <column #> index of V-gene col (ex. vals look like 'IGHV3-1')
  -j  <column #> index of J-gene col

Results folder 'CDR3_stats' is created in the same directory as 
the input data. Result files are tab delimited cols of value:count.
The names should be self-explanatory."
      exit $E_OPTERROR
      ;;
    d)
      d=1;
      break;;
    n)
      nt=$OPTARG;;
    c)
      cdr=$OPTARG;;
    v)
      vgene=$OPTARG;;
    j)
      jgene=$OPTARG;;
    \?)
      echo "unknown option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Otion -$OPTARG requires an argument.">&2
      exit 1
      ;;
  esac
  if [[ ! $OPTARG =~ ^[0-9][0-9]*$ ]]; then
    echo "Argument for "$opt" must be an integer index into data column."
    exit 1
  fi
done


fn=${!OPTIND}
if (( ! ${#fn} )); then echo -e "Must provide valid file name.\n$usageStr"; exit 1; fi
if [ ! -f "$fn" ]; then echo "File '$fn' does not exist."; exit 1; fi

origPath=`pwd`
cd "`dirname "$fn"`"
fn="`basename "$fn"`"

if [[ $d = 1 ]]; then
  echo -e "col#\tfield"
  head -n 1 "$fn" | tr "\t" "\n" | awk 'BEGIN{ OFS="\t" }{ f=substr($1,1,57); t=substr($1,58,3);gsub(/./,".",t); print NR,f t}'
  exit 1
fi


for i in nt cdr vgene jgene;
do
  # if (( ! ${!i}+0 )); then echo "Option $i is required."; exit 1; fi
  if (( ! ${#i} )); then echo "Option $i is required."; exit 1; fi
done

#####################################################################


### file names

tmpFolder="./tmp"`date +%s`"/"
outFolder="./CDR3_stats_out/"
fnSort=$tmpFolder"sorted_"$fn
fnTMP=$tmpFolder"t1.txt"
fnNoSingles=$outFolder${fn/.txt/}"_noSingles.txt"

fnUniqCDR3=$outFolder${fn/.txt/}"_uniCDR3.txt"
fnLen=$outFolder${fn/.txt/}"_LengthDist_CDR3.txt"
fnAA=$outFolder${fn/.txt/}"_AADist.txt"
fnV=$outFolder${fn/.txt/}"_VGeneDist.txt"
fnJ=$outFolder${fn/.txt/}"_JGeneDist.txt"

### do stuff

mkdir $tmpFolder
mkdir -p $outFolder

if [ $nt -ge 1 ]; then
	# put data into sorted order based on column $nt
	tail -n +2 $fn | tr -d "\r" | sort -t$'\t' -k $nt,$nt > $fnSort
	# get counts of each val in column $nt
	cut -f$nt $fnSort | uniq -c | tr -s " *" "\t" | cut -f2,3 > $fnTMP
	# remove rows with duplicate $nt vals from fnSort & join with fnTMP. Sort by decreasing count. Save.
	sort -uk $nt,$nt $fnSort |join -t$'\t' -1 2 -2 $nt $fnTMP - | sort -rk 2,2 > $fnNoSingles
	cdr=$(($cdr + 1))
	vgene=$(($vgene + 1))
	jgene=$(($jgene + 1))
else
	tail -n +2 $fn > $fnNoSingles
fi

### get unique CDR3s ###

# print CDRH3, V-gene, J-gene, CDR3 length. Allele numbers are removed from V/J genes.
vjSanitizeExpr="([a-zA-Z]*|[a-zA-Z]?($|[^a-zA-Z0-9].*))" # match all but the gene group number
sort -t$'\t' -uk $cdr,$cdr $fnNoSingles | awk -F$'\t' 'BEGIN{OFS = FS; expr="'$vjSanitizeExpr'"} {gsub(expr,"",$'$vgene'); gsub(expr,"",$'$jgene'); print $'$cdr',$'$vgene',$'$jgene',length($'$cdr')}' > $fnUniqCDR3

cdr_=1
vgene_=2
jgene_=3
len_=4

### Compile stats.

echo -e "AA\tcount"> $fnAA
cut -f$cdr_ $fnUniqCDR3 | grep -o '\w' | awk 'BEGIN{OFS="\t"} {aa[$1]++} END{for(a in aa) print a,aa[a]}' | sort >> $fnAA

echo -e "Length\tcount"> $fnLen
cut -f$len_ $fnUniqCDR3 | awk 'BEGIN{len[0]=0; max=0; i=1;} {len[$1]++; if($1>max)max=$1} END{while(i<=max+1){print i,len[i]+0;i++;}}' >> $fnLen

echo -e "V-gene\tcount"> $fnV
cut -f$vgene_ $fnUniqCDR3 | sort | uniq -c | tr -s " *" "\t" | awk -F$'\t' 'BEGIN{OFS = FS} { print $3,$2}' >> $fnV

echo -e "J-gene\tcount"> $fnJ
cut -f$jgene_ $fnUniqCDR3 | sort | uniq -c | tr -s " *" "\t" | awk -F$'\t' 'BEGIN{OFS = FS} { print $3,$2}' >> $fnJ

rm -r $tmpFolder
cd "$origPath"