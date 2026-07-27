# <Challenge / Box Name>

- **Platform:** HackTheBox / TryHackMe / CTF name
- **Difficulty:** Easy / Medium / Hard
- **Category:** Web / Network / Crypto / Forensics / Reversing / Pwn
- **Date:** YYYY-MM-DD
- **Tags:** `nmap` `sqli` `privesc` ...

## Summary

One or two sentences describing the target and the overall path to compromise/solve.

## Reconnaissance

```bash
nmap -sC -sV -oN nmap.txt <target>
```

Findings:
- Port XX/tcp — service, version
- Port XX/tcp — service, version

## Enumeration

Describe what you found while enumerating each open service/port.

## Exploitation

Describe the vulnerability, how you confirmed it, and the exploitation steps. Include commands and relevant output.

```bash
# exploit commands here
```

## Privilege Escalation

```bash
# privesc enumeration / exploitation commands
```

## Flags / Proof

- User flag: `<hash or redacted>`
- Root/system flag: `<hash or redacted>`

## Lessons Learned

- Key takeaway 1
- Key takeaway 2

## References

- [Link to relevant technique writeup]()
- [Link to CVE / advisory]()
