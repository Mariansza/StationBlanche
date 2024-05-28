import os
import subprocess
import sys

def scan_file(file_path):
    try:
        result = subprocess.run(['clamscan', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        if "OK" in output:
            print(f"Le fichier {file_path} est propre.")
            return True
        else:
            print(f"Le fichier {file_path} est infecté.")
            print(output)
            return False
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'analyse {file_path}: {str(e)}")
        return False

def scan_directory(directory_path):
    infected_files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if not scan_file(file_path):
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

if __name__ == "__main__":
    usb_mount_point = find_usb_mount_point()

    if not usb_mount_point:
        print("Aucune clé USB montée n'a été trouvée.")
        sys.exit(1)

    print(f"Clé USB trouvée et montée sur: {usb_mount_point}")

    if os.path.isfile(usb_mount_point):
        print(f"Scan du fichier: {usb_mount_point}")
        if scan_file(usb_mount_point):
            print("Aucun fichier infecté trouvé.")
        else:
            print("Fichier infecté trouvé. /n Analyse du système avec Chkrootkit...")
            if scan_system_with_chkrootkit():
                print("Le système est propre.")
            else:
                print("Le système est infecté par un rootkit.")

    elif os.path.isdir(usb_mount_point):
        print(f"Analyse du dossier: {usb_mount_point}")
        infected_files = scan_directory(usb_mount_point)
        if infected_files:
            print("Fichiers infectés trouvés:")
            for file in infected_files:
                print(file)
            print ("Analyse du système avec Chkrootkit...")
            if scan_system_with_chkrootkit():
                print("Le système est propre.")
            else:
                print("Le système est infecté par un rootkit.")
        else:
            print("Aucun fichier infecté trouvé.")
    else:
        print(f"Le chemin fourni n'est ni un fichier ni un répertoire: {usb_mount_point}")
        sys.exit(1)