import yaml
import subprocess
from color import AsciiColor

hosts = []
USER = ""
TUNNEL = ""
KEY_PATH = ""
COMMAND = ""
PORT = "22"

def read_recursion(key, data):
    if not isinstance(data, dict):
        return

    if data.get('ansible_host'):
        hosts.append({
            'name': key,
            'ip': data.get('ansible_host')
        })
        return

    for k in data:
        read_recursion(k, data[k])

def read_yml():
    global USER
    global TUNNEL
    global KEY_PATH
    global COMMAND
    global PORT

    with open("user.yml", "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        USER = data['user']
        TUNNEL = data['tunnel']
        KEY_PATH = data['key_path']
        COMMAND = data['command'] if data['command'] else "echo"
        PORT = data['port']

    with open("input.yml", "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    read_recursion("", data)
    print(hosts)
    print(AsciiColor.blue('total: ' + str(len(hosts)) + ' servers'))
    print('--------------------------')

def ssh(host):
    name = host['name']
    ip = host['ip']

    cmd = ['ssh', '-p', PORT, '-i', KEY_PATH, '-o', 'StrictHostKeyChecking=no', USER + '@' + ip, COMMAND]
    if ip[:6] == '10.200':
        cmd = ['ssh', '-p', PORT, '-i', KEY_PATH, '-o', 'StrictHostKeyChecking=no', '-J', USER + '@' + TUNNEL, USER + '@' + ip, COMMAND]
    result = subprocess.run(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    return {
        'name': name,
        'cmd': cmd,
        'stdout': result.stdout.decode("utf-8"),
        'stderr': result.stderr.decode("utf-8") if result.stderr else ""
    }

if __name__ == "__main__":
    read_yml()
    errors = []
    done = []

    for host in hosts:
        result = ssh(host)
        print(result)
        if result['stderr']:
            s = "%s %s" %(host['name'], result['stderr'])
            errors.append(s)
            print(AsciiColor.red('[ERROR]'), s)
        else:
            done.append(host['name'])
            print(AsciiColor.green('[OK]'), host, '\n')

    with open('error-log.txt', 'w') as f:
        for error in errors:
            f.write(error)

    with open('done-log.txt', 'w') as f:
        for d in done:
            f.write(d)
