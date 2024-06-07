import os
import subprocess
import sys

def scan_file_clamav(file_path):
    try:
        result = subprocess.run(['clamscan', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        if "OK" in output:
            print(f"ClamAV: Le fichier {file_path} est propre.")
            return True
        else:
            print(f"ClamAV: Le fichier {file_path} est infecté.")
            return False
    except Exception as e:
        print(f"ClamAV: Une erreur s'est produite lors de l'analyse {file_path}: {str(e)}")
        return False
    
def scan_file_sophos(file_path):
    try:
        result = subprocess.run(['/opt/sophos-av/bin/savscan', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            output = result.stdout.decode('utf-8')
        except UnicodeDecodeError:
            output = result.stdout.decode('latin-1')
        if ">>> Virus" not in output:
            print(f"Sophos: Le fichier {file_path} est propre.")
            return True 
        else: 
            print(f"Sophos: Le fichier {file_path} est infecté.")
            return False
    except Exception as e:
        print(f"Sophos: Une erreur s'est produite lors de l'analyse {file_path}: {str(e)}")
        return False

def scan_directory_clamav(directory_path):
    infected_files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if not scan_file_clamav(file_path):
                infected_files.append(file_path)
    return infected_files

def scan_directory_sophos(directory_path):
    infected_files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if not scan_file_sophos(file_path):
                infected_files.append(file_path)
    return infected_files

def scan_system_with_chkrootkit():
    try:
        result = subprocess.run(['sudo', 'chkrootkit'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        print(output)
        if "INFECTED" in output:
            print("Le système est infecté par un rootkit.")
            return False
        else:
            print("Aucun rootkit trouvé sur le système.")
            return True
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'analyse du système avec Chkrootkit: {str(e)}")
        return False

def find_usb_mount_point():
    try:
        result = subprocess.run(['lsblk', '-o', 'NAME,MOUNTPOINT'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        lines = output.strip().split('\n')
        for line in lines[1:]:
            parts = line.split()
            if len(parts) == 2 and '/media' in parts[1]:
                return parts[1]
        return None
    except Exception as e:
        print(f"Une erreur s'est produite lors de la détection de la clé USB montée: {str(e)}")
        return None

def delete_infected_files(infected_files):
    for file in infected_files:
        try:
            os.remove(file)
            print(file)
        except Exception as e:
            print(f"Une erreur s'est produite lors de la suppression du fichier {file}: {str(e)}")

def unmount_usb(mount_point):
    try:
        result = subprocess.run(['sudo', 'umount', mount_point], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(f"La clé USB montée sur {mount_point} a été démontée avec succès.")
        else:
            print(f"Une erreur s'est produite lors du démontage de la clé USB montée sur {mount_point}.")
    except Exception as e:
        print(f"Une erreur s'est produite lors du démontage de la clé USB: {str(e)}")


def main_scan():
    usb_mount_point = find_usb_mount_point()

    if not usb_mount_point:
        print("Aucune clé USB montée n'a été trouvée.")
        sys.exit(1)

    print(f"Clé USB trouvée et montée sur: {usb_mount_point}")

    if os.path.isdir(usb_mount_point):
        print(f"Analyse du dossier: {usb_mount_point}")
        clamav_infected_files = scan_directory_clamav(usb_mount_point)
        print(f"Première analyse terminée.")
        sophos_infected_files = scan_directory_sophos(usb_mount_point)
        print(f"Deuxième analyse terminée.")
        all_infected_files = set(clamav_infected_files + sophos_infected_files)
        if all_infected_files:
            print("Fichiers infectés trouvés et supprimés:")
            delete_infected_files(all_infected_files)
            print("Analyse du système avec Chkrootkit...")
            if scan_system_with_chkrootkit():
                print("Le système est propre.")
            else:
                print("Le système est infecté par un rootkit.")
            print("Relance de l'analyse complète...")
            main_scan()
        else:
            print("Aucun fichier infecté trouvé.")
            unmount_usb(usb_mount_point)
    else:
        print(f"Le chemin fourni n'est ni un fichier ni un répertoire: {usb_mount_point}")
        sys.exit(1)

if __name__ == "__main__":
    main_scan()