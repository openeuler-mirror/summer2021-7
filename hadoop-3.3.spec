# 定义全局变量，类似常量
%global _hardened_build 1

%global hadoop_version %{version}
# 类似数组
%global hdfs_services hadoop-zkfc.service hadoop-datanode.service hadoop-secondarynamenode.service hadoop-namenode.service hadoop-journalnode.service
%global mapreduce_services hadoop-historyserver.service
%global yarn_services hadoop-proxyserver.service hadoop-resourcemanager.service hadoop-nodemanager.service hadoop-timelineserver.service

# Filter out undesired provides and requires
%global __requires_exclude_from ^%{_libdir}/%{real_name}/libhadoop.so$
%global __provides_exclude_from ^%{_libdir}/%{real_name}/.*$
%define real_name hadoop
%define _binaries_in_noarch_packages_terminate_build 0
Name:   hadoop-3.3
Version: 3.3.0
Release: 1
Summary: A software platform for processing vast amounts of data
# The BSD license file is missing
# https://issues.apache.org/jira/browse/HADOOP-9849
License: Apache-2.0 and MIT and BSD-2-Clause and EPL and Zlib and MPL-2.0
URL:     https://%{real_name}.apache.org
Source0: https://www.apache.org/dist/%{real_name}/core/%{real_name}-%{version}/%{real_name}-%{version}-src.tar.gz
Source1: %{real_name}-layout.sh
Source2: %{real_name}-hdfs.service.template
Source3: %{real_name}-mapreduce.service.template
Source4: %{real_name}-yarn.service.template
Source5: context.xml
Source6: %{real_name}.logrotate
Source7: %{real_name}-httpfs.sysconfig
Source8: hdfs-create-dirs
Source9: %{real_name}-tomcat-users.xml
Source10: %{real_name}-core-site.xml
Source11: %{real_name}-hdfs-site.xml
Source12: %{real_name}-mapred-site.xml
Source13: %{real_name}-yarn-site.xml

Patch1: 0001-sys_errlist-undeclared.patch

# 编译需要的依赖
BuildRoot: %{_tmppath}/%{real_name}-%{version}-%{release}-root
BuildRequires: java-1.8.0-openjdk-devel maven hostname maven-local tomcat cmake snappy openssl-devel 
BuildRequires: cyrus-sasl-devel protobuf protobuf-c-compiler protobuf-c-devel protobuf-java
Buildrequires: chrpath systemd gcc-c++
# 运行时依赖
Requires: java-1.8.0-openjdk protobuf-java apache-zookeeper

%description
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

%package client
Summary: Libraries for Apache Hadoop clients
BuildArch: noarch
Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-hdfs = %{version}-%{release}
Requires: %{name}-mapreduce = %{version}-%{release}
Requires: %{name}-yarn = %{version}-%{release}

%description client
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package provides libraries for Apache Hadoop clients.

%package common
Summary: Common files needed by Apache Hadoop daemons
BuildArch: noarch
Requires(pre): /usr/sbin/useradd
Obsoletes: %{name}-javadoc < 2.4.1-22%{?dist}

Requires: apache-zookeeper
# 持久化的 key/value 存储 其后续产品为RocksDB
Requires: leveldb
Requires: protobuf-java

%description common
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package contains common files and utilities needed by other Apache
Hadoop modules.

%package common-native
Summary: The native Apache Hadoop library file
Requires: %{name}-common = %{version}-%{release}

%description common-native
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package contains the native-hadoop library

%package devel
Summary: Headers for Apache Hadoop
Requires: libhdfs%{?_isa} = %{version}-%{release}

%description devel
Header files for Apache Hadoop's hdfs library and other utilities

%package hdfs
Summary: The Apache Hadoop Distributed File System
BuildArch: noarch
#Requires: apache-commons-daemon-jsvc
#Requires: %{name}-common = %{version}-%{release}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description hdfs
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

The Hadoop Distributed File System (HDFS) is the primary storage system
used by Apache Hadoop applications.


%package httpfs
Summary: Provides web access to HDFS
BuildArch: noarch
# Apache Commons DataBase Pooling Package
Requires: apache-commons-dbcp
# the Eclipse Compiler for Java
Requires: ecj >= 1:4.2.1-6
# Simple Java toolkit for JSON
Requires: json_simple
# Implementation of the Java Servlet, JavaServer Pages, Java Expression Language and Java WebSocket technologies
Requires: tomcat
Requires: tomcat-lib
# Java Native Interface
# JNI wrappers for Apache Portable Runtime for Tomcat
Requires: tcnative
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description httpfs
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package provides a server that provides HTTP REST API support for
the complete FileSystem/FileContext interface in HDFS.

%package -n libhdfs
Summary: The Apache Hadoop Filesystem Library
Requires: %{name}-hdfs = %{version}-%{release}
#Requires: lzo

%description -n libhdfs
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package provides the Apache Hadoop Filesystem Library.

%package mapreduce
Summary: Apache Hadoop MapReduce (MRv2)
BuildArch: noarch
Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-mapreduce-examples = %{version}-%{release}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description mapreduce
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package provides Apache Hadoop MapReduce (MRv2).

%package mapreduce-examples
Summary: Apache Hadoop MapReduce (MRv2) examples
BuildArch: noarch
#Requires: hsqldb

%description mapreduce-examples
This package contains mapreduce examples.

%package maven-plugin
Summary: Apache Hadoop maven plugin
BuildArch: noarch
Requires: maven

%description maven-plugin
The Apache Hadoop maven plugin

%package tests
Summary: Apache Hadoop test resources
BuildArch: noarch
Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-hdfs = %{version}-%{release}
Requires: %{name}-mapreduce = %{version}-%{release}
Requires: %{name}-yarn = %{version}-%{release}

%description tests
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package contains test related resources for Apache Hadoop.

%package yarn
BuildArch: noarch
Summary: Apache Hadoop YARN
Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-mapreduce = %{version}-%{release}
# A standards for Java/J2EE AOP
Requires: aopalliance
# Java API for JSR-330 Dependency Injection
Requires: atinject
# Hamcrest框架，Hamcest提供了一套匹配符Matcher，这些匹配符更接近自然语言，用于测试
# Hamcrest matchers for Python
Requires: hamcrest
# HawtJNI is a code generator that produces the JNI code needed to implement java native methods.
# Produces the JNI code,known as a code generator
Requires: hawtjni
Requires: leveldbjni
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description yarn
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package contains Apache Hadoop YARN.

%package yarn-security
Summary: The ability to run Apache Hadoop YARN in secure mode
Requires: %{name}-yarn = %{version}-%{release}

%description yarn-security
Apache Hadoop is a framework that allows for the distributed processing of
large data sets across clusters of computers using simple programming models.
It is designed to scale up from single servers to thousands of machines, each
offering local computation and storage.

This package contains files needed to run Apache Hadoop YARN in secure mode.

%prep
%autosetup -p1 -n %{real_name}-%{version}-src
%build
mvn -Pdist,native -DskipTests -DskipIT -Dmaven.javadoc.skip=true package

%install
# Copy all jar files except those generated by the build
# $1 the src directory
# $2 the dest directory
copy_dep_jars()
{
  find $1 ! -name "hadoop-*.jar" -name "*.jar" | xargs install -m 0644 -t $2
  rm -f $2/tools-*.jar
}

# Create symlinks for jars from the build
# $1 the location to create the symlink
link_hadoop_jars()
{
  for f in `ls hadoop-* | grep -v tests | grep -v examples`
  do
    n=`echo $f | sed "s/-%{version}//" | sed "s/-1.0.0//"` 
    if [ -L $1/$n ]
    then
      continue
    elif [ -e $1/$f ]
    then
      rm -f $1/$f $1/$n
    fi
    p=`find %{buildroot}%{_jnidir} %{buildroot}%{_javadir}/%{real_name} -name $n | sed "s#%{buildroot}##"`
    %{__ln_s} $p $1/$n
  done
}

%mvn_install

install -d -m 0755 %{buildroot}%{_libdir}/%{real_name}
install -d -m 0755 %{buildroot}%{_includedir}/%{real_name}
install -d -m 0755 %{buildroot}%{_jnidir}/%{real_name}

install -d -m 0755 %{buildroot}%{_datadir}/%{real_name}/client/lib
install -d -m 0755 %{buildroot}%{_datadir}/%{real_name}/common/lib
install -d -m 0755 %{buildroot}%{_datadir}/%{real_name}/hdfs/lib
install -d -m 0755 %{buildroot}%{_datadir}/%{real_name}/hdfs/webapps
install -d -m 0755 %{buildroot}%{_datadir}/%{real_name}/httpfs/tomcat/webapps
install -d -m 0755 %{buildroot}%{_datadir}/%{real_name}/mapreduce/lib
install -d -m 0755 %{buildroot}%{_datadir}/%{real_name}/yarn/lib
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{real_name}/tomcat/Catalina/localhost
install -d -m 0755 %{buildroot}%{_sysconfdir}/logrotate.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/sysconfig
install -d -m 0755 %{buildroot}%{_tmpfilesdir}
install -d -m 0755 %{buildroot}%{_sharedstatedir}/%{real_name}-hdfs
install -d -m 0755 %{buildroot}%{_sharedstatedir}/tomcats/httpfs
install -d -m 0755 %{buildroot}%{_var}/cache/%{real_name}-yarn
install -d -m 0755 %{buildroot}%{_var}/cache/%{real_name}-httpfs/temp
install -d -m 0755 %{buildroot}%{_var}/cache/%{real_name}-httpfs/work
install -d -m 0755 %{buildroot}%{_var}/cache/%{real_name}-mapreduce
install -d -m 0755 %{buildroot}%{_var}/log/%{real_name}-yarn
install -d -m 0755 %{buildroot}%{_var}/log/%{real_name}-hdfs
install -d -m 0755 %{buildroot}%{_var}/log/%{real_name}-httpfs
install -d -m 0755 %{buildroot}%{_var}/log/%{real_name}-mapreduce
install -d -m 0755 %{buildroot}%{_var}/run/%{real_name}-yarn
install -d -m 0755 %{buildroot}%{_var}/run/%{real_name}-hdfs
install -d -m 0755 %{buildroot}%{_var}/run/%{real_name}-mapreduce

basedir='%{real_name}-common-project/%{real_name}-common/target/%{real_name}-common-%{hadoop_version}'
hdfsdir='%{real_name}-hdfs-project/%{real_name}-hdfs/target/%{real_name}-hdfs-%{hadoop_version}'
httpfsdir='%{real_name}-hdfs-project/%{real_name}-hdfs-httpfs/target/%{real_name}-hdfs-httpfs-%{hadoop_version}'
mapreddir='%{real_name}-mapreduce-project/target/%{real_name}-mapreduce-%{hadoop_version}'
yarndir='%{real_name}-yarn-project/target/%{real_name}-yarn-project-%{hadoop_version}'

# copy jar package
install -d -m 0755 %{buildroot}%{_datadir}/java/%{real_name}
install -d -m 0755 %{buildroot}%{_datadir}/maven-poms/%{real_name}
# client
install -m 0755 %{real_name}-client-modules/%{real_name}-client/target/hadoop-client-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-client.jar
echo %{_datadir}/java/%{real_name}/hadoop-client.jar >> .mfiles-hadoop-client 
install -m 0755 %{real_name}-client-modules/%{real_name}-client-api/target/hadoop-client-api-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-client-api.jar
echo %{_datadir}/java/%{real_name}/hadoop-client-api.jar >> .mfiles-hadoop-client
install -m 0755 %{real_name}-client-modules/%{real_name}-client-minicluster/target/hadoop-client-minicluster-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-client-minicluster.jar
echo %{_datadir}/java/%{real_name}/hadoop-client-minicluster.jar >> .mfiles-hadoop-client
install -m 0755 %{real_name}-client-modules/%{real_name}-client-runtime/target/hadoop-client-runtime-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-client-runtime.jar
echo %{_datadir}/java/%{real_name}/hadoop-client-runtime.jar >> .mfiles-hadoop-client
# this is special but it occurs too many times
# mv hadoop-client-modules/%{real_name}-client/target/%{real_name}-client-%{hadoop_version}/share/%{real_name}/client/lib/hadoop-shaded-protobuf_3_7-1.0.0.jar hadoop-client-modules/%{real_name}-client/target/%{real_name}-client-%{version}/share/%{real_name}/client/lib/hadoop-shaded-protobuf_3_7-3.3.0.jar
install -m 0755 hadoop-client-modules/%{real_name}-client/target/%{real_name}-client-%{hadoop_version}/share/%{real_name}/client/lib/hadoop-shaded-protobuf_3_7-1.0.0.jar %{buildroot}%{_javadir}/%{real_name}/hadoop-shaded-protobuf_3_7.jar
echo %{_datadir}/java/%{real_name}/hadoop-shaded-protobuf_3_7.jar >> .mfiles-hadoop-client

# common
install -m 0755 %{real_name}-common-project/%{real_name}-common/target/hadoop-common-%{version}.jar %{buildroot}%{_prefix}/lib/java/hadoop/hadoop-common.jar
echo %{_prefix}/lib/java/hadoop/hadoop-common.jar >> .mfiles
install -m 0755 %{real_name}-common-project/%{real_name}-kms/target/hadoop-kms-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-kms.jar
echo %{_datadir}/java/%{real_name}/hadoop-kms.jar >> .mfiles
install -m 0755 %{real_name}-common-project/%{real_name}-nfs/target/hadoop-nfs-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-nfs.jar
echo %{_datadir}/java/%{real_name}/hadoop-nfs.jar >> .mfiles
install -m 0755 %{real_name}-common-project/%{real_name}-registry/target/hadoop-registry-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-registry.jar
echo %{_datadir}/java/%{real_name}/hadoop-registry.jar >> .mfiles

echo %{_sysconfdir}/%{real_name}/hadoop-user-functions.sh.example >> .mfiles
echo %{_sysconfdir}/%{real_name}/shellprofile.d/example.sh >> .mfiles
echo %{_sysconfdir}/%{real_name}/workers >> .mfiles
echo %{_prefix}/libexec/hadoop-functions.sh >> .mfiles
echo %{_prefix}/libexec/hadoop-layout.sh.example >> .mfiles
echo %{_prefix}/sbin/workers.sh >> .mfiles
echo %{_datadir}/%{real_name}/common/hadoop-common.jar >> .mfiles

install -m 0755 %{real_name}-common-project/%{real_name}-annotations/target/hadoop-annotations-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-annotations.jar
echo %{_datadir}/java/%{real_name}/hadoop-annotations.jar >> .mfiles
install -m 0755 %{real_name}-common-project/%{real_name}-auth/target/hadoop-auth-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-auth.jar
echo %{_datadir}/java/%{real_name}/hadoop-auth.jar >> .mfiles
install -m 0755 %{real_name}-tools/%{real_name}-aws/target/hadoop-aws-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-aws.jar
echo %{_datadir}/java/%{real_name}/hadoop-aws.jar >> .mfiles
install -m 0755 %{real_name}-build-tools/target/hadoop-build-tools-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-build-tools.jar
echo %{_datadir}/java/%{real_name}/hadoop-build-tools.jar >> .mfiles

# hdfs
install -m 0755 %{real_name}-hdfs-project/%{real_name}-hdfs/target/hadoop-hdfs-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-hdfs.jar
echo %{_datadir}/java/%{real_name}/hadoop-hdfs.jar >> .mfiles-hadoop-hdfs
install -m 0755 %{real_name}-hdfs-project/%{real_name}-hdfs-client/target/hadoop-hdfs-client-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-hdfs-client.jar
echo %{_datadir}/java/%{real_name}/hadoop-hdfs-client.jar >> .mfiles-hadoop-hdfs
install -m 0755 %{real_name}-hdfs-project/%{real_name}-hdfs-httpfs/target/hadoop-hdfs-httpfs-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-hdfs-httpfs.jar
echo %{_datadir}/java/%{real_name}/hadoop-hdfs-httpfs.jar >> .mfiles-hadoop-hdfs
install -m 0755 %{real_name}-hdfs-project/%{real_name}-hdfs-native-client/target/hadoop-hdfs-native-client-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-hdfs-native-client.jar
echo %{_datadir}/java/%{real_name}/hadoop-hdfs-native-client.jar >> .mfiles-hadoop-hdfs
install -m 0755 %{real_name}-hdfs-project/%{real_name}-hdfs-nfs/target/hadoop-hdfs-nfs-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-hdfs-nfs.jar
echo %{_datadir}/java/%{real_name}/hadoop-hdfs-nfs.jar >> .mfiles-hadoop-hdfs
install -m 0755 %{real_name}-hdfs-project/%{real_name}-hdfs-rbf/target/hadoop-hdfs-rbf-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-hdfs-rbf.jar
echo %{_datadir}/java/%{real_name}/hadoop-hdfs-rbf.jar >> .mfiles-hadoop-hdfs

echo %{_prefix}/libexec/shellprofile.d/hadoop-hdfs.sh >> .mfiles-hadoop-hdfs
# mapreduce
install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-app/target/hadoop-mapreduce-client-app-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-mapreduce-client-app.jar
echo %{_datadir}/java/%{real_name}/hadoop-mapreduce-client-app.jar >> .mfiles-hadoop-mapreduce

install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-common/target/hadoop-mapreduce-client-common-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-mapreduce-client-common.jar
echo %{_datadir}/java/%{real_name}/hadoop-mapreduce-client-common.jar >> .mfiles-hadoop-mapreduce

install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-core/target/hadoop-mapreduce-client-core-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-mapreduce-client-core.jar 
echo %{_datadir}/java/%{real_name}/hadoop-mapreduce-client-core.jar >> .mfiles-hadoop-mapreduce

install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-hs-plugins/target/hadoop-mapreduce-client-hs-plugins-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-mapreduce-client-hs-plugins.jar
echo %{_datadir}/java/%{real_name}/hadoop-mapreduce-client-hs-plugins.jar >> .mfiles-hadoop-mapreduce

install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-hs/target/hadoop-mapreduce-client-hs-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-mapreduce-client-hs.jar
echo %{_datadir}/java/%{real_name}/hadoop-mapreduce-client-hs.jar >> .mfiles-hadoop-mapreduce

install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-jobclient/target/hadoop-mapreduce-client-jobclient-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-mapreduce-client-jobclient.jar
echo %{_datadir}/java/%{real_name}/hadoop-mapreduce-client-jobclient.jar >> .mfiles-hadoop-mapreduce

install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-shuffle/target/hadoop-mapreduce-client-shuffle-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-mapreduce-client-shuffle.jar
echo %{_datadir}/java/%{real_name}/hadoop-mapreduce-client-shuffle.jar >> .mfiles-hadoop-mapreduce

install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-uploader/target/hadoop-mapreduce-client-uploader-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-mapreduce-client-uploader.jar
echo %{_datadir}/java/%{real_name}/hadoop-mapreduce-client-uploader.jar >> .mfiles-hadoop-mapreduce 

echo %{_prefix}/libexec/shellprofile.d/hadoop-mapreduce.sh >> .mfiles-hadoop-mapreduce

install -m 0755 %{real_name}-tools/%{real_name}-archives/target/hadoop-archives-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-archives.jar
echo %{_datadir}/java/%{real_name}/hadoop-archives.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-datajoin/target/hadoop-datajoin-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-datajoin.jar
echo %{_datadir}/java/%{real_name}/hadoop-datajoin.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-distcp/target/hadoop-distcp-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-distcp.jar
echo %{_datadir}/java/%{real_name}/hadoop-distcp.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-extras/target/hadoop-extras-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-extras.jar
echo %{_datadir}/java/%{real_name}/hadoop-extras.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-gridmix/target/hadoop-gridmix-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-gridmix.jar
echo %{_datadir}/java/%{real_name}/hadoop-gridmix.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-openstack/target/hadoop-openstack-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-openstack.jar
echo %{_datadir}/java/%{real_name}/hadoop-openstack.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-rumen/target/hadoop-rumen-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-rumen.jar
echo %{_datadir}/java/%{real_name}/hadoop-rumen.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-sls/target/hadoop-sls-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-sls.jar
echo %{_datadir}/java/%{real_name}/hadoop-sls.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-streaming/target/hadoop-streaming-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-streaming.jar
echo %{_datadir}/java/%{real_name}/hadoop-streaming.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-tools/%{real_name}-tools-dist/target/hadoop-tools-dist-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-tools-dist.jar
echo %{_datadir}/java/%{real_name}/hadoop-tools-dist.jar >> .mfiles-hadoop-mapreduce
install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-nativetask/target/hadoop-mapreduce-client-nativetask-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-mapreduce-client-nativetask.jar
echo %{_datadir}/java/%{real_name}/hadoop-mapreduce-client-nativetask.jar >> .mfiles-hadoop-mapreduce



# mapreduce-examples
install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-examples/target/hadoop-mapreduce-examples-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-mapreduce-examples.jar
echo %{_datadir}/java/%{real_name}/hadoop-mapreduce-examples.jar >> .mfiles-hadoop-mapreduce-examples
install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-examples/pom.xml %{buildroot}%{_datadir}/maven-poms/%{real_name}/hadoop-mapreduce-examples.pom
echo %{_datadir}/maven-poms/%{real_name}/hadoop-mapreduce-examples.pom >> .mfiles-hadoop-mapreduce-examples

# maven-plugin
install -m 0755 %{real_name}-maven-plugins/target/hadoop-maven-plugins-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-maven-plugins.jar
echo %{_datadir}/java/%{real_name}/hadoop-maven-plugins.jar >> .mfiles-hadoop-maven-plugin

# tests
install -m 0755 %{real_name}-client-modules/%{real_name}-client/target/hadoop-client-%{version}-tests.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-client-tests.jar
echo %{_datadir}/java/%{real_name}/hadoop-client-tests.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-common-project/%{real_name}-common/target/hadoop-common-%{version}-tests.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-common-tests.jar
echo %{_datadir}/java/%{real_name}/hadoop-common-tests.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-hdfs-project/%{real_name}-hdfs/target/hadoop-hdfs-%{version}-tests.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-hdfs-tests.jar
echo %{_datadir}/java/%{real_name}/hadoop-hdfs-tests.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-app/target/hadoop-mapreduce-client-app-%{version}-tests.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-mapreduce-client-app-tests.jar
echo %{_datadir}/java/%{real_name}/hadoop-mapreduce-client-app-tests.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-jobclient/target/hadoop-mapreduce-client-jobclient-%{version}-tests.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-mapreduce-client-jobclient-tests.jar
echo %{_datadir}/java/%{real_name}/hadoop-mapreduce-client-jobclient-tests.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-minicluster/target/hadoop-minicluster-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-minicluster.jar
echo %{_datadir}/java/%{real_name}/hadoop-minicluster.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-tools/%{real_name}-tools-dist/target/hadoop-tools-dist-%{version}-tests.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-tools-dist-tests.jar
echo %{_datadir}/java/%{real_name}/hadoop-tools-dist-tests.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-common/target/hadoop-yarn-common-%{version}-tests.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-common-tests.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-common-tests.jar >> .mfiles-hadoop-tests
#install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-registry/target/hadoop-yarn-registry-%{version}-tests.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-registry-tests.jar
#echo %{_datadir}/java/%{real_name}/hadoop-yarn-registry-tests.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-resourcemanager/target/hadoop-yarn-server-resourcemanager-%{version}-tests.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-server-resourcemanager-tests.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-resourcemanager-tests.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-sharedcachemanager/target/hadoop-yarn-server-sharedcachemanager-%{version}-tests.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-server-sharedcachemanager-tests.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-sharedcachemanager-tests.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-tests/target/hadoop-yarn-server-tests-%{version}-tests.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-server-tests-tests.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-tests-tests.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-tests/target/hadoop-yarn-server-tests-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-server-tests.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-tests.jar >> .mfiles-hadoop-tests
install -m 0755 %{real_name}-hdfs-project/%{real_name}-hdfs-client/target/hadoop-hdfs-client-%{version}-tests.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-hdfs-client-tests.jar
echo %{_datadir}/java/%{real_name}/hadoop-hdfs-client-tests.jar >> .mfiles-hadoop-tests
# yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-api/target/hadoop-yarn-api-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-api.jar 
echo %{_datadir}/java/%{real_name}/hadoop-yarn-api.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/target/%{real_name}-yarn-project-%{version}/share/%{real_name}/yarn/hadoop-yarn-applications-catalog-webapp-3.3.0.war %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-applications-catalog-webapp.war
echo %{_datadir}/java/%{real_name}/hadoop-yarn-applications-catalog-webapp.war >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-applications/%{real_name}-yarn-applications-distributedshell/target/hadoop-yarn-applications-distributedshell-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-applications-distributedshell.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-applications-distributedshell.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/target/%{real_name}-yarn-project-%{version}/share/%{real_name}/yarn/hadoop-yarn-applications-mawo-core-3.3.0.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-applications-mawo-core.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-applications-mawo-core.jar  >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-applications/%{real_name}-yarn-applications-unmanaged-am-launcher/target/hadoop-yarn-applications-unmanaged-am-launcher-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-applications-unmanaged-am-launcher.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-applications-unmanaged-am-launcher.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-client/target/hadoop-yarn-client-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-client.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-client.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-common/target/hadoop-yarn-common-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-common.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-common.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-registry/target/hadoop-yarn-registry-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-registry.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-registry.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-applicationhistoryservice/target/hadoop-yarn-server-applicationhistoryservice-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-server-applicationhistoryservice.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-applicationhistoryservice.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-common/target/hadoop-yarn-server-common-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-server-common.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-common.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-nodemanager/target/hadoop-yarn-server-nodemanager-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-server-nodemanager.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-nodemanager.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-resourcemanager/target/hadoop-yarn-server-resourcemanager-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-server-resourcemanager.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-resourcemanager.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-router/target/hadoop-yarn-server-router-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-server-router.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-router.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-sharedcachemanager/target/hadoop-yarn-server-sharedcachemanager-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-server-sharedcachemanager.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-sharedcachemanager.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-timeline-pluginstorage/target/hadoop-yarn-server-timeline-pluginstorage-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-server-timeline-pluginstorage.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-timeline-pluginstorage.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-web-proxy/target/hadoop-yarn-server-web-proxy-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-server-web-proxy.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-web-proxy.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-applications/%{real_name}-yarn-services/%{real_name}-yarn-services-api/target/hadoop-yarn-services-api-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-services-api.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-services-api.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-applications/%{real_name}-yarn-services/%{real_name}-yarn-services-core/target/hadoop-yarn-services-core-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-services-core.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-services-core.jar >> .mfiles-hadoop-yarn

echo %{_sysconfdir}/%{real_name}/yarnservice-log4j.properties >> .mfiles-hadoop-yarn
echo %{_prefix}/bin/container-executor >> .mfiles-hadoop-yarn
echo %{_prefix}/bin/test-container-executor >> .mfiles-hadoop-yarn
echo %{_prefix}/libexec/shellprofile.d/hadoop-yarn.sh >> .mfiles-hadoop-yarn
echo %{_prefix}/sbin/FederationStateStore/* >> .mfiles-hadoop-yarn


install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-timelineservice/target/hadoop-yarn-server-timelineservice-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-server-timelineservice.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-timelineservice.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-timelineservice-hbase/%{real_name}-yarn-server-timelineservice-hbase-client/target/hadoop-yarn-server-timelineservice-hbase-client-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-server-timelineservice-hbase-client.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-timelineservice-hbase-client.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-timelineservice-hbase/%{real_name}-yarn-server-timelineservice-hbase-common/target/hadoop-yarn-server-timelineservice-hbase-common-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-server-timelineservice-hbase-common.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-timelineservice-hbase-common.jar >> .mfiles-hadoop-yarn
install -m 0755 %{real_name}-yarn-project/target/%{real_name}-yarn-project-%{version}/share/%{real_name}/yarn/timelineservice/hadoop-yarn-server-timelineservice-hbase-coprocessor-%{version}.jar %{buildroot}%{_datadir}/java/%{real_name}/hadoop-yarn-server-timelineservice-hbase-coprocessor.jar
echo %{_datadir}/java/%{real_name}/hadoop-yarn-server-timelineservice-hbase-coprocessor.jar >> .mfiles-hadoop-yarn


# copy script folders
for dir in bin libexec sbin
do
  cp -arf $basedir/$dir %{buildroot}%{_prefix}
  cp -arf $hdfsdir/$dir %{buildroot}%{_prefix}
  cp -arf $mapreddir/$dir %{buildroot}%{_prefix}
  cp -arf $yarndir/$dir %{buildroot}%{_prefix}
done

# This binary is obsoleted and causes a conflict with qt-devel
rm -rf %{buildroot}%{_bindir}/rcc

# Duplicate files
rm -f %{buildroot}%{_sbindir}/hdfs-config.sh

# copy config files
cp -arf $basedir/etc/* %{buildroot}%{_sysconfdir}
cp -arf $httpfsdir/etc/* %{buildroot}%{_sysconfdir}
cp -arf $mapreddir/etc/* %{buildroot}%{_sysconfdir}
cp -arf $yarndir/etc/* %{buildroot}%{_sysconfdir}

# copy binaries
cp -arf $basedir/lib/native/libhadoop.so* %{buildroot}%{_libdir}/%{real_name}
chrpath --delete %{buildroot}%{_libdir}/%{real_name}/*
cp -arf ./hadoop-hdfs-project/hadoop-hdfs-native-client/target/hadoop-hdfs-native-client-%{version}/include/hdfs.h %{buildroot}%{_includedir}/%{real_name}
cp -arf ./hadoop-hdfs-project/hadoop-hdfs-native-client/target/hadoop-hdfs-native-client-%{version}/lib/native/libhdfs.so* %{buildroot}%{_libdir}
chrpath --delete %{buildroot}%{_libdir}/libhdfs*

# Not needed since httpfs is deployed with existing systemd setup
rm -f %{buildroot}%{_sbindir}/httpfs.sh
rm -f %{buildroot}%{_libexecdir}/httpfs-config.sh
rm -f %{buildroot}%{_bindir}/httpfs-env.sh

# Remove files with .cmd extension
find %{buildroot} -name *.cmd | xargs rm -f 

# Modify hadoop-env.sh to point to correct locations for JAVA_HOME
# and JSVC_HOME.
# in fact, not useful
sed -i "s|\${JAVA_HOME}|/usr/lib/jvm/jre|" %{buildroot}%{_sysconfdir}/%{real_name}/%{real_name}-env.sh
sed -i "s|\${JSVC_HOME}|/usr/bin|" %{buildroot}%{_sysconfdir}/%{real_name}/%{real_name}-env.sh

# Ensure the java provided DocumentBuilderFactory is used
sed -i "s|\(HADOOP_OPTS.*=.*\)\$HADOOP_CLIENT_OPTS|\1 -Djavax.xml.parsers.DocumentBuilderFactory=com.sun.org.apache.xerces.internal.jaxp.DocumentBuilderFactoryImpl \$HADOOP_CLIENT_OPTS|" %{buildroot}%{_sysconfdir}/%{real_name}/%{real_name}-env.sh
echo "export YARN_OPTS=\"\$YARN_OPTS -Djavax.xml.parsers.DocumentBuilderFactory=com.sun.org.apache.xerces.internal.jaxp.DocumentBuilderFactoryImpl\"" >> %{buildroot}%{_sysconfdir}/%{real_name}/yarn-env.sh

# Workaround for bz1012059
install -d -m 0755 %{buildroot}%{_mavenpomdir}/
install -pm 644 hadoop-project-dist/pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{real_name}-%{real_name}-project-dist.pom
%{__ln_s} %{_jnidir}/%{real_name}/hadoop-common.jar %{buildroot}%{_datadir}/%{real_name}/common
%{__ln_s} %{_javadir}/%{real_name}/hadoop-hdfs.jar %{buildroot}%{_datadir}/%{real_name}/hdfs
%{__ln_s} %{_javadir}/%{real_name}/hadoop-client.jar %{buildroot}%{_datadir}/%{real_name}/client

# client jar depenencies
# %{__ln_s} hadoop-client-modules/%{real_name}-client/target/%{real_name}-client-%{hadoop_version}/share/%{real_name}/client/lib/hadoop-shaded-protobuf_3_7-1.0.0.jar %{buildroot}%{_datadir}/%{real_name}/client/lib/hadoop-shaded-protobuf_3_7.jar
copy_dep_jars hadoop-client-modules/%{real_name}-client/target/%{real_name}-client-%{hadoop_version}/share/%{real_name}/client/lib %{buildroot}%{_datadir}/%{real_name}/client/lib
pushd  hadoop-client-modules/%{real_name}-client/target/%{real_name}-client-%{hadoop_version}/share/%{real_name}/client/lib
  link_hadoop_jars %{buildroot}%{_datadir}/%{real_name}/client/lib
popd
cp -f hadoop-client-modules/%{real_name}-client-api/target/hadoop-client-api-%{version}.jar hadoop-client-modules/%{real_name}-client/target/%{real_name}-client-%{hadoop_version}/share/%{real_name}/client
cp -f hadoop-client-modules/%{real_name}-client-minicluster/target/hadoop-client-minicluster-%{version}.jar hadoop-client-modules/%{real_name}-client/target/%{real_name}-client-%{hadoop_version}/share/%{real_name}/client
cp -f hadoop-client-modules/%{real_name}-client-runtime/target/hadoop-client-runtime-%{version}.jar hadoop-client-modules/%{real_name}-client/target/%{real_name}-client-%{hadoop_version}/share/%{real_name}/client
pushd  hadoop-client-modules/%{real_name}-client/target/%{real_name}-client-%{hadoop_version}/share/%{real_name}/client
  link_hadoop_jars %{buildroot}%{_datadir}/%{real_name}/client
popd

# common jar depenencies
copy_dep_jars $basedir/share/%{real_name}/common/lib %{buildroot}%{_datadir}/%{real_name}/common/lib
cp -f hadoop-common-project/%{real_name}-kms/target/hadoop-kms-%{version}.jar $basedir/share/%{real_name}/common
cp -f hadoop-common-project/%{real_name}-nfs/target/hadoop-nfs-%{version}.jar $basedir/share/%{real_name}/common 
cp -f hadoop-common-project/%{real_name}-auth/target/hadoop-auth-%{version}.jar $basedir/share/%{real_name}/common
pushd $basedir/share/%{real_name}/common
  link_hadoop_jars %{buildroot}%{_datadir}/%{real_name}/common
popd
pushd $basedir/share/%{real_name}/common/lib
  link_hadoop_jars %{buildroot}%{_datadir}/%{real_name}/common/lib
popd

# hdfs jar dependencies
copy_dep_jars $hdfsdir/share/%{real_name}/hdfs/lib %{buildroot}%{_datadir}/%{real_name}/hdfs/lib
%{__ln_s} %{_jnidir}/%{real_name}/%{real_name}-hdfs-bkjournal.jar %{buildroot}%{_datadir}/%{real_name}/hdfs/lib
cp -f hadoop-hdfs-project/%{real_name}-hdfs-client/target/hadoop-hdfs-client-%{version}.jar $hdfsdir/share/%{real_name}/hdfs
cp -f hadoop-hdfs-project/%{real_name}-hdfs-httpfs/target/hadoop-hdfs-httpfs-%{version}.jar $hdfsdir/share/%{real_name}/hdfs
cp -f hadoop-hdfs-project/%{real_name}-hdfs-native-client/target/hadoop-hdfs-native-client-%{version}.jar $hdfsdir/share/%{real_name}/hdfs
cp -f hadoop-hdfs-project/%{real_name}-hdfs-nfs/target/hadoop-hdfs-nfs-%{version}.jar $hdfsdir/share/%{real_name}/hdfs
cp -f hadoop-hdfs-project/%{real_name}-hdfs-rbf/target/hadoop-hdfs-rbf-%{version}.jar $hdfsdir/share/%{real_name}/hdfs
pushd $hdfsdir/share/%{real_name}/hdfs
  link_hadoop_jars %{buildroot}%{_datadir}/%{real_name}/hdfs
popd

# httpfs
# Create the webapp directory structure
pushd %{buildroot}%{_sharedstatedir}/tomcats/httpfs
  %{__ln_s} %{_datadir}/%{real_name}/httpfs/tomcat/conf conf
  %{__ln_s} %{_datadir}/%{real_name}/httpfs/tomcat/lib lib
  %{__ln_s} %{_datadir}/%{real_name}/httpfs/tomcat/logs logs
  %{__ln_s} %{_datadir}/%{real_name}/httpfs/tomcat/temp temp
  %{__ln_s} %{_datadir}/%{real_name}/httpfs/tomcat/webapps webapps
  %{__ln_s} %{_datadir}/%{real_name}/httpfs/tomcat/work work
popd

# Copy the tomcat configuration and overlay with specific configuration bits.
# This is needed so the httpfs instance won't collide with a system running
# tomcat
for cfgfile in catalina.policy catalina.properties context.xml \
  tomcat.conf web.xml server.xml logging.properties;
do
  cp -a %{_sysconfdir}/tomcat/$cfgfile %{buildroot}%{_sysconfdir}/%{real_name}/tomcat
done

# Replace, in place, the Tomcat configuration files delivered with the current
# Fedora release. See BZ#1295968 for some reason.
sed -i -e 's/8005/${httpfs.admin.port}/g' -e 's/8080/${httpfs.http.port}/g' %{buildroot}%{_sysconfdir}/%{real_name}/tomcat/server.xml
sed -i -e 's/catalina.base/httpfs.log.dir/g' %{buildroot}%{_sysconfdir}/%{real_name}/tomcat/logging.properties
# Given the permission, only the root and tomcat users can access to that file,
# not the build user. So, the build would fail here.
install -m 660 %{SOURCE9} %{buildroot}%{_sysconfdir}/%{real_name}/tomcat/tomcat-users.xml

# Copy the httpfs webapp
cp -arf %{real_name}-hdfs-project/%{real_name}-hdfs-httpfs/target/classes/webapps/webhdfs %{buildroot}%{_datadir}/%{real_name}/httpfs/tomcat/webapps

# Tell tomcat to follow symlinks
install -d -m 0766 %{buildroot}%{_datadir}/%{real_name}/httpfs/tomcat/webapps/webhdfs/META-INF/
cp %{SOURCE5} %{buildroot}%{_datadir}/%{real_name}/httpfs/tomcat/webapps/webhdfs/META-INF/

# Remove the jars included in the webapp and create symlinks
rm -f %{buildroot}%{_datadir}/%{real_name}/httpfs/tomcat/webapps/webhdfs/WEB-INF/lib/tools*.jar
rm -f %{buildroot}%{_datadir}/%{real_name}/httpfs/tomcat/webapps/webhdfs/WEB-INF/lib/tomcat-*.jar

pushd %{buildroot}%{_datadir}/%{real_name}/httpfs/tomcat
  %{__ln_s} %{_datadir}/tomcat/bin bin
  %{__ln_s} %{_sysconfdir}/%{real_name}/tomcat conf
  %{__ln_s} %{_datadir}/tomcat/lib lib
  %{__ln_s} %{_var}/cache/%{real_name}-httpfs/temp temp
  %{__ln_s} %{_var}/cache/%{real_name}-httpfs/work work
  %{__ln_s} %{_var}/log/%{real_name}-httpfs logs
popd

# touch new null file
touch %{buildroot}%{_sysconfdir}/%{real_name}/httpfs-signature.secret

# mapreduce jar dependencies
mrdir='%{real_name}-mapreduce-project/target/%{real_name}-mapreduce-%{hadoop_version}'
copy_dep_jars $mrdir/share/%{real_name}/mapreduce/lib %{buildroot}%{_datadir}/%{real_name}/mapreduce/lib
%{__ln_s} %{_javadir}/%{real_name}/%{real_name}-annotations.jar %{buildroot}%{_datadir}/%{real_name}/mapreduce/lib
cp -f hadoop-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-nativetask/target/hadoop-mapreduce-client-nativetask-%{version}.jar $mrdir/share/%{real_name}/mapreduce
cp -f hadoop-mapreduce-project/%{real_name}-mapreduce-client/%{real_name}-mapreduce-client-uploader/target/hadoop-mapreduce-client-uploader-%{version}.jar $mrdir/share/%{real_name}/mapreduce
cp -f hadoop-mapreduce-project/%{real_name}-mapreduce-examples/target/hadoop-mapreduce-examples-%{version}.jar $mrdir/share/%{real_name}/mapreduce
pushd $mrdir/share/%{real_name}/mapreduce
  link_hadoop_jars %{buildroot}%{_datadir}/%{real_name}/mapreduce
popd

# yarn jar dependencies
yarndir='%{real_name}-yarn-project/target/%{real_name}-yarn-project-%{hadoop_version}'
copy_dep_jars $yarndir/share/%{real_name}/yarn/lib %{buildroot}%{_datadir}/%{real_name}/yarn/lib
%{__ln_s} %{_javadir}/%{real_name}/%{real_name}-annotations.jar %{buildroot}%{_datadir}/%{real_name}/yarn/lib
cp -f hadoop-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-nodemanager/target/hadoop-yarn-server-nodemanager-%{version}.jar $yarndir/share/%{real_name}/yarn
cp -f hadoop-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-router/target/hadoop-yarn-server-router-%{version}.jar $yarndir/share/%{real_name}/yarn
cp -f hadoop-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-timeline-pluginstorage/target/hadoop-yarn-server-timeline-pluginstorage-%{version}.jar $yarndir/share/%{real_name}/yarn
cp -f hadoop-yarn-project/%{real_name}-yarn/%{real_name}-yarn-applications/%{real_name}-yarn-services/%{real_name}-yarn-services-api/target/hadoop-yarn-services-api-%{version}.jar $yarndir/share/%{real_name}/yarn
cp -f hadoop-yarn-project/%{real_name}-yarn/%{real_name}-yarn-applications/%{real_name}-yarn-services/%{real_name}-yarn-services-core/target/hadoop-yarn-services-core-%{version}.jar $yarndir/share/%{real_name}/yarn
cp -f hadoop-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-timelineservice/target/hadoop-yarn-server-timelineservice-%{version}.jar $yarndir/share/%{real_name}/yarn
cp -f hadoop-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-timelineservice-hbase/%{real_name}-yarn-server-timelineservice-hbase-client/target/hadoop-yarn-server-timelineservice-hbase-client-%{version}.jar $yarndir/share/%{real_name}/yarn
cp -f hadoop-yarn-project/%{real_name}-yarn/%{real_name}-yarn-server/%{real_name}-yarn-server-timelineservice-hbase/%{real_name}-yarn-server-timelineservice-hbase-common/target/hadoop-yarn-server-timelineservice-hbase-common-%{version}.jar $yarndir/share/%{real_name}/yarn
cp -f hadoop-yarn-project/target/%{real_name}-yarn-project-%{version}/share/%{real_name}/yarn/timelineservice/hadoop-yarn-server-timelineservice-hbase-coprocessor-%{version}.jar $yarndir/share/%{real_name}/yarn
pushd $yarndir/share/%{real_name}/yarn
  link_hadoop_jars %{buildroot}%{_datadir}/%{real_name}/yarn
popd

# Install hdfs webapp bits
cp -arf hadoop-hdfs-project/hadoop-hdfs/target/webapps/* %{buildroot}%{_datadir}/%{real_name}/hdfs/webapps

# hadoop layout. Convert to appropriate lib location for 32 and 64 bit archs
lib=$(echo %{?_libdir} | sed -e 's:/usr/\(.*\):\1:')
if [ "$lib" = "%_libdir" ]; then
  echo "_libdir is not located in /usr.  Lib location is wrong"
  exit 1
fi
sed -e "s|HADOOP_COMMON_LIB_NATIVE_DIR\s*=.*|HADOOP_COMMON_LIB_NATIVE_DIR=$lib/%{real_name}|" %{SOURCE1} > %{buildroot}%{_libexecdir}/%{real_name}-layout.sh

# Default config
cp -f %{SOURCE10} %{buildroot}%{_sysconfdir}/%{real_name}/core-site.xml
cp -f %{SOURCE11} %{buildroot}%{_sysconfdir}/%{real_name}/hdfs-site.xml
cp -f %{SOURCE12} %{buildroot}%{_sysconfdir}/%{real_name}/mapred-site.xml
cp -f %{SOURCE13} %{buildroot}%{_sysconfdir}/%{real_name}/yarn-site.xml

# systemd configuration
install -d -m 0755 %{buildroot}%{_unitdir}/
for service in %{hdfs_services} %{mapreduce_services} %{yarn_services}
do
  s=`echo $service | cut -d'-' -f 2 | cut -d'.' -f 1`
  daemon=$s
  if [[ "%{hdfs_services}" == *$service* ]]
  then
    src=%{SOURCE2}
  elif [[ "%{mapreduce_services}" == *$service* ]]
  then
    src=%{SOURCE3}
  elif [[ "%{yarn_services}" == *$service* ]]
  then
    if [[ "$s" == "timelineserver" ]]
    then
      daemon='historyserver'
    fi
    src=%{SOURCE4}
  else
    echo "Failed to determine type of service for %service"
    exit 1
  fi
  sed -e "s|DAEMON|$daemon|g" $src > %{buildroot}%{_unitdir}/%{real_name}-$s.service
done

cp -f %{SOURCE7} %{buildroot}%{_sysconfdir}/sysconfig/tomcat@httpfs

# Ensure /var/run directories are recreated on boot
echo "d %{_var}/run/%{real_name}-yarn 0775 yarn hadoop -" > %{buildroot}%{_tmpfilesdir}/%{real_name}-yarn.conf
echo "d %{_var}/run/%{real_name}-hdfs 0775 hdfs hadoop -" > %{buildroot}%{_tmpfilesdir}/%{real_name}-hdfs.conf
echo "d %{_var}/run/%{real_name}-mapreduce 0775 mapred hadoop -" > %{buildroot}%{_tmpfilesdir}/%{real_name}-mapreduce.conf

# logrotate config
for type in hdfs httpfs yarn mapreduce
do
  sed -e "s|NAME|$type|" %{SOURCE6} > %{buildroot}%{_sysconfdir}/logrotate.d/%{real_name}-$type
done
sed -i "s|{|%{_var}/log/hadoop-hdfs/*.audit\n{|" %{buildroot}%{_sysconfdir}/logrotate.d/%{real_name}-hdfs

# hdfs init script
install -m 755 %{SOURCE8} %{buildroot}%{_sbindir}

%pretrans -p <lua> hdfs
path = "%{_datadir}/%{real_name}/hdfs/webapps"
st = posix.stat(path)
if st and st.type == "link" then
  os.remove(path)
end

# 写入用户信息
%pre common
# getent 查看系统的数据库中的相关记录。
# 将输出输出到/dev/null
getent group hadoop >/dev/null || groupadd -r hadoop

%pre hdfs
getent group hdfs >/dev/null || groupadd -r hdfs
getent passwd hdfs >/dev/null || /usr/sbin/useradd --comment "Apache Hadoop HDFS" --shell /sbin/nologin -M -r -g hdfs -G hadoop --home %{_sharedstatedir}/%{real_name}-hdfs hdfs

%pre mapreduce
getent group mapred >/dev/null || groupadd -r mapred
getent passwd mapred >/dev/null || /usr/sbin/useradd --comment "Apache Hadoop MapReduce" --shell /sbin/nologin -M -r -g mapred -G hadoop --home %{_var}/cache/%{real_name}-mapreduce mapred

%pre yarn
getent group yarn >/dev/null || groupadd -r yarn
getent passwd yarn >/dev/null || /usr/sbin/useradd --comment "Apache Hadoop Yarn" --shell /sbin/nologin -M -r -g yarn -G hadoop --home %{_var}/cache/%{real_name}-yarn yarn

%preun hdfs
%systemd_preun %{hdfs_services}

%preun mapreduce
%systemd_preun %{mapreduce_services}

%preun yarn
%systemd_preun %{yarn_services}

# The scripts support a special flag, -p which allows the scriptlet to invoke a single program directly rather than having to spawn a shell to invoke the programs. 
# ldconfig 命令的用途,主要是在默认搜寻目录(/lib和/usr/lib)以及动态库配置文件/etc/ld.so.conf内所列的目录下,搜索出可共享的动态链接库(格式如前介绍,lib*.so*),进而创建出动态装入程序(ld.so)所需的连接和缓存文件.缓存文件默认为 /etc/ld.so.cache,此文件保存已排好序的动态链接库名字列表.
# ldconfig通常在系统启动时运行,而当用户安装了一个新的动态链接库时,就需要手工运行这个命令.
%post common-native -p /sbin/ldconfig

%post hdfs
# Change the home directory for the hdfs user
if [[ `getent passwd hdfs | cut -d: -f 6` != "%{_sharedstatedir}/%{real_name}-hdfs" ]]
then
  /usr/sbin/usermod -d %{_sharedstatedir}/%{real_name}-hdfs hdfs
fi

if [ $1 -gt 1 ]
then
  if [ -d %{_var}/cache/%{real_name}-hdfs ] && [ ! -L %{_var}/cache/%{real_name}-hdfs ]
  then
    # Move the existing hdfs data to the new location
    mv -f %{_var}/cache/%{real_name}-hdfs/* %{_sharedstatedir}/%{real_name}-hdfs/
  fi
fi
%systemd_post %{hdfs_services}

%post -n libhdfs -p /sbin/ldconfig

%post mapreduce
%systemd_post %{mapreduce_services}

%post yarn
%systemd_post %{yarn_services}

%postun common-native -p /sbin/ldconfig

%postun hdfs
%systemd_postun_with_restart %{hdfs_services}

if [ $1 -lt 1 ]
then
  # Remove the compatibility symlink
  rm -f %{_var}/cache/%{real_name}-hdfs
fi

%postun -n libhdfs -p /sbin/ldconfig

%postun mapreduce
%systemd_postun_with_restart %{mapreduce_services}

%postun yarn
%systemd_postun_with_restart %{yarn_services}

%posttrans hdfs
# Create a symlink to the new location for hdfs data in case the user changed
# the configuration file and the new one isn't in place to point to the
# correct location
if [ ! -e %{_var}/cache/%{real_name}-hdfs ]
then
  %{__ln_s} %{_sharedstatedir}/%{real_name}-hdfs %{_var}/cache
fi

%files -f .mfiles-%{real_name}-client client
%{_datadir}/%{real_name}/client

%files -f .mfiles common
%doc LICENSE.txt
%doc NOTICE.txt
%doc README.txt
%config(noreplace) %{_sysconfdir}/%{real_name}/core-site.xml
%config(noreplace) %{_sysconfdir}/%{real_name}/%{real_name}-env.sh
%config(noreplace) %{_sysconfdir}/%{real_name}/%{real_name}-metrics2.properties
%config(noreplace) %{_sysconfdir}/%{real_name}/%{real_name}-policy.xml
%config(noreplace) %{_sysconfdir}/%{real_name}/log4j.properties
%config(noreplace) %{_sysconfdir}/%{real_name}/ssl-client.xml.example
%config(noreplace) %{_sysconfdir}/%{real_name}/ssl-server.xml.example
%config(noreplace) %{_sysconfdir}/%{real_name}/configuration.xsl

%dir %{_datadir}/%{real_name}
%dir %{_datadir}/%{real_name}/common
%{_datadir}/%{real_name}/common/lib
%{_datadir}/%{real_name}/common/hadoop-kms.jar
%{_datadir}/%{real_name}/common/hadoop-nfs.jar
%{_datadir}/%{real_name}/common/hadoop-auth.jar
%{_libexecdir}/%{real_name}-config.sh
%{_libexecdir}/%{real_name}-layout.sh

# Workaround for bz1012059
%{_mavenpomdir}/JPP.%{real_name}-%{real_name}-project-dist.pom

%{_bindir}/%{real_name}
%{_sbindir}/%{real_name}-daemon.sh
%{_sbindir}/%{real_name}-daemons.sh
%{_sbindir}/start-all.sh
%{_sbindir}/start-balancer.sh
%{_sbindir}/start-dfs.sh
%{_sbindir}/start-secure-dns.sh
%{_sbindir}/stop-all.sh
%{_sbindir}/stop-balancer.sh
%{_sbindir}/stop-dfs.sh
%{_sbindir}/stop-secure-dns.sh

%files common-native
%{_libdir}/%{real_name}/libhadoop.*

%files devel
%{_includedir}/%{real_name}
%{_libdir}/libhdfs.so

%files -f .mfiles-%{real_name}-hdfs hdfs
%config(noreplace) %{_sysconfdir}/%{real_name}/hdfs-site.xml
%{_datadir}/%{real_name}/hdfs
%{_unitdir}/%{real_name}-datanode.service
%{_unitdir}/%{real_name}-namenode.service
%{_unitdir}/%{real_name}-journalnode.service
%{_unitdir}/%{real_name}-secondarynamenode.service
%{_unitdir}/%{real_name}-zkfc.service
%{_libexecdir}/hdfs-config.sh
%{_bindir}/hdfs
%{_sbindir}/distribute-exclude.sh
%{_sbindir}/refresh-namenodes.sh
%{_sbindir}/hdfs-create-dirs
%{_tmpfilesdir}/%{real_name}-hdfs.conf
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/logrotate.d/%{real_name}-hdfs
%attr(0755,hdfs,hadoop) %dir %{_var}/run/%{real_name}-hdfs
%attr(0755,hdfs,hadoop) %dir %{_var}/log/%{real_name}-hdfs
%attr(0755,hdfs,hadoop) %dir %{_sharedstatedir}/%{real_name}-hdfs


%files httpfs
%config(noreplace) %{_sysconfdir}/sysconfig/tomcat@httpfs
%config(noreplace) %{_sysconfdir}/%{real_name}/httpfs-env.sh
%config(noreplace) %{_sysconfdir}/%{real_name}/httpfs-log4j.properties
%config(noreplace) %{_sysconfdir}/%{real_name}/httpfs-signature.secret
%config(noreplace) %{_sysconfdir}/%{real_name}/httpfs-site.xml
%attr(-,tomcat,tomcat) %config(noreplace) %{_sysconfdir}/%{real_name}/tomcat/*.*
%attr(0775,root,tomcat) %dir %{_sysconfdir}/%{real_name}/tomcat
%attr(0775,root,tomcat) %dir %{_sysconfdir}/%{real_name}/tomcat/Catalina
%attr(0775,root,tomcat) %dir %{_sysconfdir}/%{real_name}/tomcat/Catalina/localhost
%{_datadir}/%{real_name}/httpfs
%{_sharedstatedir}/tomcats/httpfs
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/logrotate.d/%{real_name}-httpfs
%attr(0775,root,tomcat) %dir %{_var}/log/%{real_name}-httpfs
%attr(0775,root,tomcat) %dir %{_var}/cache/%{real_name}-httpfs
%attr(0775,root,tomcat) %dir %{_var}/cache/%{real_name}-httpfs/temp
%attr(0775,root,tomcat) %dir %{_var}/cache/%{real_name}-httpfs/work

%files -n libhdfs
%{_libdir}/libhdfs.so.*

%files -f .mfiles-%{real_name}-mapreduce mapreduce
%config(noreplace) %{_sysconfdir}/%{real_name}/mapred-env.sh
%config(noreplace) %{_sysconfdir}/%{real_name}/mapred-queues.xml.template
%config(noreplace) %{_sysconfdir}/%{real_name}/mapred-site.xml
%{_datadir}/%{real_name}/mapreduce
%{_libexecdir}/mapred-config.sh
%{_unitdir}/%{real_name}-historyserver.service
%{_bindir}/mapred
%{_sbindir}/mr-jobhistory-daemon.sh
%{_tmpfilesdir}/%{real_name}-mapreduce.conf
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/logrotate.d/%{real_name}-mapreduce
%attr(0755,mapred,hadoop) %dir %{_var}/run/%{real_name}-mapreduce
%attr(0755,mapred,hadoop) %dir %{_var}/log/%{real_name}-mapreduce
%attr(0755,mapred,hadoop) %dir %{_var}/cache/%{real_name}-mapreduce

%files -f .mfiles-%{real_name}-mapreduce-examples mapreduce-examples

%files -f .mfiles-%{real_name}-maven-plugin maven-plugin

%files -f .mfiles-%{real_name}-tests tests

%files -f .mfiles-%{real_name}-yarn yarn
%config(noreplace) %{_sysconfdir}/%{real_name}/capacity-scheduler.xml
%config(noreplace) %{_sysconfdir}/%{real_name}/yarn-env.sh
%config(noreplace) %{_sysconfdir}/%{real_name}/yarn-site.xml
%{_unitdir}/%{real_name}-nodemanager.service
%{_unitdir}/%{real_name}-proxyserver.service
%{_unitdir}/%{real_name}-resourcemanager.service
%{_unitdir}/%{real_name}-timelineserver.service
%{_libexecdir}/yarn-config.sh
%{_datadir}/%{real_name}/yarn
%{_bindir}/oom-listener
%{_bindir}/yarn
%{_sbindir}/yarn-daemon.sh
%{_sbindir}/yarn-daemons.sh
%{_sbindir}/start-yarn.sh
%{_sbindir}/stop-yarn.sh
%{_tmpfilesdir}/%{real_name}-yarn.conf
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/logrotate.d/%{real_name}-yarn
%attr(0755,yarn,hadoop) %dir %{_var}/run/%{real_name}-yarn
%attr(0755,yarn,hadoop) %dir %{_var}/log/%{real_name}-yarn
%attr(0755,yarn,hadoop) %dir %{_var}/cache/%{real_name}-yarn

%files yarn-security
%config(noreplace) %{_sysconfdir}/%{real_name}/container-executor.cfg

%changelog
