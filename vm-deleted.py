import psycopg2
import socket
import smtplib
import datetime

MAIL_SEND_TO = ['your-email@example.com']
VCENTER_DB_PASSWORD = 'vcenter-db-password'
MAILSERVER_IP = 'mail-server-IP'
TIME_STAMP_FILE = 'lastrun-timestamp.txt'


def send_mail_error_mail(e):
    from_mail_address = socket.getfqdn().split('.')[0] + '@yourdomain.com'

    msj = 'Subject: Execution error on VM alert \n\n' \
          'Vcenter: ' + socket.getfqdn() + '\n' \
          'Execution Error: \n' + str(e) + '\n' \
          +'\n\n\n'
    # connection to mail server
    server = smtplib.SMTP(MAILSERVER_IP)
    server.sendmail(from_mail_address, MAIL_SEND_TO, msj)
    server.quit()


def send_deleted_vm_alert(data):
    try:
        #get data from row
        vm_name = data[1]
        username = data[2]
        from_mail_address = socket.getfqdn().split('.')[0] + '@yourdomain.com'
        start_time = '{0:%Y-%m-%d %H:%M:%S}'.format(data[3])


        #set mail format
        msj = 'Subject: Virtual Machine deleted \n\n' \
               'A Virtual machine has been deleted\n' +\
               'Vcenter: ' + socket.getfqdn() + '\n'\
               'VM name: '+vm_name +'\n' \
               'Executed by: ' + username +'\n' \
               'Start task time: ' + start_time + 'UTC\n\n\n'


        #connection to mail server
        server = smtplib.SMTP(MAILSERVER_IP)
        server.sendmail(from_mail_address, MAIL_SEND_TO, msj)
        server.quit()
    except Exception as e:
            print(e)

def save_timestamp_last_run():
    with open(TIME_STAMP_FILE,'w+') as f:
        f.write('{}'.format(datetime.datetime.utcnow()))
    f.close()

def recover_timestamp_last_run():
    with open(TIME_STAMP_FILE, 'r') as f:
        last_run_timestamp = f.readline().replace('\n','')
        last_run_timestamp =datetime.datetime.strptime(last_run_timestamp,'%Y-%m-%d %H:%M:%S.%f') - datetime.timedelta(minutes=10)
        last_run_timestamp = '{}'.format(last_run_timestamp)

    f.close()
    return last_run_timestamp


if __name__ == '__main__':

    try:
        conn = psycopg2.connect(host='127.0.0.1',dbname='VCDB',port=5432,user='vc',password=VCENTER_DB_PASSWORD)
        cur = conn.cursor()
        query_string = "SELECT entity_id,entity_name,username,start_time " \
                        "FROM vpx_task WHERE " \
                    "descriptionid='vim.VirtualMachine.destroy' and" \
                    " start_time > '" + recover_timestamp_last_run() + "';"

        cur.execute(query_string)

        rows = cur.fetchall()
        for row in rows:
            send_deleted_vm_alert(row)

        cur.close()
        conn.close()

        save_timestamp_last_run()
    except Exception as e:
        send_mail_error_mail(e)
