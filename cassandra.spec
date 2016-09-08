%{?scl:%scl_package cassandra}
%{!?scl:%global pkg_name %{name}}

# not reserved yet
%global allocated_gid 156
%global allocated_uid 156

Name:           %{?scl_prefix}cassandra
Version:        3.5
Release:        0%{?dist}
Summary:        OpenSource database Apache Cassandra

License:        ASL 2.0
URL:            http://%{pkg_name}.apache.org/
Source0:        https://github.com/apache/%{pkg_name}/archive/%{pkg_name}-%{version}.tar.gz
Source1:	%{pkg_name}.logrotate
Source2:	%{pkg_name}d.service
Source3:	%{pkg_name}-tmpfile

#fix encoding error
Patch0:		%{pkg_name}-build.patch
#airline0.7 imports fix
Patch1:		%{pkg_name}-airline0.7.patch
# modify installed scripts
Patch2:		%{pkg_name}-scripts.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1340876
# remove "Open" infix from all hppc classes
Patch3:		%{pkg_name}-hppc.patch
# changes autoclosable issue with TTransport in thrift
Patch4:		%{pkg_name}-thrift.patch
# add two more parameters for SubstituteLogger constructor in slf4j
Patch5:		%{pkg_name}-slf4j.patch

#BuildArch:      noarch
%{?scl:Requires: %scl_runtime}
Requires:	jpackage-utils
Requires(pre):  shadow-utils

BuildRequires:  systemd
BuildRequires:  python2-devel
BuildRequires:  Cython
BuildRequires:  maven-local
BuildRequires:	ant
BuildRequires:  %{?scl_java_prefix}antlr-tool
BuildRequires:  mvn(de.jflex:jflex)
BuildRequires:  mvn(org.apache.thrift:libthrift)
BuildRequires:  mvn(com.github.jbellis:jamm)
BuildRequires:  %{?scl_prefix}stream-lib
# not supporting f23 any more
BuildRequires:  mvn(io.dropwizard.metrics:metrics-core)
BuildRequires:  mvn(com.googlecode.json-simple:json-simple)
BuildRequires:  mvn(net.ju-n.compile-command-annotations:compile-command-annotations)
# using high-scale-lib from stephenc, no Cassandra original
#BuildRequires:  mvn(com.boundary:high-scale-lib)
BuildRequires:  mvn(com.github.stephenc.high-scale-lib:high-scale-lib)
# temporarly removed as it is optional
# BuildRequires:  mvn(com.datastax.cassandra:cassandra-driver-core)
BuildRequires:  mvn(net.jpountz.lz4:lz4)
BuildRequires:  %{?scl_prefix}snappy-java
BuildRequires:  %{?scl_prefix}jBCrypt
BuildRequires:  mvn(com.googlecode.concurrentlinkedhashmap:concurrentlinkedhashmap-lru)
BuildRequires:  mvn(org.caffinitas.ohc:ohc-core)
# using hadoop-common instead of hadoop-core, no Cassandra original
#BuildRequires:  mvn(org.apache.hadoop:hadoop-core)
# temporarly removed as it is optional
#BuildRequires:  hadoop-common
#BuildRequires:  hadoop-mapreduce
BuildRequires:  %{?scl_prefix}concurrent-trees
BuildRequires:  mvn(com.carrotsearch:hppc)
# using repackaging of the snowball stemmer so that it's available on Maven Central 
#BuildRequires:  mvn(com.github.rholder:snowball-stemmer)
BuildRequires:  mvn(org.tartarus:snowball)
BuildRequires:  mvn(net.mintern:primitive)
BuildRequires:  mvn(ch.qos.logback:logback-core)
BuildRequires:  mvn(ch.qos.logback:logback-classic)
BuildRequires:  mvn(com.addthis.metrics:reporter-config3)
BuildRequires:  mvn(com.ning:compress-lzf)
BuildRequires:  mvn(com.thinkaurelius.thrift:thrift-server)
BuildRequires:  %{?scl_prefix}airline
BuildRequires:  mvn(org.fusesource:sigar)
BuildRequires:  mvn(org.slf4j:log4j-over-slf4j)
BuildRequires:  mvn(org.slf4j:jcl-over-slf4j)
# test dependencies
BuildRequires:  mvn(org.apache.ant:ant-junit)
BuildRequires:  mvn(org.jboss.byteman:byteman)
BuildRequires:  %{?scl_prefix}jmh
# scl dependencies
%{?scl:Requires: %scl_require rh-maven33}

# leftovers 
#BuildRequires:  mvn(org.apache.hadoop:hadoop-minicluster)
#BuildRequires:  mvn(junit:junit)
#BuildRequires:	 hadoop-common
#BuildRequires:	 jsr-305
#BuildRequires:  hadoop-hdfs
#BuildRequires:  hadoop-client
#BuildRequires:  hadoop-common-native
#BuildRequires:  hadoop-devel
#BuildRequires:  hadoop-hdfs-fuse
#BuildRequires:  hadoop-httpfs
#BuildRequires:  hadoop-maven-plugin
#BuildRequires:  hadoop-tests
#BuildRequires:  hadoop-yarn
#BuildRequires:  hadoop-yarn-security
#BuildRequires:  mvn(org.apache.hadoop:hadoop-minicluster)
#BuildRequires:  mvn(org.slf4j:jcl-over-slf4j)
#BuildRequires:  mvn(com.codahale.metrics:metrics-core)
#BuildRequires:  mvn(org.slf4j:log4j-over-slf4j)
#BuildRequires:  mvn(io.netty:netty-all)


%description
Cassandra is a partitioned row store. Rows are organized into tables with
a required primary key. Partitioning means that Cassandra can distribute your
data across multiple machines in an application-transparent matter. Cassandra
will automatically repartition as machines are added / removed from the cluster.
Row store means that like relational databases, Cassandra organizes data by
rows and columns. The Cassandra Query Language (CQL) is a close relative of SQL.
Database Pure Java Driver. It was developed specifically as a lightweight
JDBC connector for use with MySQL and MariaDB database servers.

%package parent
Summary:        Parent POM for %{pkg_name}

%description parent
Parent POM for %{pkg_name}.

%package        thrift
Summary:        Thrift for %{pkg_name}
Requires:       %{pkg_name} = %{version}-%{release}

%description thrift
Allows portable (across programming languages) access to the database. Thrift
accomplishes this by generated source code for the programming language in
question based on a Thrift IDL file describing the service.

%package        clientutil
Summary:        Client utilities for %{pkg_name}
Requires:       %{pkg_name} = %{version}-%{release}
Requires:	python-cassandra-driver

%description clientutil
Utilities usable by client for %{pkg_name}

%package        stress
Summary:        Stress testing utility for %{pkg_name}
Requires:       %{pkg_name} = %{version}-%{release}

%description stress
The cassandra-stress tool is a Java-based stress testing utility
for benchmarking and load testing a Cassandra cluster.

%package        javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%{?scl_enable}
%setup -qcn %{pkg_name}-%{version}
cp -pr %{pkg_name}-%{pkg_name}-%{version}/* .
rm -r %{pkg_name}-%{pkg_name}-%{version}

# remove binary and library files
find -name "*.class" -print -delete
find -name "*.jar" -print -delete
find -name "*.zip" -print -delete
#./lib/futures-2.1.6-py2.py3-none-any.zip
#./lib/six-1.7.3-py2.py3-none-any.zip
#./lib/cassandra-driver-internal-only-2.6.0c2.post.zip
find -name "*.so" -print -delete
find -name "*.dll" -print -delete
find -name "*.sl" -print -delete
find -name "*.dylib" -print -delete
rm -r lib/sigar-bin/sigar-x86-winnt.lib
find -name "*.exe" -print -delete
find -name "*.bat" -print -delete
find -name "*.pyc" -print -delete
find -name "*py.class" -print -delete

# create links to installed libraries
ln -sf $(build-classpath antlr3) lib/antlr-3.5.2.jar
ln -sf $(build-classpath stringtemplate4) lib/ST4-4.0.8.jar
ln -sf $(build-classpath jsr-305) lib/jsr305-2.0.2.jar
ln -sf $(build-classpath commons-lang3) lib/commons-lang3-3.1.jar
ln -sf $(build-classpath libthrift) lib/libthrift-0.9.2.jar
ln -sf $(build-classpath slf4j/api) lib/slf4j-api-1.7.7.jar
ln -sf $(build-classpath guava) lib/guava-18.0.jar
ln -sf $(build-classpath jamm) lib/jamm-0.3.0.jar
ln -sf $(build-classpath stream-lib) lib/stream-2.5.2.jar
ln -sf $(build-classpath metrics/metrics-core) lib/metrics-core-3.0.1.jar
ln -sf $(build-classpath metrics/metrics-logback) lib/metrics-logback-3.0.1.jar
ln -sf $(build-classpath json_simple) lib/json-simple-1.1.jar
ln -sf $(build-classpath antlr3-runtime) lib/antlr-runtime-3.5.2.jar
ln -sf $(build-classpath compile-command-annotations) lib/compile-command-annotations-1.2.0.jar
# https://bugzilla.redhat.com/show_bug.cgi?id=1308556
ln -sf $(build-classpath high-scale-lib/high-scale-lib) lib/high-scale-lib-1.0.6.jar
# temporarly removed because it is optional
#ln -sf $(build-classpath cassandra-java-driver/cassandra-driver-core) lib/cassandra-driver-core-3.0.0.jar
ln -sf $(build-classpath netty/netty-all) lib/netty-all-4.0.23.Final.jar
ln -sf $(build-classpath lz4) lib/lz4-1.3.0.jar
ln -sf $(build-classpath snappy-java) lib/snappy-java-1.1.1.7.jar
ln -sf $(build-classpath jBCrypt) lib/jbcrypt-0.3m.jar
ln -sf $(build-classpath concurrentlinkedhashmap-lru) lib/concurrentlinkedhashmap-lru-1.4.jar
ln -sf $(build-classpath ohc/ohc-core) lib/ohc-core-0.4.2.jar
# temporarly removed because it is optional
#ln -sf $(build-classpath hadoop/hadoop-common) lib/hadoop-common-2.4.1.jar
ln -sf $(build-classpath snakeyaml) lib/snakeyaml-1.11.jar
ln -sf $(build-classpath jackson/jackson-core-asl) lib/jackson-core-asl-1.9.2.jar
ln -sf $(build-classpath jackson/jackson-mapper-asl) lib/jackson-mapper-asl-1.9.2.jar
ln -sf $(build-classpath ecj) lib/ecj-4.4.2.jar
ln -sf $(build-classpath objectweb-asm/asm) lib/asm-5.0.4.jar
ln -sf $(build-classpath commons-math3) lib/commons-math3-3.2.jar
# temporarly removed because it is optional
#ln -sf $(build-classpath hadoop/hadoop-mapreduce-client-core) lib/hadoop-mapreduce-client-core-2.7.2.jar 
ln -sf $(build-classpath concurrent-trees) lib/concurrent-trees-2.5.0.jar
ln -sf $(build-classpath hppc) lib/hppc-0.5.4.jar
ln -sf $(build-classpath snowball-java) lib/snowball-0.jar
ln -sf $(build-classpath logback/logback-classic) lib/logback-classic-1.1.3.jar
ln -sf $(build-classpath logback/logback-core) lib/logback-core-1.1.3.jar
ln -sf $(build-classpath metrics-reporter-config/reporter-config) lib/reporter-config3-3.0.0.jar
ln -sf $(build-classpath metrics-reporter-config/reporter-config-base) lib/reporter-config-base-3.0.0.jar
ln -sf $(build-classpath joda-time) lib/joda-time-2.4.jar
ln -sf $(build-classpath compress-lzf) lib/compress-lzf-0.8.4.jar
ln -sf $(build-classpath disruptor-thrift-server) lib/thrift-server-0.3.8.jar
ln -sf $(build-classpath commons-cli) lib/commons-cli-1.1.jar
ln -sf $(build-classpath airline) lib/airline-0.6.jar
ln -sf $(build-classpath jna) lib/jna-4.0.0.jar
ln -sf $(build-classpath sigar) lib/sigar-1.6.4.jar
# temporarly removed because it is optional
#ln -sf $(build-classpath hadoop/hadoop-annotations) lib/hadoop-annotations-2.4.1.jar
ln -sf $(build-classpath primitive) lib/primitive-1.0.jar
ln -sf $(build-classpath jflex) lib/jflex-1.6.0.jar
ln -sf $(build-classpath java_cup) lib/java_cup-0.11b.jar
ln -sf $(build-classpath commons-codec) lib/commons-codec-1.2.jar
# test dependencies
ln -sf $(build-classpath junit) lib/junit-4.6.jar
ln -sf $(build-classpath ant) lib/ant-1.9.4.jar
ln -sf $(build-classpath ant/ant-junit) lib/ant-junit-1.9.4.jar
ln -sf $(build-classpath hamcrest/core) lib/hamcrest-1.3.jar
ln -sf $(build-classpath apache-commons-io) lib/apache-commons-io-2.4.jar
ln -sf $(build-classpath byteman/byteman-bmunit) lib/byteman-bmunit-3.0.3.jar
ln -sf $(build-classpath commons-collections) lib/commons-collections-3.2.1.jar
ln -sf $(build-classpath jmh/jmh-core) lib/jmh-core-1.1.1.jar
# binaries dependencies
ln -sf $(build-classpath javax.inject) lib/javax.inject.jar

# leftovers
#ln -sf $(build-classpath disruptor) lib/disruptor-3.0.1.jar
#ln -sf $(build-classpath slf4j/jcl-over-slf4j) lib/jcl-over-slf4j-1.7.7.jar

# org.apache.hadoop:hadoop-core,hadoop-minicluster:1.0.3 org.apache.hadoop.conf.Configuration
#rm -r src/java/org/apache/cassandra/hadoop

# build patch
%patch0 -p1
# airline patch
%patch1 -p1
# scripts patch
%patch2 -p1
# hppc patch
%patch3 -p1
# thrift patch
%patch4 -p1
# slf4j patch
%patch5 -p1

%mvn_package "org.apache.%{pkg_name}:%{pkg_name}-parent:pom:3.5" %{pkg_name}-parent
%mvn_package ":%{pkg_name}-thrift"  %{pkg_name}-thrift
%mvn_package ":%{pkg_name}-clientutil" %{pkg_name}-clientutil
%{?scl_disable}

%build
%{?scl_enable}
ant jar javadoc -Drelease=true 

# Build the cqlshlib Python module
pushd pylib
%py2_build
popd
%{?scl_disable}

%install
%{?scl_enable}
%mvn_artifact build/%{pkg_name}-%{version}-parent.pom
%mvn_artifact build/%{pkg_name}-%{version}.pom  build/%{pkg_name}-%{version}.jar
%mvn_artifact build/%{pkg_name}-thrift-%{version}.pom  build/%{pkg_name}-thrift-%{version}.jar
%mvn_artifact build/%{pkg_name}-clientutil-%{version}.pom  build/%{pkg_name}-clientutil-%{version}.jar

%mvn_install -J build/javadoc/

# Install the cqlshlib Python module
pushd pylib
%py2_install
popd
%{?scl_disable}

# create data dir
mkdir -p %{buildroot}%{?scl:%{_root_sharedstatedir}}%{!?scl:%{_sharedstatedir}}/%{pkg_name}

# logs directory plus files
mkdir -p %{buildroot}%{?scl:%{_root_localstatedir}}%{!?scl:%{_localstatedir}}/log/%{pkg_name}
install -p -D -m 644 "%{SOURCE1}"  %{buildroot}%{?scl:%{_root_sysconfdir}}%{!?scl:%{_sysconfdir}}/logrotate.d/%{pkg_name}

#%jpackage_script org.apache.cassandra.service.CassandraDaemon "" "" %%{classpath} cassandra true
install -p -D -m 755 bin/%{pkg_name} %{buildroot}%{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/%{pkg_name}
install -p -D -m 755 bin/%{pkg_name}.in.sh %{buildroot}%{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/%{pkg_name}.in.sh
install -p -D -m 755 conf/%{pkg_name}-env.sh %{buildroot}%{?scl:%{_root_sysconfdir}}%{!?scl:%{_sysconfdir}}/%{pkg_name}-env.sh
install -p -D -m 644 conf/%{pkg_name}.yaml %{buildroot}%{?scl:%{_root_sysconfdir}}%{!?scl:%{_sysconfdir}}/%{pkg_name}.yaml
#cp -p conf/%%{pkg_name}-rackdc.properties %%{buildroot}%%{?scl:%%{_root_sysconfdir}}%%{!?scl:%%{_sysconfdir}}/%%{pkg_name}-rackdc.properties
#cp -p conf/%%{pkg_name}-topology.properties %%{buildroot}%%{?scl:%%{_root_sysconfdir}}%%{!?scl:%%{_sysconfdir}}/%%{pkg_name}-topology.properties
#cp -p conf/commitlog_archiving.properties %%{buildroot}%%{?scl:%%{_root_sysconfdir}}%%{!?scl:%%{_sysconfdir}}/commitlog_archiving.properties
install -p -D -m 644 conf/jvm.options %{buildroot}%{?scl:%{_root_sysconfdir}}%{!?scl:%{_sysconfdir}}/jvm.options
install -p -D -m 644 conf/logback-tools.xml %{buildroot}%{?scl:%{_root_sysconfdir}}%{!?scl:%{_sysconfdir}}/logback-tools.xml
install -p -D -m 644 conf/logback.xml %{buildroot}%{?scl:%{_root_sysconfdir}}%{!?scl:%{_sysconfdir}}/logback.xml
#cp -p conf/metrics-reporter-config-sample.yaml %%{buildroot}%%{?scl:%%{_root_sysconfdir}}%%{!?scl:%%{_sysconfdir}}/metrics-reporter-config-sample.yaml
install -p -D -m 755 bin/cqlsh.py %{buildroot}%{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/cqlsh
install -p -D -m 755 bin/nodetool %{buildroot}%{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/nodetool
install -p -D -m 755 bin/sstableloader %{buildroot}%{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/sstableloader
install -p -D -m 755 bin/sstablescrub %{buildroot}%{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/sstablescrub
install -p -D -m 755 bin/sstableupgrade %{buildroot}%{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/sstableupgrade
install -p -D -m 755 bin/sstableutil %{buildroot}%{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/sstableutil
install -p -D -m 755 bin/sstableverify %{buildroot}%{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/sstableverify
install -p -D -m 755 tools/bin/sstabledump %{buildroot}%{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/sstabledump
install -p -D -m 755 tools/bin/sstableexpiredblockers %{buildroot}%{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/sstableexpiredblockers
install -p -D -m 755 tools/bin/sstablelevelreset %{buildroot}%{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/sstablelevelreset
install -p -D -m 755 tools/bin/sstablemetadata %{buildroot}%{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/sstablemetadata
install -p -D -m 755 tools/bin/sstableofflinerelevel %{buildroot}%{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/sstableofflinerelevel
install -p -D -m 755 tools/bin/sstablerepairedset %{buildroot}%{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/sstablerepairedset
install -p -D -m 755 tools/bin/sstablesplit %{buildroot}%{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/sstablesplit
install -p -D -m 755 build/tools/lib/%{pkg_name}-stress.jar %{buildroot}%{?scl:%{_root_javadir}}%{!?scl:%{_javadir}}/%{pkg_name}-stress.jar
install -p -D -m 755 tools/bin/%{pkg_name}-stress %{buildroot}%{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/%{pkg_name}-stress
install -p -D -m 755 tools/bin/%{pkg_name}-stressd %{buildroot}%{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/%{pkg_name}-stressd

# install cassandrad.service
install -p -D -m 644 "%{SOURCE2}"  %{buildroot}%{?scl:%{_root_unitdir}}%{!?scl:%{_unitdir}}/%{pkg_name}d.service

%pre
getent group %{pkg_name} >/dev/null || groupadd -f -g %{allocated_gid} -r %{pkg_name}
if ! getent passwd %{pkg_name} >/dev/null ; then
  if ! getrnt passwd %{allocated_uid} >/dev/null ; then
    useradd -r -u %{allocated_uid} -g %{pkg_name} -d %{?scl:%{_root_sharedstatedir}}%{!?scl:%{_sharedstatedir}}/%{pkg_name} \
      -s /sbin/nologin -c "Cassandra Database Server" %{pkg_name}
  else
    useradd -r -g %{pkg_name} -d %{?scl:%{_root_sharedstatedir}}%{!?scl:%{_sharedstatedir}}/%{pkg_name} -s /sbin/nologin \
      -c "Cassandra Database Server" %{pkg_name}
  fi
fi
exit 0

%files -f .mfiles
%doc README.asc CHANGES.txt NEWS.txt
%license LICENSE.txt NOTICE.txt
# just for testing
#%dir %%attr(755, %%{pkg_name}, root) %%{?scl:%%{_root_sharedstatedir}}%%{!?scl:%%{_sharedstatedir}}/%%{pkg_name}
#%dir %%attr(750, %%{pkg_name}, root) %%{?scl:%%{_root_localstatedir}}%%{!?scl:%%{_localstatedir}}/log/%%{pkg_name}
%dir %attr(755, trepik, root) %{?scl:%{_root_sharedstatedir}}%{!?scl:%{_sharedstatedir}}/%{pkg_name}
%dir %attr(750, trepik, root) %{?scl:%{_root_localstatedir}}%{!?scl:%{_localstatedir}}/log/%{pkg_name}
%attr(755, root, root) %{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/%{pkg_name}
%attr(755, root, root) %{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/%{pkg_name}.in.sh
%config(noreplace) %{?scl:%{_root_sysconfdir}}%{!?scl:%{_sysconfdir}}/%{pkg_name}-env.sh
%config(noreplace) %{?scl:%{_root_sysconfdir}}%{!?scl:%{_sysconfdir}}/%{pkg_name}.yaml
#%config(noreplace) %%{?scl:%%{_root_sysconfdir}}%%{!?scl:%%{_sysconfdir}}/%%{pkg_name}-rackdc.properties
#%config(noreplace) %%{?scl:%%{_root_sysconfdir}}%%{!?scl:%%{_sysconfdir}}/%%{pkg_name}-topology.properties
#%config(noreplace) %%{?scl:%%{_root_sysconfdir}}%%{!?scl:%%{_sysconfdir}}/commitlog_archiving.properties
%config(noreplace) %{?scl:%{_root_sysconfdir}}%{!?scl:%{_sysconfdir}}/jvm.options
%config(noreplace) %{?scl:%{_root_sysconfdir}}%{!?scl:%{_sysconfdir}}/logback-tools.xml
%config(noreplace) %{?scl:%{_root_sysconfdir}}%{!?scl:%{_sysconfdir}}/logback.xml
#%config(noreplace) %%{?scl:%%{_root_sysconfdir}}%%{!?scl:%%{_sysconfdir}}/metrics-reporter-config-sample.yaml
%config(noreplace) %{?scl:%{_root_sysconfdir}}%{!?scl:%{_sysconfdir}}/logrotate.d/%{pkg_name}
%{?scl:%{_root_unitdir}}%{!?scl:%{_unitdir}}/%{pkg_name}d.service

%files parent -f .mfiles-%{pkg_name}-parent
%license LICENSE.txt NOTICE.txt

%files thrift -f .mfiles-%{pkg_name}-thrift
%license LICENSE.txt NOTICE.txt

%files clientutil -f .mfiles-%{pkg_name}-clientutil
%doc conf/cqlshrc.sample
%license LICENSE.txt NOTICE.txt
%attr(755, root, root) %{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/cqlsh
%{python2_sitearch}/cqlshlib
%{python2_sitearch}/%{pkg_name}_pylib-0.0.0-py%{python2_version}.egg-info
%attr(755, root, root) %{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/nodetool
%attr(755, root, root) %{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/sstableloader
%attr(755, root, root) %{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/sstablescrub
%attr(755, root, root) %{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/sstableupgrade
%attr(755, root, root) %{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/sstableutil
%attr(755, root, root) %{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/sstableverify
%attr(755, root, root) %{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/sstabledump
%attr(755, root, root) %{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/sstableexpiredblockers
%attr(755, root, root) %{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/sstablelevelreset
%attr(755, root, root) %{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/sstablemetadata
%attr(755, root, root) %{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/sstableofflinerelevel
%attr(755, root, root) %{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/sstablerepairedset
%attr(755, root, root) %{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/sstablesplit

%files stress  
%license LICENSE.txt NOTICE.txt
%attr(755, root, root) %{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/%{pkg_name}-stress
%attr(755, root, root) %{?scl:%{_root_javadir}}%{!?scl:%{_javadir}}/%{pkg_name}-stress.jar
%attr(755, root, root) %{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/%{pkg_name}-stressd
%attr(755, root, root) %{?scl:%{_root_bindir}}%{!?scl:%{_bindir}}/%{pkg_name}.in.sh

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog

