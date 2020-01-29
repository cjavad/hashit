Name:       hashit
Version:    3.5.3
Release:    1
Summary:    hashit, a hashing application.
License:    LICENSE
URL:        https://cjavad.github.io/hashit
Requires:   python3

%description
Hashing Application with muliple modes, settings and more!
Hashit, is an hashing application used as an verification tool, intendet to replace the "standard" linux hashing utilities such as
md5sum, sha1sum and so on. One of the main reasons why this program was develop was to create an easy-to-use command line tool for 
newcomers and professionals alike to hash/verify files and other data. For more see our homepage at https://cjavad.github.io/hashit.


%prep
python3 setup.py clean -a

%build
python3 setup.py build --force

%install
python3 setup.py install --force

%files
# python takes care of this

%changelog
# removed changelog :cry:
