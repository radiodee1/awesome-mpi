yum -y update

#yum install -y nfs-utils nfs-utils-lib svn

#yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel compat-gcc-34-g77 gcc

#wget https://www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz --no-check-certificate
#tar xf Python-2.7.8.tgz
#cd Python-2.7.8
#./configure --prefix=/usr/local --enable-unicode=ucs4 --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"
#make && make altinstall
 
yum -y install mpich2 
