#!/bin/bash

# ########################################################################
# ###### Skip this section to run it as a script
# ########################################################################

# usageStr="Usage: `basename $0` [-f filename] [-s sample name] (-h for help) (-d to print file headers)"
# if (($# == 0)); then
#   echo $usageStr;
#   exit $E_OPTERROR;
# fi

# ## TODO: more input arg checking, documentation.
# while getopts ":f:s:dh" opt; do
#   case $opt in
#     h)
#       echo "$usageStr
# Input arguments:
#   -f  input file (required)
#   -s  sample name
#     -- OR --
#   -d  print each header field & its index.
# "
#       exit $E_OPTERROR
#       ;;
#     d)
#       d=1;
#       break;;
#     f)
#       fn=$OPTARG;;
#     c)
#       sample=$OPTARG;;
#     \?)
#       echo "unknown option: -$OPTARG" >&2
#       exit 1
#       ;;
#     :)
#       echo "Otion -$OPTARG requires an argument.">&2
#       exit 1
#       ;;
#   esac
# done

# if (( ! ${#fn} )); then echo -e "Must provide valid file name.\n$usageStr"; exit 1; fi
# if [ ! -f "$fn" ]; then echo "File '$fn' does not exist."; exit 1; fi

# origPath=$(pwd)
# cd "$(dirname "$fn")"
# fn="$(basename "$fn")"

# if [[ $d = 1 ]]; then
#   echo -e "col#\tfield"
#   head -n 1 "$fn" | tr "\t" "\n" |
#     awk ' BEGIN {
#         OFS="\t"
#       }
#       {
#         f=substr($1,1,57);
#         t=substr($1,58,1); sub(/./,"...",t);
#         print NR,f t
#       }
#     '
#   exit 1
# fi
# fOriginal="$fn"


########################################################################
###### User-defined parameters
########################################################################

#   fOriginal: input file you want to process
# fOriginal="./023_002_V6_unique_processed.txt"
#   sample: used for naming output files
#     Risk of writing over original file is this is named exactly the same
# sample="023_002_V6_unique_processed"

#   column indices
#     See just below for a command to print file column indices
col_Ref_Header=1
col_VDJ_aa=2
col_Count=3
col_CDRH3=4

#   print delimited fields of first line with column numbers
# head $fOriginal -n 1 | tr '\t' '\n' | awk 'BEGIN{print("\ncol  field")} { printf("  %-3d%s\n", NR, $0)}'


######              end of user-defined params                    ######

########################################################################
###### Initialize common vars used in scripts below
########################################################################

# Field index & delimiter vars passed into most of the awk scripts.
#   FS: input field separator (default is tabs & spaces)
#   OFS: output field separator
awkParams="-v cHeader=$col_Ref_Header
-v cVDJaa=$col_VDJ_aa
-v cReads=$col_Count
-v cCDRH3=$col_CDRH3
-v FS=\t
-v OFS=\t"

# Preprocess original file. Remove first line (assumes it's a header) and empty seqence lines.
#   If your file has no header, use this instead: sed -e '/^[ \t]*$/d' < $fIn > $fClean
fClean="$sample"
sed -e '1d' -e '/^[ \t]*$/d' < $fOriginal > "$fClean"
fIn="$fClean" # this file will now be the input for subsequent scripts.


########################################################################
###### Main scripts
########################################################################

####################################
### filter out non-IgG sequences, discard VDJaa sequence past the ASTK
### rule: keeps line if VDJaa contains "...CDR3...ASTK"
####################################
echo "filter out non-IgG sequences, discard VDJaa sequence past the ASTK"
fOut_IgG_trunc="$fIn""_IgG-trunc"
awk $awkParams '
    {
      if (match($cVDJaa, /'$cCDRH3'.*ASTK/)) {
        $cVDJaa = substr($cVDJaa,0,RLENGTH);
        print;
      }
    }
  ' "$fIn" > "$fOut_IgG_trunc"

    # ### same as above but retains full VDJaa sequence
    # fOut="_IgG_fullVDJaa"
    # awk $awkParams '
    #       $cVDJaa ~ /'$cCDRH3'.*ASTK/ {
    #         print
    #       }
    #   ' "$fIn" > "$fOut"

####################################
### merge IgG based on ASTK-terminated VDJaa seqs, combining read counts
###   This might look better as a sed script.
####################################
echo "merge IgG based on ASTK-terminated VDJaa seqs, combining read counts"
fIn="$fOut_IgG_trunc"
fOut_IgG="$sample""_IgG"
sort -t $'\t' -k $col_VDJ_aa "$fIn" |  
  awk $awkParams '
      BEGIN {
        lineBuf = "";
        seqReads=0;
        prevSeq = "";
      }
      $cVDJaa == prevSeq {
        seqCount += $cReads;
      }
      $cVDJaa != prevSeq {
        if (NR>1) {
          sub(/~~~/,seqCount,lineBuf)
          print(lineBuf)
        }
        prevSeq = $cVDJaa;
        seqCount = $cReads;
        $cReads = "~~~";
        lineBuf = $0;
      }
      END {
        sub(/~~~/,seqCount,lineBuf)
        print(lineBuf)
      }
    ' > $fOut_IgG

####################################
### filter out single reads and VDJaa containing 'X' or 'Z'
####################################
echo "filter out single reads and VDJaa containing 'X' or 'Z'"
fIn="$fOut_IgG"
fOut_filt="$fIn""_2+reads_noXZ"
awk $awkParams '
    $cVDJaa !~ /[XZ]/  &&  $cReads>1 {print}
  ' "$fIn" > "$fOut_filt"

    # ####################################
    # ### filter out single reads
    # ####################################
    # fOut="$fIn""_2+reads"
    # awk $awkParams '
    #     $cReads>1 {print}
    #   ' "$fIn" > "$fOut"

    # ####################################
    # ### filter out reads containing 'X' or 'Z'
    # ####################################
    # fOut="$fIn""_noXZ"
    # awk $awkParams '
    #     $cVDJaa !~ /[XZ]/ {print}
    #   ' "$fIn" > "$fOut"

####################################
### print set of all unique CDRH3s
####################################
echo "print set of all unique CDRH3s"
fIn_uniCDRH3="$fOut_filt"
fOut_uniCDRH3="$fIn""_uniqueCDRH3"
cut -f $col_CDRH3 "$fIn_uniCDRH3" | sort | uniq > "$fOut_uniCDRH3"


########################################################################


####################################
### CLUSTER!
####################################

# function CLUST_WITH_ARGS.EXE clusters sequences

fIn_toClust="$fOut_uniCDRH3"
fOut_clusts="$(date "+CDR3_clusts_%m%d%y_%H%M%S")" # create output clust file with timestamp
clustThreshold=0.1 # threshold for sequence similarity.
                   #   Determines max # of differences/errors/mismatches/gaps for seqs to cluster.
                   # allowedErrors = 1 OR round( clustThreshold*length(sequence) ). 0.1 corresponds to 90% similarity.
./clust_with_args -f "$fIn_toClust" -o "$fOut_clusts" -t $clustThreshold


####################################
### Append cluster # to filtered original file.
####################################
  fOut_Clustered="$sample""_Clustered"
  fIn="$fIn_uniCDRH3"
    fTemp="TEMP_$fIn"
    sort -t$'\t' -k $col_CDRH3 "$fIn" > "$fTemp"
  ## merge the clustering results with CDRH3 counts.
  sort -k 1 "$fOut_clusts" |
    join -t$'\t' -j1 $col_CDRH3 -j2 1 "$fTemp" - |
    awk $awkParams '
        {
          t = $1
          for ( i=1; i < cCDRH3; i++ ) {
            $(i) = $(i+1);
          }
          $cCDRH3 = t;
          print;
        }
      ' > "$fOut_Clustered"
  rm $fTemp


####################################
### print FASTA of Ref_Header & VDR_aa
####################################
echo "print FASTA of VDJaa with header: Ref_Header, VDJaa reads, CDRH3, Cluster #"
fPreFasta="$fOut_Clustered"
fFasta="$fPreFasta.fasta"
awk $awkParams '
    { printf(">%s|%d|%s|%d\n%s\n", $cHeader, $cReads, $cCDRH3, $NF, $cVDJaa) }
  ' "$fPreFasta" > "$fFasta"



exit


########################################################################
        #        ~~~~~~~~ Troubleshooting ~~~~~~~~        #
########################################################################

#   ERROR: 'Range violation'
#     Clustering program assumes input file contains a column of sequences & nothing else.
#     sequences contain ONLY capitalized letters.
#     Run following line to check your sequence input file:
fIn="$fIn_toClust"
awk 'BEGIN {
      maxPrintLines = 10;
      c=0;
    }
    /[^QWERTYUIOPASDFGHJKLZXCVBNM]/ {
      if(c==0) { print("Bad input lines:")};
      if( c<=maxPrintLines ) {
        printf("  %-4s %c%s%c\n", NR":", 39, $0, 39)
      } else if(c == maxPrintLines+1 ) { print("  ...") }
      c++;
    }
    END {
      if( c > 0 ) {
        printf("--  %d total errors  --\n", c)
      }
      else{
        print("\nInput looks good.\n")
      }
    }
    ' "$fIn"





########################################################################
###### more stuff, not needed for pipeline
###### Print read distributions, reads vs cluster, etc.
########################################################################

####################################
### print distribution of sequence reads
####################################
fIn="$fClean"
fOut="$fIn""_readDist"
cut -f $col_Count "$fIn" | sort -n | uniq -c > "$fOut"

####################################
### accumulate CDR3 reads -- like an SQL groupby
####################################
fIn="$fClean"
fOut_CDR3Dist="$fIn""_CDR3Dist"
awk $awkParams '
    BEGIN { cdr3Count[""]=0 }
    { cdr3Count[$cCDRH3] += $cReads }
    END {
      for ( cdr3 in cdr3Count ) {
        if (cdr3 != "" && cdr3 !~ /[^QWERTYUIOPASDFGHJKLZXCVBNM]/ ) { print cdr3, cdr3Count[cdr3] }
      }
    }
  ' "$fIn" | sort -nr -k 2 > "$fOut_CDR3Dist"


####################################
### make a human-friendly text file showing CDRH3, Cluster#, Length, CDRH3 Reads
####################################
  fOut="Clusts_$sample"
  ## accumulate CDR3 reads
    fIn="$fOut_CDR3Dist"
    fTemp="TEMP_$fIn"
    sort -k 1 "$fIn" > "$fTemp"
  ## merge the clustering results with CDRH3 counts
  sort -k 1 "$fOut_clusts" |
    join -o0,1.2,2.2 "$fTemp" - |
      # each piped line now has format: <$1:CDR3> <$2:Reads> <$3:Cluster>
      # sort cluster then reads
    sort -nr -k 2 |
      # format and print results, adding a field for CDRH3 length
    awk '
      BEGIN {
        printf("%-30s  %-7s %-7s %s\n", "CDRH3", "Cluster", "Length", "Reads")
      }
      {
        cdr3 = $1;
        reads = $2;
        clust = $3;
        if (clust != 0) { printf("%-30s  %-7d %-7d %d\n", cdr3, clust, length(cdr3), reads) }
      }' > "$fOut"
  ### to make the last file into a tab delimited for Excel import
  sed 's/  */\t/g' "$fOut" > "$fOut""_tabDelim.txt"

####################################
### compare CDR clusters to original set of CDR3 with reads.
###   Also, print which CDR3s were discarded before clustering. Include read counts.
####################################
  fOut_prettyClusts="prettyClusts.txt"
  fOut_CDR3_not_clustered="CDRH3_not_clustered.txt"
  sort -k 1 "$fOut_CDR3Dist" > "$fOut_CDR3Dist""_sorted"
  sort -k 1 "$fOut_clusts" |
      # merge clusters with CDRH3 counts
    join -e0 -a1 -o0,1.2,2.2 "$fOut_CDR3Dist""_sorted" - |
      # each piped line now has format: <$1:CDR3> <$2:Reads> <$3:Cluster>
      # sort cluster then reads
    sort -nr -k 2 |
      # format and print results, adding a field for CDRH3 length
    awk '
      BEGIN {
        fOut_prettyClusts="'$fOut_prettyClusts'";
        fOut_notClustered="'$fOut_CDR3_not_clustered'";
        printf("%-30s  %-7s %-7s %s\n", "CDRH3", "Cluster", "Length", "Reads") > fOut_prettyClusts;
        printf("%-30s  %-7s %s\n", "CDRH3", "Length", "Reads") > fOut_notClustered;
      }
      {
        cdr3 = $1;
        reads = $2;
        clust = $3;
        if( clust == 0) {
          printf("%-30s  %-7d %d\n", cdr3, length(cdr3), reads) > fOut_notClustered;
        } else {
          printf("%-30s  %-7d %-7d %d\n", cdr3, clust, length(cdr3), reads) > fOut_prettyClusts;
        }
      }'