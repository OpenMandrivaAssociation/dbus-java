%define section         free
%define gcj_support     0

Name:           dbus-java
Version:        2.5.1
Release:        %mkrel 0.0.1
Epoch:          0
Summary:        Java bindings for D-Bus
License:        GPL
Group:          Development/Java
URL:            https://dbus.freedesktop.org/
Source0:        http://dbus.freedesktop.org/releases/dbus-java/dbus-java-%{version}.tar.gz
Requires:       jpackage-utils >= 0:1.6
Requires:       libmatthew-java
BuildRequires:  docbook-dtd41-sgml
BuildRequires:  docbook-utils
BuildRequires:  tex4ht
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  libmatthew-java
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
D-Bus is a message bus system, a simple way for applications to
talk to one another. In addition to interprocess communication,
D-Bus helps coordinate process lifecycle; it makes it simple and
reliable to code a "single instance" application or daemon, and to
launch applications and daemons on demand when their services are
needed.

This package contains the Java bindings for D-Bus.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%{__mkdir_p} api
%{__perl} -pi -e 's|.*Class-Path.*$||g' Makefile
/bin/touch Manifest
%{__perl} -pi -e 's|docbook-to-man|/bin/true|g' Makefile

%build
export CLASSPATH=`pwd`:$(build-classpath libmatthew-java)
export OPT_JAR_LIST=:
%{__make} \
  JAVAC=%{javac} \
  JAR=%{jar} \
  JAVAH=%{java_home}/bin/javah \
  GCJ=%{gcj} \
  CC=%{__cc} \
  LD=%{__ld} \
  CFLAGS="-fPIC %{optflags}" \
  LDFLAGS="-fPIC -shared" \
  GCJFLAGS="%{optflags} -fjni" \
  JCFLAGS="-nowarn -source 1.5" \
  JAVA_HOME=%{java_home}

%{javadoc} -d api `%{_bindir}/find . -name '*.java'`

%install
%{__rm} -rf %{buildroot}

%{makeinstall_std} \
  PREFIX=%{_prefix} \
  JARPREFIX=%{_javadir} \
  BINPREFIX=%{_bindir} \
  DOCPREFIX=%{_docdir}/%{name} \
  MANPREFIX=%{_mandir}/man1 \
  JAVAUNIXLIBDIR=%{_libdir} \
  JAVAUNIXJARDIR=%{jnidir} \
  JAVAC=%{javac} \
  JAR=%{jar} \
  JAVAH=%{java_home}/bin/javah \
  GCJ=%{gcj} \
  CC=%{__cc} \
  LD=%{__ld} \
  CFLAGS="-fPIC %{optflags}" \
  LDFLAGS="-fPIC -shared" \
  GCJFLAGS="%{optflags} -fjni" \
  JCFLAGS="-nowarn -source 1.5" \
  JAVA_HOME=%{java_home}

(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

(cd %{buildroot}%{_bindir} && %{__perl} -pi \
  -e 's|^JAVA=.*|JAVA=`%{_bindir}/test -r %{_javadir}-utils/java-functions && . %{_javadir}-utils/java-functions && set_javacmd && /bin/echo \$\{JAVACMD\}`|;' \
  -e 's|^JARPATH=.*|JARPATH=%{_javadir}|;' \
  -e 's|^JAVAUNIXLIBPATH=.*|JAVAUNIXLIBPATH=%{_libdir}|;' \
  -e 's|^JAVAUNIXJARPATH=.*|JAVAUNIXJARPATH=%{_jnidir}/libmatthew-java|;' \
  -e 's|^exec ||' \
  *)

for man in `%{_bindir}/find . -name '*.sgml'`; do
    name=`/bin/basename ${man} .sgml`
    %{_bindir}/docbook2man ${man} -o ${name}
    %{__rm} %{buildroot}%{_mandir}/man1/${name}.1
    %{__cp} -a ${name}/*.1 %{buildroot}%{_mandir}/man1/${name}.1
done

%{gcj_compile}

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc AUTHORS changelog COPYING INSTALL README
%attr(0755,root,root) %{_bindir}/*
%{_javadir}/*.jar
%{_mandir}/man1/*.1*
%{gcj_files}

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %dir %{_javadocdir}/%{name}
