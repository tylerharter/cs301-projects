version=stable
rm -rf redis-$version
curl -O http://download.redis.io/releases/redis-$version.tar.gz && tar -xzf redis-$version.tar.gz && rm redis-$version.tar.gz

cd redis-$version
make
make test
echo "Now install redis..."
sudo make install
cp redis.conf ../
cd ..
rm -rf redis-$version
echo "Success! Please run redis-server ./redis.conf" to start redis server.
