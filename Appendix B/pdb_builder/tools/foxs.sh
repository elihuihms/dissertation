shopt -s nullglob
for f in $1/*pdb
do
	foxs -q 0.3 -s 200 $f
done

