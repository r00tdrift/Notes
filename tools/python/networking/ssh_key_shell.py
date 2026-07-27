#!/usr/bin/env python3
"""
ssh_key_shell.py

A reusable interactive SSH client using paramiko + an SSH private key.
Originally built for the DeathNote VM (key-based SSH as user 'kira'),
generalized here so target IP, username, and key path are all
provided as arguments instead of hardcoded.

Educational use only — for authorized labs, CTFs, and personal VMs.

Usage:
    python3 ssh_key_shell.py --host 192.168.56.110 --user kira --key ~/l_id_rsa
    python3 ssh_key_shell.py --host 10.10.10.10 --user root --key ./id_rsa --port 2222
"""

import argparse
import io
import select
import sys

import paramiko
from cryptography.hazmat.primitives import serialization


def load_key(key_path: str, passphrase: str | None = None) -> paramiko.PKey:
    """Load an SSH private key (any common format) and return a paramiko key object."""
    with open(key_path, "rb") as f:
        key_data = f.read()

    private_key = serialization.load_ssh_private_key(
        key_data,
        password=passphrase.encode() if passphrase else None,
    )
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # paramiko can load RSA, Ed25519, ECDSA, etc. — try RSA first, then fall back
    key_file = io.StringIO(pem.decode())
    try:
        return paramiko.RSAKey.from_private_key(key_file)
    except paramiko.SSHException:
        key_file.seek(0)
        return paramiko.Ed25519Key.from_private_key(key_file)


def interactive_shell(channel: paramiko.Channel) -> None:
    """Relay an interactive shell session between the local terminal and the remote channel."""
    while True:
        if channel.recv_ready():
            data = channel.recv(9999).decode(errors="replace")
            sys.stdout.write(data)
            sys.stdout.flush()
        if channel.exit_status_ready() and not channel.recv_ready():
            break
        if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
            line = sys.stdin.readline()
            if not line:
                break
            channel.send(line)


def main() -> None:
    parser = argparse.ArgumentParser(description="Interactive SSH shell using a private key.")
    parser.add_argument("--host", required=True, help="Target host/IP.")
    parser.add_argument("--user", required=True, help="SSH username.")
    parser.add_argument("--key", required=True, help="Path to the SSH private key.")
    parser.add_argument("--port", type=int, default=22, help="SSH port (default: 22).")
    parser.add_argument("--passphrase", default=None, help="Passphrase for the key, if any.")
    args = parser.parse_args()

    try:
        pkey = load_key(args.key, args.passphrase)
    except FileNotFoundError:
        print(f"[!] Key file not found: {args.key}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"[!] Failed to load key: {exc}", file=sys.stderr)
        sys.exit(1)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(args.host, port=args.port, username=args.user, pkey=pkey)
    except Exception as exc:
        print(f"[!] Connection failed: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Connected to {args.user}@{args.host}:{args.port}")
    channel = client.invoke_shell()

    try:
        interactive_shell(channel)
    except KeyboardInterrupt:
        print("\n[*] Interrupted, closing connection.")
    finally:
        client.close()


if __name__ == "__main__":
    main()
