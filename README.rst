======================================================
Social Graph Analysis using Elastic MapReduce and PyPy
======================================================

This project demonstrates some simple social graph analysis based on the
largest publicly available crawl of the twitter social graph.  This data
was collected by
`Kwak, Haewoon and Lee, Changhyun and Park, Hosung and Moon, Sue`_ in 2009.

This 5 gigabyte compressed (26 gigabyte uncompressed) dataset makes
for a good excuse to use MapReduce_ and MrJob_ for processing.  MrJob makes
it easy to test MapReduce jobs locally as well as run them on a local Hadoop_
cluster or on Amazon's `Elastic MapReduce`_.

Analyzing the data
------------------

This project contains two MapReduce jobs:

``jobs/follower_count.py``
   A simple single-stage MapReduce job that reads the data in and sums the number of
   followers each user has.

``jobs/follower_histogram.py``
   This is a two-phase MapReduce job that first sums the number of followers a each
   user has then for each follower count sums the number of users that have that number
   of followers.  This is one of many interesting ways at looking at this raw data.


Running the jobs
----------------

The following assumes you have a modern Python and have already installed MrJob
(``pip install MrJob`` or ``easy_install MrJob`` or `install it from source`_).

To run the sample data locally::

    $ python jobs/follower_count.py data/twitter_synthetic.txt

This should print out a summary of how many followers each user (represented by id)
has::

    5       2
    6       1
    7       3
    8       2
    9       1

You can also run a larger sample (the first 10 million rows of the full dataset mentioned
above) locally though it will likely take several minutes to process::

    $ python jobs/follower_count.py data/twitter_sample.txt.gz

After editing ``conf/mrjob-emr.conf`` you can also run the sample on Elastic MapReduce::

    $ python jobs/follower_count.py -c conf/mrjob-emr.conf -r emr -o s3://your-bucket/your-output-location --no-output data/twitter_sample.txt.gz
    
You can also upload data to an S3 bucket and reference it that way::

    $ python jobs/follower_count.py -c conf/mrjob-emr.conf -r emr -o s3://your-bucket/your-output-location --no-output s3://your-bucket/twitter_sample.txt.gz

You may also download the full dataset and run either the follower count or the histogram job.  The
following general steps are required:

1. Download the whole data file from `Kwak, Haewoon and Lee, Changhyun and Park, Hosung and Moon, Sue`_
   via bittorrent.  I did this on a small EC2 instance in order to make uploading to S3 easier.
2. To make processing faster, decompress it, split it in to lots of smaller files (``split -l 10000000``
   for example).
3. Upload to an S3 bucket.
4. Run the full job (it took a little over 15 minutes to read through 1.47 billion relationships and
   took just over an hour to complete).

::

    python jobs/follower_histogram.py -c conf/mrjob-emr.conf -r emr -o s3://your-bucket/your-output-location --no-output s3://your-split-input-bucket/

Speeding things up with PyPy
----------------------------

While there are lots of other things to explore in the data, I also wanted to be able to run PyPy_ on
Elastic MapReduce.  Through the use of `bootstrap actions`_, we can prepare our environment to use PyPy
and tell MrJob to execute jobs with PyPy instead of system Python.  The following need to be added to your
configuration file (and vary between 32 and 64 bit)::

    # Use PyPy instead of system Python
    bootstrap_scripts:
    - bootstrap-pypy-64bit.sh
    python_bin: /home/hadoop/bin/pypy

This configuration change (available in ``conf/mrjob-emr-pypy-32bit.conf`` and ``conf/mrjob-emr-pypy-64bit.conf``)
also makes use of a custom bootstrap script found in ``conf/bootstrap-pypy-32bit.sh`` and ``conf/bootstrap-pypy-64bit.sh``).

A single run of ``follower_histogram.py`` with 8 ``c1.xlarge`` instances took approximately 66 minutes
using Elastic MapReduce's system Python.  A single run with the same configuration took approximately 44
minutes.  While not a scientific comparison, that's a pretty impressive speedup for such a simple task.  PyPy should speed things up even more for more complex tasks.

.. _Kwak, Haewoon and Lee, Changhyun and Park, Hosung and Moon, Sue: http://an.kaist.ac.kr/traces/WWW2010.html
.. _MapReduce: http://en.wikipedia.org/wiki/MapReduce
.. _MrJob: http://packages.python.org/mrjob/
.. _Hadoop: http://hadoop.apache.org/
.. _Elastic MapReduce: http://aws.amazon.com/elasticmapreduce/
.. _head: http://en.wikipedia.org/wiki/Head_(Unix)
.. _reservoir sampling: http://en.wikipedia.org/wiki/Reservoir_sampling
.. _install it from source: https://github.com/Yelp/mrjob
.. _PyPy: http://pypy.org/
.. _bootstrap actions: http://docs.amazonwebservices.com/ElasticMapReduce/latest/DeveloperGuide/index.html?Bootstrap.html