%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

Name:	webvirtmgr	
Version: 4.5.2
Release:	1%{?dist}
Summary:  Web based control of libvirt KVM instances	

Group:	virtualization
License: Apache
URL:	https://github.com/retspen/webvirtmgr	
Source0:	webvirtmgr-%{version}.tar.gz

Requires:	libvirt-python 
Requires:	libxml2-python 
Requires:	python-websockify
Requires:	supervisor
Requires:	nginx
Requires:	python-django = 1.5.5
Requires:	python-gunicorn = 18.0
Requires:       python-django-auth-ldap
BuildRequires:  python-devel
BuildRequires:  sqlite
BuildArch:	noarch

%description
Web (django) based control of KVM virtual guests through the libvirt API

%prep
%setup -q -n webvirtmgr

%build


%install
mkdir -p %{buildroot}/var/www/webvirtmgr/images
install -D conf/initd/webvirtmgr-novnc-redhat %{buildroot}/etc/init.d/webvirtmgr-novnc

rm -rf conf/initd
rm -rf conf/saltstack
rm -f conf/libvirt-bootstrap.sh
rm -f webvirtmgr/settings_jenkins.py

for dir in console create hostdetail instance locale networks serverlog servers static storages templates vrtManager webvirtmgr conf
do
cp -r ${dir} %{buildroot}/var/www/webvirtmgr/ 
done 
install -D README.md %{buildroot}/usr/share/doc/webvirtmgr/webvirtmgr-README.md
install -D images/README.md %{buildroot}/usr/share/doc/webvirtmgr/images-README.md
install -D manage.py %{buildroot}/var/www/webvirtmgr/manage.py
touch %{buildroot}/var/www/webvirtmgr/webvirtmgr.sqlite3 
sqlite3 %{buildroot}/var/www/webvirtmgr/webvirtmgr.sqlite3 '.show' &> /dev/null
sqlite3 %{buildroot}/var/www/webvirtmgr/webvirtmgr.sqlite3 '.databases' &> /dev/null

/usr/lib/rpm/brp-python-bytecompile
ln -sf /usr/lib/python2.6/site-packages/django/contrib/admin/static/admin %{buildroot}/var/www/webvirtmgr/static/admin
rm -f %{buildroot}/var/www/webvirtmgr/manage.py{c,o}
rm -f %{buildroot}/var/www/webvirtmgr/webvirtmgr/settings.py{c,o}

%files
%defattr(644,nginx,nginx,775)
%doc /usr/share/doc/webvirtmgr
%dir /var/www/webvirtmgr
/var/www/webvirtmgr/conf
/var/www/webvirtmgr/console
/var/www/webvirtmgr/create
/var/www/webvirtmgr/hostdetail
/var/www/webvirtmgr/images
/var/www/webvirtmgr/instance
/var/www/webvirtmgr/locale
/var/www/webvirtmgr/networks
/var/www/webvirtmgr/serverlog
/var/www/webvirtmgr/servers
/var/www/webvirtmgr/static
/var/www/webvirtmgr/storages
/var/www/webvirtmgr/templates
/var/www/webvirtmgr/vrtManager
/var/www/webvirtmgr/webvirtmgr
%config /var/www/webvirtmgr/webvirtmgr/settings.py
%config /var/www/webvirtmgr/webvirtmgr.sqlite3
%defattr(755,root,root,755)
/var/www/webvirtmgr/manage.py
/var/www/webvirtmgr/console/webvirtmgr-novnc
/etc/init.d/webvirtmgr-novnc

%changelog
* Mon Mar 31 2014 James Hogarth - 4.5.2-6
- Make the settings.py file labelled as config so that puppet can safely manipulate it and add the ldap depdendency.
* Mon Mar 31 2014 James Hogarth - 4.5.2-5
- Break extra code over primary source as patches to ease maintenance
* Mon Mar 31 2014 James Hogarth - 4.5.2-4
- Enabled ssl requirement
* Mon Mar 31 2014 James Hogarth - 4.5.2-3
- Enabled  django admin interface 
* Fri Mar 28 2014 James Hogarth - 4.5.2-2
- Tuned permissions and moved some spec stuff to puppet module
* Thu Mar 13 2014 James Hogarth - 4.5.2-1
- Initial package.

