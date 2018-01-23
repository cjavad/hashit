<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html><head><title>Python: module hashit.__main__</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head><body bgcolor="#f0f0f8">

<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="heading">
<tr bgcolor="#7799ee">
<td valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial">&nbsp;<br><big><big><strong><a href="hashit.html"><font color="#ffffff">hashit</font></a>.__main__</strong></big></big> (version 3.3.3a0)</font></td
><td align=right valign=bottom
><font color="#ffffff" face="helvetica, arial"><a href=".">index</a><br><a href="file:/home/javad/Dropbox/playground/hashit/hashit/__main__.py">/home/javad/Dropbox/playground/hashit/hashit/__main__.py</a></font></td></tr></table>
    <p><tt>Command&nbsp;line&nbsp;program&nbsp;for&nbsp;hashit<br>
&nbsp;<br>
this&nbsp;module&nbsp;"__main__"&nbsp;contains&nbsp;all&nbsp;the&nbsp;code&nbsp;for&nbsp;argparsing,&nbsp;running<br>
and&nbsp;anything&nbsp;needed&nbsp;for&nbsp;an&nbsp;command&nbsp;lin&nbsp;application&nbsp;such&nbsp;as&nbsp;hashit.<br>
&nbsp;<br>
it&nbsp;uses&nbsp;argc&nbsp;another&nbsp;package&nbsp;by&nbsp;me,&nbsp;but&nbsp;i&nbsp;am&nbsp;considering&nbsp;switching&nbsp;to&nbsp;argparse</tt></p>
<p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#aa55cc">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial"><big><strong>Modules</strong></big></font></td></tr>
    
<tr><td bgcolor="#aa55cc"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>
<td width="100%"><table width="100%" summary="list"><tr><td width="25%" valign=top><a href="hashlib.html">hashlib</a><br>
</td><td width="25%" valign=top><a href="json.html">json</a><br>
</td><td width="25%" valign=top><a href="os.html">os</a><br>
</td><td width="25%" valign=top><a href="random.html">random</a><br>
</td></tr></table></td></tr></table><p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#eeaa77">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial"><big><strong>Functions</strong></big></font></td></tr>
    
<tr><td bgcolor="#eeaa77"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>
<td width="100%"><dl><dt><a name="-Exit"><strong>Exit</strong></a> = exit(...)</dt><dd><tt>exit([status])<br>
&nbsp;<br>
Exit&nbsp;the&nbsp;interpreter&nbsp;by&nbsp;raising&nbsp;SystemExit(status).<br>
If&nbsp;the&nbsp;status&nbsp;is&nbsp;omitted&nbsp;or&nbsp;None,&nbsp;it&nbsp;defaults&nbsp;to&nbsp;zero&nbsp;(i.e.,&nbsp;success).<br>
If&nbsp;the&nbsp;status&nbsp;is&nbsp;an&nbsp;integer,&nbsp;it&nbsp;will&nbsp;be&nbsp;used&nbsp;as&nbsp;the&nbsp;system&nbsp;exit&nbsp;status.<br>
If&nbsp;it&nbsp;is&nbsp;another&nbsp;kind&nbsp;of&nbsp;object,&nbsp;it&nbsp;will&nbsp;be&nbsp;printed&nbsp;and&nbsp;the&nbsp;system<br>
exit&nbsp;status&nbsp;will&nbsp;be&nbsp;one&nbsp;(i.e.,&nbsp;failure).</tt></dd></dl>
 <dl><dt><a name="-config"><strong>config</strong></a>(argv)</dt><dd><tt>Sets&nbsp;argvs'&nbsp;config&nbsp;and&nbsp;commands</tt></dd></dl>
 <dl><dt><a name="-main"><strong>main</strong></a>(args=None)</dt><dd><tt>Main&nbsp;function&nbsp;with&nbsp;error&nbsp;catching,&nbsp;can&nbsp;force-exit&nbsp;with&nbsp;os._exit(1)<br>
&nbsp;<br>
this&nbsp;main&nbsp;function&nbsp;calls&nbsp;<a href="#-main_">main_</a>()&nbsp;and&nbsp;cathes&nbsp;any&nbsp;error&nbsp;while&nbsp;giving&nbsp;the&nbsp;user&nbsp;a&nbsp;"pretty"<br>
error.</tt></dd></dl>
 <dl><dt><a name="-main_"><strong>main_</strong></a>(args=None)</dt><dd><tt>Main&nbsp;function&nbsp;which&nbsp;is&nbsp;the&nbsp;cli&nbsp;parses&nbsp;arguments&nbsp;and&nbsp;runs&nbsp;appropriate&nbsp;commands</tt></dd></dl>
 <dl><dt><a name="-walk"><strong>walk</strong></a>(goover)</dt><dd><tt>Goes&nbsp;over&nbsp;a&nbsp;path&nbsp;an&nbsp;finds&nbsp;all&nbsp;files,&nbsp;appends&nbsp;them&nbsp;to&nbsp;a&nbsp;list&nbsp;and&nbsp;returns&nbsp;that&nbsp;list</tt></dd></dl>
</td></tr></table><p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#55aa55">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial"><big><strong>Data</strong></big></font></td></tr>
    
<tr><td bgcolor="#55aa55"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>
<td width="100%"><strong>GLOBAL</strong> = {'ACCESS': True, 'BLANK': (None, True), 'COLORS': {'GREEN': '<font color="#c040c0">\x1b</font>[0;32m', 'RED': '<font color="#c040c0">\x1b</font>[0;31m', 'RESET': '<font color="#c040c0">\x1b</font>[0m', 'YELLOW': '<font color="#c040c0">\x1b</font>[0;33m'}, 'DEFAULTS': {'APPEND': False, 'COLORS': True, 'DETECT': None, 'HASH': 'md5', 'MEMOPT': False, 'QUIET': False, 'SIZE': False, 'STRIP': False}, 'DEVMODE': True, 'ERRORS': {'FileNotFoundError': "Error, file seems to be missing calling systemd to confirm 'sure you haved checked the MBR?'", 'OSError': {'END': 'JDK, so something happend with your os, message: ', 'linux': 'So {} , to be continued...<font color="#c040c0">\n</font>', 'macos': 'Macos (Sierra+) and OSX (El Captain-) thank god for apples naming', 'windows': 'Windows 10, windows 8(.1), windows 7 (sp*), wind...p*), windows 98/95, windows NT *. OK not that bad'}, 'TypeError': 'Wrong type used (in cli-arguments) - please use a static programming language'}, 'EXTRA': {'crc32': &lt;class 'hashit.extra.Crc32'&gt;}, 'HASH_STR': 'Hello World!', 'MESSAGES': {'CUR_FORM': 'current format is', 'EMPTY_CHK': 'checksum file is empty', 'FAIL': 'FAILED', 'FILE_NOT': 'File does not exist', 'HASH_NOT': 'is not a valid hash', 'LOAD_FAIL': 'Failed to load', 'MAYBE': 'Did you maybe mean:', 'OK': 'OK', 'PERM_ERR': 'could not be accessed', 'WORKS_ON': 'is not guaranteed to work on your system', ...}, 'SNAP_PATH': '/var/lib/snapd/hostfs', ...}<br>
<strong>LINUX_LIST</strong> = ['Mythbuntu', 'Mac OS X', 'Debian Pure Blend', 'RPM', 'Symphony OS', 'Astra Linux', 'Emdebian Grip', 'Russian Fedora Remix', 'Secure-K', 'Knopperdisk', 'Mobilinux', 'touchscreen', 'MX Linux', 'NepaLinux', 'fli4l', 'Nix', 'Ubuntu Mobile', 'primary', 'Fedora Core', 'ChromeOS', ...]<br>
<strong>__algorithms__</strong> = ['DSA', 'md4', 'sha', 'md5', 'sha1', 'crc32', 'sha224', 'sha384', 'sha256', 'sha512', 'DSA-SHA', 'blake2b', 'blake2s', 'ripemd160', 'whirlpool', 'dsaWithSHA', 'dsaEncryption', 'ecdsa-with-SHA1']<br>
<strong>__license__</strong> = 'MIT, Copyrigth (c) 2017-present Javad Shafique'</td></tr></table><p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#7799ee">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial"><big><strong>Author</strong></big></font></td></tr>
    
<tr><td bgcolor="#7799ee"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>
<td width="100%">Javad&nbsp;Shafique</td></tr></table>
</body></html>