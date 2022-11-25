### VCENTER VM DELETED ALERT
# VMware vcenter vsphere >6.5 - Virtual Machine deleted alert

Vmware vCenter in its different versions does not allow the option to send alerts due to the deletion of virtual machines(VM).

This code allows you to read the records of the database associated with the deletion of VM's and send a warning email to whoever needs to know

<ol> 
 <li> Install required libraries</li>


```console
tdnf install -y gcc python3-devel
pip3 install psycopg2-binary
 ```
 
 
 <li> Create automation directory </li>
 
 
```console
mkdir /opt/custom-alerts
vim /opt/custom-alerts/vm-deleted-alarm.py
```
 
 <li> Vcenter BD password </li>
Obtain the vcenter database password

```console
cat /etc/vmware-vpx/vcdb.properties 
```

Copy password to *VCENTER_DB_PASSWORD*
```console
MAIL_SEND_TO = ['your-email@example.com']
VCENTER_DB_PASSWORD = 'vcenter-db-password'
MAILSERVER_IP = 'mail-server-IP'
TIME_STAMP_FILE = 'lastrun-timestamp.txt'
ORGANIZATION_DOMAIN = '@org.com'
```

<li> Create contrab</li>
Create crontab for executing VM deletion events

```console
crontab -e
0 10 * * * /usr/bin/python3.5 /opt/custom-alerts/vm-deleted-alarm.py > /var/log/custom-alerts.log
```

</ol>
