### Backup LXD Containers (version 3.0.6):

```
lxc snapshot gitlab gitlab-snap
lxc publish gitlab/gitlab-snap --alias 20210801_gitlab-backup
lxc image export 20210801_gitlab-backup ~/backup_gitlab/
lxc image delete 20210801_gitlab-backup
rsync -aP /var/lib/lxd/containers/gitlab ~/backup_gitlab/
lxc delete gitlab
 ```