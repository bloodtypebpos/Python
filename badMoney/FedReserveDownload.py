import os
import requests

dbDir = r'C:\Users\Matt\Desktop\BadMoney'

def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))

for y in range(19,22):
    for m in range(1,13):
        for d in range(1,32):
            dd = str(d)
            mm = str(m)
            yy = str(y)
            if len(dd) < 2:
                dd = "0" + dd
            if len(mm) < 2:
                mm = "0" + mm
            f = yy + mm + dd + "00.xlsx"
            url = "https://fsapps.fiscal.treasury.gov/dts/files/" + f
            print(url)
            if y == 19:
                if m > 7:
                    download(url, dest_folder=dbDir)
            else:
                if y > 19:
                    download(url, dest_folder=dbDir)
            print("-----------------------------------------------------")





