
# Installation

## Requirement

   - nodejs (~0.10.33)
   - npm (~2.1.8)
      - bower (~1.3.12)
      - forever (~0.13.0)

```
# nodejs
curl -sL https://deb.nodesource.com/setup | sudo bash -
sudo apt-get install -y nodejs
# npm
curl -L https://npmjs.org/install.sh | sh
# npm package
npm -g install bower forever
```

### Reference
   * [Installing Node.js via package manager](https://github.com/joyent/node/wiki/installing-node.js-via-package-manager)

## Repository
```
git clone ****ntubmtlab.git
cd ntubmtlab/server
npm install
bower install
```


## files
crontab
```
$REPO_DIR=`which ntubmtlab`
*/30 * * * * $REPO_DIR/task/sport.py > $REPO_DIR/log/data.log
*/30 * * * * $REPO_DIR/task/wakeup.py >> $REPO_DIR/log/data.log
@reboot  PORT=1080 `which forever` start $REPO_DIR/server/bin/www
```

