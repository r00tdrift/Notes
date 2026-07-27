# Networking

Scripts for network recon, connections, and remote access during labs/CTFs.

## Contents

- **ssh_key_shell.py** — Interactive SSH client that authenticates with a private key instead of a password. Generalized from a one-off script used on the DeathNote VM (previously hardcoded to a specific IP/user/key path) so it now works against any target.

### Dependencies

```bash
pip install paramiko cryptography
```

### Usage

```bash
python3 ssh_key_shell.py --host 192.168.56.110 --user kira --key ~/l_id_rsa
python3 ssh_key_shell.py --host 10.10.10.10 --user root --key ./id_rsa --port 2222
```

If the key is passphrase-protected, add `--passphrase "yourpassphrase"`.

### Notes

- For authorized labs, CTFs, and personal VMs only.
- Supports RSA and Ed25519 keys; other paramiko-supported key types may need a small addition to `load_key()`.
