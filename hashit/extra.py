"""Extra functions and classes for hashit"""
import binascii
import hashlib

# final class
class Crc32:
    """This class is an api for the crc32 function that is compatible with mor"""
    def __init__(self, data=b''):
        """init class, creates data""" 
        self.name = "crc32"
        self.data = data

    def update(self, data=b''):
        """Update self.data with new data"""
        self.data += data

    def copy(self):
        """return new Crc32 object with same properties"""
        return Crc32(self.data)

    def digest(self):
        """Digest as int"""
        return binascii.crc32(self.data) & 0xFFFFFFFF

    def hexdigest(self):
        """Digest as hex"""
        buf = (binascii.crc32(self.data) & 0xFFFFFFFF)
        return ("%08X" % buf).lower()
        
# class for shake hash
class shake:
    """Top-level api for hashlib.shake"""
    def __init__(self, hashname, data=b''):
        """Init class create hasher and data"""
        if hashname[:5] == "shake":
            self.hash = hashlib.shake_256(data)
            self.name = hashname
            self.length = int(hashname.split("_")[1])
        else:
            raise ValueError

    def update(self, data=b''):
        """Update self.data with new data"""
        self.hash.update(data)

    def copy(self):
        return self.hash.copy()

    def digest(self, length=None):
        """Digest binary"""
        length = length or self.length
        return self.hash.digest(length)
    
    def hexdigest(self, length=None):
        """Digest hex"""
        length = length or self.length
        return self.hash.hexdigest(length)


LINUX_LIST = ['Mythbuntu', 'Mac OS X', 'Debian Pure Blend', 'Symphony OS', 'Astra Linux', 'Emdebian Grip',\
    'Russian Fedora Remix', 'Secure-K', 'Knopperdisk', 'Mobilinux', 'touchscreen', 'MX Linux', 'NepaLinux', 'fli4l', 'Nix', 'Ubuntu Mobile', 'primary',\
    'Fedora Core', 'ChromeOS', 'rPath', 'LEAF Project', 'MuLinux', 'Ubuntu',\
    'Berry Linux', 'dyne:bolic', 'TurnKey GNU/Linux', 'EasyPeasy', 'Budgie', 'Tin Hat Linux', 'paldo', 'Conary', 'Ubuntu Touch', 'netbooks', 'Emmabuntus',\
    'Linpus Linux Lite', 'Poseidon Linux', 'Elive', 'Source Mage', 'Skolelinux', 'Ubuntu MATE', 'Ubuntu Kylin', 'Solus', 'Nova', 'MeeGo', 'Pinguy OS', 'Nokia N9',\
    'Kanotix', 'Korora', 'Linux Mint', 'Billix', 'Linpus Linux', 'Ubuntu JeOS', 'XFCE', 'TinyMe', 'VectorLinux', 'Antergos', 'Asianux', 'BlankOn', 'Netrunner',\
    'Trisquel GNU/Linux', 'Tinfoil Hat Linux', 'Familiar Linux', 'Sentry Firewall', 'Fedora', 'Parsix', 'MythTV', 'Castile-La Mancha', 'Pardus', 'Austrumi Linux',\
    'Bodhi Linux', 'OpenZaurus', 'SME Server', 'Mandrake 9.2', 'Frugalware Linux', 'Coyote Linux', 'Sorcerer', 'senior citizens',\
    'Red Flag Linux', 'Chakra Linux', 'Arch Linux', 'Caldera OpenLinux', 'cAos Linux', 'Red Hat', 'EnGarde Secure Linux', 'Annvix',\
    'Feather Linux', 'CoreOS', 'Gentoox', 'SUSE Studio', 'Red Hat Linux', 'SmoothWall', 'Goobuntu', 'SystemRescueCD', 'Peppermint OS', 'Wolvix',\
    'Iskolinux', 'Ubuntu Netbook Edition', 'Lunar Linux', 'Guadalinex', 'bioinformatics', 'Network Security Toolkit', 'The Amnesic Incognito Live System',\
    'Container Linux', 'ELinOS', 'Aurora', 'LinuxMCE', 'antiX', 'GeeXboX', 'Foresight Linux', 'RXART', 'Prevas Industrial Linux', 'thin client',\
    'Parabola GNU/Linux-libre', 'Go', 'Ututo', 'Dreamlinux', 'Sunwah Linux', 'LOUD', 'Yellow Dog Linux', 'Trinity Rescue Kit',\
    'Miracle Linux', 'Hanthana', 'ROSA Linux', 'Munich', 'OpenGEU', 'BackTrack', 'Calculate Linux', 'Sabayon Linux', 'Chromium OS', 'Platypux', 'Xfce', 'ArchBang',\
    'Baltix', 'Mageia', 'MontaVista Linux', 'SUSE Linux Enterprise Server', 'Joli OS', 'SolydXK', 'DNALinux', 'SalineOS', 'Fermi Linux LTS', 'SliTaz',\
    'Android', 'KDE', 'Sacix', 'LliureX', 'Xubuntu', 'musl', 'Univention Corporate Server', 'Red Hat Enterprise Linux', 'Ubuntu for Android', 'ALT Linux',\
    'Canaima', 'Kurumin', 'Moblin', 'Vyatta', 'Kubuntu', 'Pentoo', 'GIS', 'Topologilinux', 'WinLinux', 'autonomic',\
    'CentOS', 'CRUX', 'Trustix','Galsoft Linux', 'Sugar-on-a-Stick Linux', 'BackBox', 'simpleLinux', 'Smallfoot', 'BackSlash Linux', 'HandyLinux',\
    'Funtoo Linux', 'Element OS', 'Ubuntu Budgie', 'YOPER', 'Xbox', 'Corel Linux', 'Webconverger', 'PelicanHPC', 'HostGIS',\
    'Yggdrasil Linux/GNU/X', 'BLAG Linux and GNU', 'LinHES', 'Raspbian', 'gNewSense', 'Slackintosh', 'OpenWrt', 'SalixOS', 'Qubes OS', 'One-Laptop-Per-Child project',\
    'Unity Linux', 'Mezzo', 'MythDora', 'Gobuntu', 'Fuduntu', 'CrunchBang Linux', 'Bharat Operating System Solutions', 'Italy', 'Enlightenment','Aurora SPARC Linux',\
    'Sabily', 'GNU Guix', 'PowerPC', 'MAX', 'SteamOS', 'Raspberry Pi Foundation', 'Mandriva Linux', 'Ubuntu GNOME', 'MkLinux', 'Frozen', 'Karoshi', 'Damn Small Linux',\
    'ZipSlack', 'MEPIS', 'Scientific Linux', 'Kuki Linux', 'LiMux', 'Finnix', 'SuperGamer', 'NimbleX', 'Slamd64', 'grml', 'Ubuntu Server', 'Alpine Linux', 'Dragora GNU/Linux-Libre',\
    'Fermi National Accelerator Laboratory', 'Porteus', 'NixOS', 'Generalitat Valenciana', 'Jlime', 'Puppy Linux', 'Tiny Core Linux', 'tomsrtbt', 'Edubuntu', 'OpenMandriva',\
    'Thinstation', 'elementary OS', 'Void Linux', 'Rocks Cluster Distribution', 'Lubuntu', 'gOS', 'Ubuntu TV', 'Openbox', 'Sharp Zaurus', 'PS2 Linux', 'MintPPC', 'Kali Linux',\
    'Qimo 4 Kids', 'Nitix', 'SUSE Linux Enterprise Desktop', 'GendBuntu', 'Buildix', 'Impi Linux', 'Linux Lite', 'Guix System Distribution', 'Turbolinux', 'Maemo',\
    'Softlanding Linux System', 'SUSE', 'EduLinux', 'Debian Live', 'OpenTV', 'Daylight Linux', 'Manjaro Linux', 'Nagra', 'Slax', 'Caldera', 'UberStudent',\
    'MCC Interim Linux', 'Oracle Linux', 'K12LTSP', 'Devuan', 'OjubaLinux', 'Xandros', 'Molinux', 'openSUSE', 'SparkyLinux', 'DSLinux', 'GoboLinux',\
    'LinuxTLE', 'MATE', 'Zenwalk', 'Andalucia', 'LinuxBBQ', 'Slackware', 'Vine Linux', 'PCLinuxOS', 'Vinux', 'Musix GNU+Linux',\
    'Ubuntu Studio', 'Knoppix', 'ClearOS', 'Hikarunix', 'NASLite', 'KateOS', 'LTSP', 'Mandrake Linux', 'Nokia N800']
