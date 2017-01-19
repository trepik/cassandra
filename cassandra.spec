%{?scl:%scl_package cassandra}
%{!?scl:%global pkg_name %{name}}

%global allocated_gid 143
%global allocated_uid 143

%global cqlsh_version 5.0.1

Name:		%{?scl_prefix}cassandra
Version:	3.9
Release:	2%{?dist}
Summary:	OpenSource database for high-scale application
# Apache (v2.0) BSD (3 clause):
# ./src/java/org/apache/cassandra/utils/vint/VIntCoding.java
License:	ASL 2.0 and BSD
URL:		http://cassandra.apache.org/
Source0:	https://github.com/apache/%{pkg_name}/archive/%{pkg_name}-%{version}.tar.gz
Source1:	%{pkg_name}.logrotate
Source2:	%{pkg_name}d.service
Source3:	%{pkg_name}-tmpfile
# pom files are not generated but used are the ones from mavencentral
# because of orphaned mavent-ant-task package doing the work in this case
# failed koji build: http://koji.fedoraproject.org/koji/taskinfo?taskID=15542960
Source4:	http://central.maven.org/maven2/org/apache/%{pkg_name}/%{pkg_name}-all/%{version}/%{pkg_name}-all-%{version}.pom
Source5:	http://central.maven.org/maven2/org/apache/%{pkg_name}/%{pkg_name}-thrift/%{version}/%{pkg_name}-thrift-%{version}.pom
Source6:	http://central.maven.org/maven2/org/apache/%{pkg_name}/%{pkg_name}-clientutil/%{version}/%{pkg_name}-clientutil-%{version}.pom
Source7:	http://central.maven.org/maven2/org/apache/%{pkg_name}/%{pkg_name}-parent/%{version}/%{pkg_name}-parent-%{version}.pom

# fix encoding, naming, classpaths and dependencies
Patch0:		%{pkg_name}-%{version}-build.patch
# airline0.7 imports fix in cassandra source, which is dependent on 0.6 version
# https://issues.apache.org/jira/browse/CASSANDRA-12994
Patch1:		%{pkg_name}-%{version}-airline0.7.patch
# modify installed scripts
Patch2:		%{pkg_name}-%{version}-scripts.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1340876
# remove "Open" infix from all hppc classes
# https://issues.apache.org/jira/browse/CASSANDRA-12995X
Patch3:		%{pkg_name}-%{version}-hppc.patch
# changes autoclosable issue with TTransport in thrift
# https://bugzilla.redhat.com/show_bug.cgi?id=1183877
Patch4:		%{pkg_name}-%{version}-thrift.patch
# add two more parameters for SubstituteLogger constructor in slf4j
# https://issues.apache.org/jira/browse/CASSANDRA-12996
Patch5:		%{pkg_name}-%{version}-slf4j.patch
# remove net.mintern:primitive as it will be removed in next upstream release
# https://github.com/apache/cassandra/commit/8f0d5a295d34972ef719574df4aa1b59bf9e8478
Patch6:		%{pkg_name}-%{version}-remove-primitive.patch

#BuildArchitectures:	noarch

%{?scl:Requires: %scl_runtime}
Requires(pre):	shadow-utils
Requires:	%{?scl_prefix}sigar
%{?systemd_ordering}
BuildRequires:	systemd
BuildRequires:	%{?scl_prefix_maven}maven-local
BuildRequires:	%{?scl_prefix_java_common}ant
BuildRequires:	%{?scl_prefix_java_common}ecj
BuildRequires:	%{?scl_prefix}jamm
BuildRequires:	%{?scl_prefix}stream-lib
BuildRequires:	%{?scl_prefix}metrics
BuildRequires:	%{?scl_prefix}metrics-jvm
BuildRequires:	%{?scl_prefix}json_simple
BuildRequires:	%{?scl_prefix}compile-command-annotations
BuildRequires:	%{?scl_prefix}jBCrypt
BuildRequires:	%{?scl_prefix}concurrent-trees
BuildRequires:	%{?scl_prefix}logback
BuildRequires:	%{?scl_prefix}metrics-reporter-config
BuildRequires:	%{?scl_prefix}compress-lzf
BuildRequires:	%{?scl_prefix}disruptor-thrift-server
BuildRequires:	%{?scl_prefix}airline
BuildRequires:	%{?scl_prefix}jmh
BuildRequires:	%{?scl_prefix}byteman
BuildRequires:	%{?scl_prefix}HdrHistogram
BuildRequires:	%{?scl_prefix}sigar-java
BuildRequires:	%{?scl_prefix}jackson
BuildRequires:	%{?scl_prefix}antlr3-tool
BuildRequires:	%{?scl_prefix}caffeine
BuildRequires:	%{?scl_prefix}hppc
# using high-scale-lib from stephenc, no Cassandra original
#BuildRequires:	 mvn(com.boundary:high-scale-lib)
BuildRequires:	%{?scl_prefix}high-scale-lib
# using repackaging of the snowball stemmer so that it's available on Maven Central 
#BuildRequires:	mvn(com.github.rholder:snowball-stemmer)
BuildRequires:	%{?scl_prefix}snowball-java
# probably won't need in the future
BuildRequires:	%{?scl_prefix}concurrentlinkedhashmap-lru
# in rh-maven33: 1.4.3, needed: 1.6.0
BuildRequires:	%{?scl_prefix_maven}jflex
# in rh-java-common: 1.7.4, needed: 1.7.7
BuildRequires:	%{?scl_prefix_java_common}log4j-over-slf4j
# in rh-java-common: 1.7.4, needed: 1.7.7
BuildRequires:	%{?scl_prefix_java_common}jcl-over-slf4j
# in rh-java-common: 1.9.2, needed: 1.9.4
BuildRequires:	%{?scl_prefix_java_common}ant-junit
# in rh-java-common: 4.0.28, needed: 4.0.39.Final
BuildRequires:	%{?scl_prefix_java_common}netty
# in cassandra39: 0.9.1, needed: 0.9.2
BuildRequires:	%{?scl_prefix}libthrift-java
# TODO
BuildRequires:	%{?scl_prefix}cassandra-java-driver
BuildRequires:	%{?scl_prefix}lz4-java
BuildRequires:	%{?scl_prefix}snappy-java
BuildRequires:	%{?scl_prefix}ohc
BuildRequires:	%{?scl_prefix}ohc-core-j8
# the SCL version of the package depends on rh-maven33 collection
#%{?scl:Requires: %%scl_require rh-maven33}

# temporarly removed as it is optional
# using hadoop-common instead of hadoop-core, no Cassandra original
#BuildRequires:	mvn(org.apache.hadoop:hadoop-core)
#BuildRequires:	hadoop-common
#BuildRequires:	hadoop-mapreduce

%description
Cassandra is a partitioned row store. Rows are organized into tables with
a required primary key. Partitioning means that Cassandra can distribute your
data across multiple machines in an application-transparent matter. Cassandra
will automatically re-partition as machines are added/removed from the cluster.
Row store means that like relational databases, Cassandra organizes data by
rows and columns. The Cassandra Query Language (CQL) is a close relative of SQL.

%package parent
Summary:	Parent POM for %{pkg_name}

%description parent
Parent POM for %{pkg_name}.

%package thrift
Summary:	Thrift for %{pkg_name}
Requires:	%{pkg_name} = %{version}-%{release}

%description thrift
Allows portable (across programming languages) access to the database. Thrift
accomplishes this by generated source code for the programming language in
question based on a Thrift IDL file describing the service.

%package clientutil
Summary:	Client utilities for %{pkg_name}
Requires:	%{pkg_name} = %{version}-%{release}

%description clientutil
Utilities usable by client for %{pkg_name}

# source codes of cqlshlib are not python3 compatible, therefore using python2
%package python2-cqlshlib
Summary:	Commandline interface for %{pkg_name}
BuildRequires:	python2-devel
BuildRequires:	Cython
Requires:	%{name} = %{version}-%{release}
Requires:	python2-cassandra-driver
Provides:	cqlsh = %{cqlsh_version}
%{?python_provide:%python_provide python2-cqlshlib}

%description python2-cqlshlib
Commandline client used to communicate with %{pkg_name} server.

%package stress
Summary:	Stress testing utility for %{pkg_name}
Requires:	%{pkg_name} = %{version}-%{release}

%description stress
The cassandra-stress tool is a Java-based stress testing utility
for benchmarking and load testing a Cassandra cluster.

%package javadoc
Summary:	Javadoc for %{pkg_name}

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
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

# copy pom files
mkdir build
cp -p %{SOURCE4} build/%{pkg_name}-%{version}.pom
cp -p %{SOURCE5} build/%{pkg_name}-thrift-%{version}.pom
cp -p %{SOURCE6} build/%{pkg_name}-clientutil-%{version}.pom
cp -p %{SOURCE7} build/%{pkg_name}-%{version}-parent.pom

# remove hadoop
rm src/java/org/apache/cassandra/client/RingCache.java
rm -r src/java/org/apache/cassandra/hadoop
rm test/unit/org/apache/cassandra/client/TestRingCache.java
rm test/unit/org/apache/cassandra/hadoop/ColumnFamilyInputFormatTest.java
# remove hadoop also from pom files
%pom_remove_dep -r org.apache.hadoop: build/%{pkg_name}-%{version}.pom
# remove shaded classifier in cassandra driver from pom files
%pom_xpath_remove "pom:dependencies/pom:dependency/pom:classifier" build/%{pkg_name}-%{version}.pom

# build jar repositories for dependencies
build-jar-repository lib antlr3
build-jar-repository lib stringtemplate4
build-jar-repository lib jsr-305
build-jar-repository lib commons-lang3
build-jar-repository lib libthrift
build-jar-repository lib slf4j/api
build-jar-repository lib guava
build-jar-repository lib jamm
build-jar-repository lib stream-lib
build-jar-repository lib metrics/metrics-core
build-jar-repository lib metrics/metrics-jvm
build-jar-repository lib json_simple
build-jar-repository lib antlr3-runtime
build-jar-repository lib compile-command-annotations
# https://bugzilla.redhat.com/show_bug.cgi?id=1308556
build-jar-repository lib high-scale-lib/high-scale-lib
build-jar-repository lib cassandra-java-driver/cassandra-driver-core
build-jar-repository lib netty/netty-all
build-jar-repository lib lz4-java
build-jar-repository lib snappy-java
build-jar-repository lib jBCrypt
build-jar-repository lib concurrentlinkedhashmap-lru
build-jar-repository lib ohc/ohc-core
# temporarly removed because it is optional
#build-jar-repository lib hadoop/hadoop-common
build-jar-repository lib snakeyaml
build-jar-repository lib jackson/jackson-core-asl
build-jar-repository lib jackson/jackson-mapper-asl
build-jar-repository lib ecj
build-jar-repository lib objectweb-asm/asm
build-jar-repository lib commons-math3
# temporarly removed because it is optional
#build-jar-repository lib hadoop/hadoop-mapreduce-client-core
build-jar-repository lib concurrent-trees
build-jar-repository lib hppc
build-jar-repository lib snowball-java
build-jar-repository lib logback/logback-classic
build-jar-repository lib logback/logback-core
build-jar-repository lib metrics-reporter-config/reporter-config
build-jar-repository lib metrics-reporter-config/reporter-config-base
build-jar-repository lib joda-time
build-jar-repository lib compress-lzf
build-jar-repository lib disruptor-thrift-server
build-jar-repository lib commons-cli
build-jar-repository lib airline
build-jar-repository lib jna
build-jar-repository lib sigar
# temporarly removed because it is optional
#build-jar-repository lib hadoop/hadoop-annotations
build-jar-repository lib jflex
build-jar-repository lib java_cup
build-jar-repository lib commons-codec
build-jar-repository lib caffeine
# test dependencies
build-jar-repository lib junit
build-jar-repository lib ant
build-jar-repository lib ant/ant-junit
build-jar-repository lib hamcrest/core
build-jar-repository lib apache-commons-io
build-jar-repository lib byteman/byteman-bmunit
build-jar-repository lib commons-collections
build-jar-repository lib jmh/jmh-core
build-jar-repository lib HdrHistogram
# binaries dependencies
build-jar-repository lib javax.inject

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
# remove primitive patch
%patch6 -p1

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
# update dependencies that are not correct in the downloaded pom files
%pom_change_dep com.boundary: com.github.stephenc.high-scale-lib: build/%{name}-%{version}.pom
%pom_change_dep com.github.rholder:snowball-stemmer org.tartarus:snowball build/%{name}-thrift-%{version}.pom

# remove primitve as a dependency
%pom_remove_dep -r :primitive build/%{pkg_name}-thrift-%{version}.pom

%mvn_package "org.apache.%{pkg_name}:%{pkg_name}-parent:pom:%{version}" parent
%mvn_package ":%{pkg_name}-thrift" thrift
%mvn_package ":%{pkg_name}-clientutil" clientutil
%mvn_package ":%{pkg_name}-stress" stress
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
ant jar javadoc -Drelease=true 
%{?scl:EOF}

# Build the cqlshlib Python module
pushd pylib
%py2_build
popd

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_artifact build/%{pkg_name}-%{version}-parent.pom
%mvn_artifact build/%{pkg_name}-%{version}.pom build/%{pkg_name}-%{version}.jar
%mvn_artifact build/%{pkg_name}-thrift-%{version}.pom build/%{pkg_name}-thrift-%{version}.jar
%mvn_artifact build/%{pkg_name}-clientutil-%{version}.pom build/%{pkg_name}-clientutil-%{version}.jar
%mvn_artifact org.apache.cassandra:%{pkg_name}-stress:%{version} build/tools/lib/%{pkg_name}-stress.jar

%mvn_install -J build/javadoc/
%{?scl:EOF}

# Install the cqlshlib Python module
pushd pylib
%py2_install
popd

# create data dir
mkdir -p %{buildroot}%{_sharedstatedir}/%{pkg_name}

# logs directory plus files
mkdir -p %{buildroot}%{_localstatedir}/log/%{pkg_name}
install -p -D -m 644 "%{SOURCE1}"  %{buildroot}%{_sysconfdir}/logrotate.d/%{pkg_name}
install -p -D -m 755 bin/%{pkg_name} %{buildroot}%{_bindir}/%{pkg_name}
install -p -D -m 755 bin/%{pkg_name}.in.sh %{buildroot}%{_datadir}/%{pkg_name}/%{pkg_name}.in.sh
install -p -D -m 755 conf/%{pkg_name}-env.sh %{buildroot}%{_datadir}/%{pkg_name}/%{pkg_name}-env.sh
install -p -D -m 644 conf/%{pkg_name}.yaml %{buildroot}%{_sysconfdir}/%{pkg_name}/%{pkg_name}.yaml
install -p -D -m 644 conf/jvm.options %{buildroot}%{_sysconfdir}/%{pkg_name}/jvm.options
install -p -D -m 644 conf/logback-tools.xml %{buildroot}%{_sysconfdir}/%{pkg_name}/logback-tools.xml
install -p -D -m 644 conf/logback.xml %{buildroot}%{_sysconfdir}/%{pkg_name}/logback.xml
install -p -D -m 755 bin/cqlsh.py %{buildroot}%{_bindir}/cqlsh
install -p -D -m 755 bin/nodetool %{buildroot}%{_bindir}/nodetool
install -p -D -m 755 bin/sstableloader %{buildroot}%{_bindir}/sstableloader
install -p -D -m 755 bin/sstablescrub %{buildroot}%{_bindir}/sstablescrub
install -p -D -m 755 bin/sstableupgrade %{buildroot}%{_bindir}/sstableupgrade
install -p -D -m 755 bin/sstableutil %{buildroot}%{_bindir}/sstableutil
install -p -D -m 755 bin/sstableverify %{buildroot}%{_bindir}/sstableverify
install -p -D -m 755 tools/bin/sstabledump %{buildroot}%{_bindir}/sstabledump
install -p -D -m 755 tools/bin/sstableexpiredblockers %{buildroot}%{_bindir}/sstableexpiredblockers
install -p -D -m 755 tools/bin/sstablelevelreset %{buildroot}%{_bindir}/sstablelevelreset
install -p -D -m 755 tools/bin/sstablemetadata %{buildroot}%{_bindir}/sstablemetadata
install -p -D -m 755 tools/bin/sstableofflinerelevel %{buildroot}%{_bindir}/sstableofflinerelevel
install -p -D -m 755 tools/bin/sstablerepairedset %{buildroot}%{_bindir}/sstablerepairedset
install -p -D -m 755 tools/bin/sstablesplit %{buildroot}%{_bindir}/sstablesplit
install -p -D -m 755 tools/bin/%{pkg_name}-stress %{buildroot}%{_bindir}/%{pkg_name}-stress
install -p -D -m 755 tools/bin/%{pkg_name}-stressd %{buildroot}%{_bindir}/%{pkg_name}-stressd

# install cassandrad.service
install -p -D -m 644 "%{SOURCE2}"  %{buildroot}%{_unitdir}/%{pkg_name}d.service

%pre
getent group %{pkg_name} >/dev/null || groupadd -f -g %{allocated_gid} -r %{pkg_name}
if ! getent passwd %{pkg_name} >/dev/null ; then
  if ! getrnt passwd %{allocated_uid} >/dev/null ; then
    useradd -r -u %{allocated_uid} -g %{pkg_name} -d %{_sharedstatedir}/%{pkg_name} \
      -s /sbin/nologin -c "Cassandra Database Server" %{pkg_name}
  else
    useradd -r -g %{pkg_name} -d %{_sharedstatedir}/%{pkg_name} -s /sbin/nologin \
      -c "Cassandra Database Server" %{pkg_name}
  fi
fi
exit 0

%post
%systemd_post %{pkg_name}d.service

%preun
%systemd_preun %{pkg_name}d.service

%postun
%systemd_postun_with_restart %{pkg_name}d.service

%files -f .mfiles
%doc README.asc CHANGES.txt NEWS.txt
%license LICENSE.txt NOTICE.txt
%dir %attr(755, %{pkg_name}, root) %{_sharedstatedir}/%{pkg_name}
%dir %attr(755, %{pkg_name}, root) %{_localstatedir}/log/%{pkg_name}
%{_bindir}/%{pkg_name}
%{_datadir}/%{pkg_name}/%{pkg_name}.in.sh
%{_datadir}/%{pkg_name}/%{pkg_name}-env.sh
%config(noreplace) %{_sysconfdir}/%{pkg_name}/%{pkg_name}.yaml
%config(noreplace) %{_sysconfdir}/%{pkg_name}/jvm.options
%config(noreplace) %{_sysconfdir}/%{pkg_name}/logback-tools.xml
%config(noreplace) %{_sysconfdir}/%{pkg_name}/logback.xml
%config(noreplace) %{_sysconfdir}/logrotate.d/%{pkg_name}
%{_unitdir}/%{pkg_name}d.service

%files parent -f .mfiles-parent
%license LICENSE.txt NOTICE.txt

%files thrift -f .mfiles-thrift
%license LICENSE.txt NOTICE.txt

%files clientutil -f .mfiles-clientutil
%license LICENSE.txt NOTICE.txt
%attr(755, root, root) %{_bindir}/nodetool
%attr(755, root, root) %{_bindir}/sstableloader
%attr(755, root, root) %{_bindir}/sstablescrub
%attr(755, root, root) %{_bindir}/sstableupgrade
%attr(755, root, root) %{_bindir}/sstableutil
%attr(755, root, root) %{_bindir}/sstableverify
%attr(755, root, root) %{_bindir}/sstabledump
%attr(755, root, root) %{_bindir}/sstableexpiredblockers
%attr(755, root, root) %{_bindir}/sstablelevelreset
%attr(755, root, root) %{_bindir}/sstablemetadata
%attr(755, root, root) %{_bindir}/sstableofflinerelevel
%attr(755, root, root) %{_bindir}/sstablerepairedset
%attr(755, root, root) %{_bindir}/sstablesplit

%files python2-cqlshlib
%doc conf/cqlshrc.sample
%license LICENSE.txt NOTICE.txt
%attr(755, root, root) %{_bindir}/cqlsh
%{python2_sitearch}/cqlshlib
%{python2_sitearch}/%{pkg_name}_pylib-0.0.0-py%{python2_version}.egg-info

%files stress -f .mfiles-stress
%license LICENSE.txt NOTICE.txt
%attr(755, root, root) %{_bindir}/%{pkg_name}-stress
%attr(755, root, root) %{_bindir}/%{pkg_name}-stressd
%{_datadir}/%{pkg_name}/%{pkg_name}.in.sh

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt NOTICE.txt

%changelog
* Wed Jan 18 2017 Tomas Repik <trepik@redhat.com> - 3.9-2
- fix paths so that one could run the server

* Thu Dec 01 2016 Tomas Repik <trepik@redhat.com> - 3.9-1
- initial package
