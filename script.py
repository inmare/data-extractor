import zipfile
import os

package_dir = "playlist_generator"

file_name = package_dir + ".zip"
file_exists = os.path.exists(file_name)
if file_exists:
    os.remove(file_name)


zipf = zipfile.ZipFile(
    file_name,
    "w",
    zipfile.ZIP_DEFLATED,
)

files = os.listdir(package_dir)

for file in files:
    zipf.write(os.path.join(package_dir, file), file)

zipf.close()
