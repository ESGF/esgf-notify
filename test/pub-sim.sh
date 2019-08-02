cert=cert.pem
host=`hostname -f`
i=0

for file in `ls $1` ; do

	wget --no-check-certificate --ca-certificate $cert\
     --certificate $cert --private-key $cert\
     --verbose --post-file=$file\
     https://$host/esg-search/ws/publish

	sleep 30

	i=$(( $i + 1 ))

	if [ $i -eq $2 ] ; then
		exit 0
	fi
done

