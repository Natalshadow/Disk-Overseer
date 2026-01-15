import os, pathlib
import shutil
import psutil
from gotify import Gotify
from dotenv import load_dotenv


load_dotenv() 

# Now you can pull your variables safely
GOTIFY_TOKEN = os.getenv("GOTIFY_TOKEN")
GOTIFY_URL = os.getenv("GOTIFY_URL")

##config##
gotify = Gotify(
    base_url=GOTIFY_URL,
    app_token=GOTIFY_TOKEN,
)


def check_diskusage():
    disk_total, disk_used, disk_free = shutil.disk_usage("/home/")
    print((disk_total))

    # Convert bytes to Gigabytes
    x = disk_total/1000000000
    y = disk_used/1000000000
    z = disk_free/1000000000

    # Cast to integer for human-readable output (approximation)
    hr_disktotal = int(x)
    hr_diskused = int(y)
    hr_diskfree = int(z)
    print("total |  used  |  free")
    print(hr_disktotal, "g | ", hr_diskused, "g | ", hr_diskfree, "g")

    # Calculate the usage ratio
    calc = hr_diskused/hr_disktotal

    print(calc)
    return calc


# The function now uses the local parameter 'calc'
def trigger(calc):
    
    print(calc)
    threshold = 0.76
    
    # Using the local parameter 'calc' instead of the global 'disk_ratio'
    if calc < threshold:
        print("Ok.")
        triggered = False
    elif calc >= threshold:
        print("Error. Not enough space. Running diagnostics.")
        triggered = True
    else:
        print("There is an issue and the value wasn't computed.")
    return triggered


def disk_analysis(triggered):
    print(f"Value is {triggered}")
    if triggered:
        size = os.stat("/home/").st_size
        print(f"{size}G")
        send_gotify()
    else:
        print("Not triggered.")


def top_biggest(path, n=10):
    items = []
    for (root, dirs, files) in os.walk(path, topdown=True):
        for name in files:
            try:
                full_path = os.path.join(root, name)
                size = os.path.getsize(full_path)
                items.append((full_path, size))
            except FileNotFoundError:
                pass
    items.sort(key=lambda x: x[1], reverse=True)
    return items[:n]

top_10 = top_biggest("/var/", n=10)
for f, s in top_10:
    print(f,s/1024**2, "MB")

def send_gotify():
    gotify.create_message(
        "Disk space issue detected.",
        title="DiskOverseer",
        priority=0,
    )




def main():
    print("This script is made to monitor the disk space available on my server and notify in case of low space.\n")

    print("Checking disk usage:\n")
    disk_ratio = check_diskusage()
    print("Bytes gathered, converting...\n")
    print("Checking threshold value...\n")
    alarm = trigger(disk_ratio)
    print("Checking if threshold triggered...\n")
    analysis = disk_analysis(alarm)






main()
