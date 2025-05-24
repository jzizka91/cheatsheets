### Migrate DB data from Mysql 5.7 to 8.4
https://php.watch/articles/fix-php-mysql-84-mysql_native_password-not-loaded

#### 1. Force upgrade DB. Mysql server service must be stopped!
```bash
docker run --rm -it \
  --name mysql_aowow_fix \
  -v aowow_db:/var/lib/mysql \
  -v my-aowow.cnf:/etc/mysql/conf.d/my-aowow.cnf \
  mysql:8.4.5 \
  --upgrade=FORCE
```

* Mysql config (my-aowow.cnf) must have "mysql_native_password=on"
* Use `mysqld --upgrade=FORCE` if docker container not used.


#### 2. List MySQL Users using mysql_native_password

* On a MySQL console, run the following to list users using the deprecated authentication plugin:

`SELECT user, host, plugin from mysql.user WHERE plugin='mysql_native_password';`

* Running the above command should list all users that use the mysql_native_password plugin:


#### 3. Update mysql_native_password users to caching_sha2_password

`ALTER USER '<USERNAME>'@'<HOST>' IDENTIFIED WITH caching_sha2_password BY '<PASSWORD>';`

* Replace <USERNAME>, <HOST>, and <PASSWORD> with the MySQL user's username, host, and password.


#### 4. Make full-backup

`mysqldump -u root -p"$DB_PW" --all-databases --single-transaction --ignore-table=mysql.innodb_index_stats --ignore-table=mysql.innodb_table_stats > <BACKUP.sql>`

* Not ignoring innodb tables causes error `ERROR 3554 (HY000) at line 318: Access to system table 'mysql.innodb_index_stats' is rejected.`


#### 5. Run Mysql with using the full-backup (modified for caching_sha2_password usage)
