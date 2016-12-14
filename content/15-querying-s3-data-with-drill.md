Title: Query your S3-hosted CSV data like a SQL database with Drill!
Date: 2016-04-12 16:55
Tags: data, sql, drill, apache, s3
Slug: querying-s3-data-with-drill
Author: Matthew Rich
Summary: Apache Drill can turn CSVs into a cloud-hosted database.

There is a large and growing [ecosystem](https://hadoopecosystemtable.github.io/)
of tools around the Hadoop project, tackling various parts of the problem of
analyzing data at scale. One of the projects I find most interesting is [Apache
Drill](https://drill.apache.org/), a query engine that can translate
ANSI-complete SQL queries into map-reduce statements that it runs against a
variety of non-relational storage backends: HBase, MongoDB, local files, and
one that I found most interesting: [S3](http://aws.amazon.com/s3/).

## Standards

Of course we all love the CSV file format for tabular data and the SQL
language for querying relational data. Both are universally supported, well
understood, and battle tested over decades.

There's a newer standard that I love as well: S3. it's incredibly easy to use
and understand, cheap, reliable, and works over the internet using the standard
HTTP tools that power the rest of the web. There are also plenty of vendors out
there that offer storage services that are API-compatible with S3, so while S3
itself is a single vendor's product, it has also become a de facto standard for
object storage on the web.

Apache Drill can tie these three awesome standards together and make
data analysis on distributed data over the web fast and easy.

## Getting Started

I like to play around with the [USGS Great Lakes Commercial Fishing Data
Set](http://gcmd.gsfc.nasa.gov/KeywordSearch/Metadata.do?Portal=idn_ceos&KeywordPath=[Personnel%3A+Last_Name%3D%27STEVENS%27%2C+Middle_Name%3D%27B.%27%2C+First_Name%3D%27TYLER%27]&OrigMetadataNode=GCMD&EntryId=brdglsc0001&MetadataView=Full&MetadataType=0&lbnode=mdlb3)
because I love the Great Lakes, the data is pretty interesting, and it is
available in easy to parse CSV files. For this exercise I uploaded the data to
an S3 bucket called `drill-demo`. If you want to follow along, go ahead and do
the same and make sure you have an IAM user created that has at least the
`AmazonS3ReadOnlyAccess` policy attached and has access to the bucket. You'll
need that user's access key and secret key later.

To get Drill up and running, do the following:

### Create an EC2 instance running Ubuntu 14.04 and install Drill.
You'll need to make sure that the security group you launch this instance
allows inbound SSH connections *and* inbound connections on TCP port 8047 from
your IP address.  Drill's web console listens on port 8047. I used a t2.large
instance so Drill would have the 8GB of RAM that it wants. Once it is up and
running, SSH into it to run the following commands:

```
ubuntu@<hostname>:~$ sudo apt-get install default-jdk
ubuntu@<hostname>:~$ curl -o apache-drill-1.6.0.tar.gz http://apache.mesi.com.ar/drill/drill-1.6.0/apache-drill-1.6.0.tar.gz
ubuntu@<hostname>:~$ tar xvfz apache-drill-1.6.0.tar.gz
ubuntu@<hostname>:~$ cd apache-drill-1.6.0
```

### Add your IAM credentials.
You need to tell Drill which credentials to use to access S3, so edit
`conf/core-site.xml` and enter your IAM Access Key and Secret Key:

```
<configuration>

  <property>
	  <name>fs.s3a.access.key</name>
	  <value>YOUR_ACCESS_KEY</value>
  </property>

  <property>
	  <name>fs.s3a.secret.key</name>
	  <value>YOUR_SECRET_KEY</value>
  </property>

</configuration>
```

### Start Drill.
```
ubuntu@<hostname>:~$ ./bin/drill-embedded
```

If you get an unknown host error, you may need to edit the `/etc/hosts` file
and add an entry for your hostname and IP address. You can view your IP
address with this command:

```
ubuntu@<hostname>:~$ /sbin/ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | awk '{print $1}'
```

and then add it to your `/etc/hosts` file with this command:

```
ubuntu@<hostname>:~$ sudo sh -c 'echo "<YOUR IP ADDRESS> `hostname`" >>/etc/hosts'
```
Then re-run the `./bin/drill-embedded` command.
  
### Configure the S3 storage plugin.
Open a browser and point it at http://`<public ip>`:8047/ where `<public ip>`
is the public IP address for your instance shown in the EC2 console. Click the
"Storage" nav link, then click the "Update" button next to the "dfs" plugin,
and copy the JSON document there to your clipboard. Then click "Back", and if
there is already a plugin named "s3" click its "Update" button, otherwise
create a new storage plugin named "s3". Paste in the JSON from your clipboard,
and edit the `connection` field to look like the following:
```
"connection": "s3a://<s3-bucket-name>/",
```
replacing `<s3-bucket-name>` with the name of your bucket. Note that the
default configuration of Drill assumes you are actually using Amazon S3, and so
its default endpoint is `s3.amazonaws.com`. If you are using an S3-compatible
provider you will need to do additional configuration in `core-site.xml`, as
outlined
[here](https://hadoop.apache.org/docs/stable/hadoop-aws/tools/hadoop-aws/index.html).

If you have put your files into the root directory of your bucket you are good
to go, otherwise you may want to edit the "root" workspace location to be the
folder containing your files.

Now click the "Update" and "Enable" buttons, and you are all set.

## Do SQL to your data!

At this point you can go back to your SSH session where the Drill prompt is
waiting for you to query the data. Assuming that your storage plugin is named
`s3`and the `root` workspace contains your CSV files, you can use the `USE`
command in Drill to set that as your default workspace:
```
0: jdbc:drill:zk=local> USE `s3`.`root`;
+-------+-----------------------------------------+
|  ok   |                 summary                 |
+-------+-----------------------------------------+
| true  | Default schema changed to [s3.root]  |
+-------+-----------------------------------------+
1 row selected (1.448 seconds)
```
Cool! Now we can just access our CSVs like they were SQL tables!
```
0: jdbc:drill:zk=local> SELECT * FROM `LAKE.csv`;
+-----------------------+
|        columns        |
+-----------------------+
| ["LAKE","LAKE_NAME"]  |
| ["1","Superior "]     |
| ["2","Michigan "]     |
| ["3","Huron    "]     |
| ["4","St. Clair"]     |
| ["5","Erie     "]     |
| ["6","Ontario  "]     |
+-----------------------+
7 rows selected (1.088 seconds)
```

Huh, that's weird. These CSV files all have a header row but Drill doesn't
know to use it. To fix that, we can edit our `s3` storage plugin again, adding
`"extractHeader": true,` to the options for the `csv` format. Save the change
and Drill immediately picks it up, no need to restart:
```
0: jdbc:drill:zk=local> SELECT * FROM `LAKE.csv`;
+-------+------------+
| LAKE  | LAKE_NAME  |
+-------+------------+
| 1     | Superior   |
| 2     | Michigan   |
| 3     | Huron      |
| 4     | St. Clair  |
| 5     | Erie       |
| 6     | Ontario    |
+-------+------------+
6 rows selected (0.865 seconds)
```
Much better! `CATCH.csv` is the biggest file, containing each individual catch
recorded by the study. Let's see how many records there are. We can't do a 
`SELECT COUNT(*)` because we have `extractHeader` turned on, so we need to
pick an actual column to count:
```
0: jdbc:drill:zk=local> SELECT COUNT(CATCH_ID) FROM `CATCH.csv`;
+----------+
|  EXPR$0  |
+----------+
| 2800764  |
+----------+
1 row selected (9.182 seconds)
```
2.8 million records counted in about 9 seconds -- not blazingly fast by any means,
but considering we're doing this over the web, not too shabby! We could no doubt
speed things up by using a cluster of Drill nodes rather than just the single,
"embedded" instance we are using now.

Let's try a join and an aggregation. The `DEPTH1` field contains the beginning
depth of the catch, in fathoms, so let's take a look at that, converting it to
feet:
```
0: jdbc:drill:zk=local> SELECT `LAKE.csv`.LAKE_NAME, AVG(CAST(`EFFORT.csv`.DEPTH1 AS INT))*6
. . . . . . . . . . . > FROM `CATCH.csv`
. . . . . . . . . . . > JOIN `EFFORT.csv` ON `CATCH.csv`.EFFRT_ID = `EFFORT.csv`.EFFRT_ID
. . . . . . . . . . . > JOIN `IDENTIFY.csv` ON `CATCH.csv`.RPRT_ID = `IDENTIFY.csv`.RPRT_ID
. . . . . . . . . . . > JOIN `LAKE.csv` ON `IDENTIFY.csv`.LAKE = `LAKE.csv`.LAKE
. . . . . . . . . . . > WHERE `EFFORT.csv`.DEPTH1 IS NOT NULL AND `EFFORT.csv`.DEPTH1 <> ''
. . . . . . . . . . . > GROUP BY `LAKE.csv`.LAKE_NAME;
+------------+---------------------+
| LAKE_NAME  |       EXPR$1        |
+------------+---------------------+
| Superior   | 259.41383426656904  |
| Erie       | 49.724441190057675  |
| Michigan   | 120.11003070055284  |
| Huron      | 61.84580334925012   |
| Ontario    | 20.343089633412212  |
+------------+---------------------+
5 rows selected (17.582 seconds)
```
There you have it -- average catch depth in feet for each of the great lakes.

In a follow-up blog post, I'll show how you can connect to Drill via ODBC so
you're not limited to just raw SQL and can integrate Drill into your data
analysis pipeline! 
