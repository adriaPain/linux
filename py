import platform
import psutil
import subprocess

def get_system_info():
    # Informations générales sur le système
    print(f"Nom de l'ordinateur : {platform.node()}")
    print(f"Système d'exploitation : {platform.system()} {platform.release()}")
    print(f"Version du noyau : {platform.uname().release}")
    print(f"Architecture du processeur : {platform.machine()}")
    print(f"Fabricant : {get_dmidecode_info('system-manufacturer')}")
    print(f"Modèle : {get_dmidecode_info('system-product-name')}")

    # Informations sur le processeur
    cpu_info = subprocess.check_output(['lscpu']).decode('utf-8')
    print(f"Processeur : {get_cpu_info('Model name', cpu_info)}")
    print(f"Nombre de cœurs de processeur : {get_cpu_info('CPU(s)', cpu_info)}")
    print(f"Nombre total de processeurs : {psutil.cpu_count(logical=False)}")

    # Informations sur la mémoire
    mem_info = psutil.virtual_memory()
    print(f"Mémoire totale : {format_bytes(mem_info.total)}")

    # Informations sur le disque dur
    disk_info = psutil.disk_usage('/')
    print(f"Espace disque total : {format_bytes(disk_info.total)}")

    # Informations sur les utilisateurs
    print("Utilisateurs du système :")
    for user in psutil.users():
        print(f"   - {user.name}")

    # Informations sur les logiciels installés (pour les systèmes basés sur Debian)
    print("Logiciels installés :")
    try:
        installed_packages = subprocess.check_output(['dpkg', '-l']).decode('utf-8')
        for line in installed_packages.split('\n')[5:]:
            if line:
                print(f"   - {line.split()[1]}")
    except subprocess.CalledProcessError:
        print("Impossible de récupérer la liste des logiciels installés.")

    # Informations sur les mises à jour (pour les systèmes basés sur Debian)
    print("Mises à jour installées :")
    try:
        updates_count = subprocess.check_output(['apt', 'list', '--installed']).count(b'installed')
        print(f"   - {updates_count}")
    except subprocess.CalledProcessError:
        print("Impossible de récupérer le nombre de mises à jour installées.")

def get_dmidecode_info(keyword):
    try:
        output = subprocess.check_output(['sudo', 'dmidecode', '-s', keyword]).decode('utf-8').strip()
        return output if output else "N/A"
    except subprocess.CalledProcessError:
        return "N/A"

def get_cpu_info(keyword, cpu_info):
    for line in cpu_info.split('\n'):
        if keyword in line:
            return line.split(':')[1].strip()
    return "N/A"

def format_bytes(bytes):
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}B"
        bytes /= 1024

if __name__ == "__main__":
    get_system_info()
