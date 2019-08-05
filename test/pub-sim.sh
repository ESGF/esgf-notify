cert=cert.pem
host=`hostname -f`
sleeptime=30

i=0

for f in `ls $1` ; do

    file=$1/$f

	wget --no-check-certificate --ca-certificate $cert\
     --certificate $cert --private-key $cert\
     --verbose --post-file=$file\
     https://$host/esg-search/ws/publish

	if [ $? -eq 0 ] ; then
	    mv $file $3
	fi


	sleep $sleeptime

	i=$(( $i + 1 ))

	if [ $i -eq $2 ] ; then
		exit 0
	fi
done

