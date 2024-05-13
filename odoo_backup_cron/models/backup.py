import odoo

import os
import datetime
import time
import shutil
import json
import tempfile

import os
import re

from odoo import api, fields, models, tools, _
from datetime import datetime, timedelta

DB_NAME = 'GAP'
#ODOO_CONF = '/etc/odoo.conf'

FILE_BACKUP_PATH = '/opt/odooGAPbackup/'

UID = odoo.SUPERUSER_ID
#odoo.tools.config.parse_config(['--config=%s' % ODOO_CONF])

regexp = r'GAP.*\.zip$'

class OdooBackup(models.Model):
    _name = 'odoo.backup'

    def runOdooBackup(self):
        print('RUN CRON')

        res = [f for f in os.listdir(FILE_BACKUP_PATH) if re.search(regexp , f)]
        for f in res:
            print('Remove: '+f)
            os.remove(FILE_BACKUP_PATH + f)

        with odoo.api.Environment.manage():
            registry = odoo.modules.registry.Registry(DB_NAME)
            with registry.cursor() as cr:

                db_name = cr.dbname

                bkp_file = '%s_%s.%s' % (db_name, time.strftime('%Y-%m-%d_%H-%M-%S'), 'zip')
                file_path = os.path.join('/tmp', bkp_file)
                fp = open(file_path, 'wb')

                cmd = ['pg_dump', '--no-owner']
                cmd.append(db_name)

                pg_version = "%d.%d" % divmod(cr._obj.connection.server_version / 100, 100)
                cr.execute("SELECT name, latest_version FROM ir_module_module WHERE state = 'installed'")
                modules = dict(cr.fetchall())
                manifest = {
                    'odoo_dump': '1',
                    'db_name': db_name,
                    'version': odoo.release.version,
                    'version_info': odoo.release.version_info,
                    'major_version': odoo.release.major_version,
                    'pg_version': pg_version,
                    'modules': modules,
                }

                with tempfile.TemporaryDirectory() as dump_dir:
                    filestore = odoo.tools.config.filestore(db_name)
                    if os.path.exists(filestore):
                        shutil.copytree(filestore, os.path.join(dump_dir, 'filestore'))
                    with open(os.path.join(dump_dir, 'manifest.json'), 'w') as fh:
                        db = odoo.sql_db.db_connect(db_name)
                        with db.cursor() as cr:
                            json.dump(manifest, fh, indent=4)
                    cmd.insert(-1, '--file=' + os.path.join(dump_dir, 'dump.sql'))
                    odoo.tools.exec_pg_command(*cmd)
                    odoo.tools.osutil.zip_dir(dump_dir, fp, include_dir=False, fnct_sort=lambda file_name: file_name != 'dump.sql')

                fp.close()
                # Backup on Docker
                shutil.move(file_path, FILE_BACKUP_PATH)


                #try:
                #    import paramiko
                #    host = '10.8.0.53'
                #    port = 22
                #    password = 'unduhdata'
                #    username = 'bakuser'

                #    ssh = paramiko.SSHClient()
                #    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                #    ssh.connect(host, port, username, password)
                #
                #    sftp = ssh.open_sftp()
                #
                #    remotepath = "/bakuser/kgs/{bkp_file}".format(bkp_file=bkp_file)
                #    localpath = "/etc/odoo/backups/{bkp_file}".format(bkp_file=bkp_file)
                #    sftp.put(localpath, remotepath)
                #
                #    sftp.close()
                #    ssh.close()
                #    import os
                #    if os.path.exists("/etc/odoo/backups/{bkp_file}".format(bkp_file=bkp_file)):
                #        os.remove("/etc/odoo/backups/{bkp_file}".format(bkp_file=bkp_file))
                #except Exception as e:
                #    print(e)

