from bs4 import BeautifulSoup
import os

images_extentions = ('.png','.jpeg','.jpg','.gif')

print("Searching All Images....")
all_images = [os.path.join(dirpath,filename) for dirpath, _, filenames in os.walk('.') for filename in filenames if filename.endswith(images_extentions)]
all_files = [os.path.join(dirpath,filename) for dirpath, _, filenames in os.walk('.') for filename in filenames if filename.endswith(('.html'))]
all_images = list(set(all_images))

images_not_found = []
images_used = []
images_not_used = []

print("Reading All HTML Files...")
for file in all_files:
    page = open(file)
    print("Opening - ", file)
    soup = BeautifulSoup(page.read(),"html.parser")
    html_images = soup.find_all('img')
    for h_images in html_images:
        accurate_image = ".\\website\\"+h_images.get("src").replace("/", "\\")
        if accurate_image in all_images:
            images_used.append(accurate_image)
        else:
            images_not_found.append(accurate_image)

images_used = list(set(images_used))
images_not_found = list(set(images_not_found))
not_used_images = list(set(all_images) - set(images_used))
total_not_used_images_filesize = [(os.path.getsize(image_filesize)/float(1<<20)) for image_filesize in not_used_images]
space_free = round(sum(total_not_used_images_filesize),2)

print("Total Images - ",len(all_images) ,all_images)
print("Images Used in HTML Code - ", len(images_used),images_used)
print("Images Not Found - ",len(images_not_found) ,images_not_found)
print("Extra Images - ", len(not_used_images) ,not_used_images)
print("Extra Images Total Size - ",space_free,"MB")

if space_free != 0:
    is_delete = input("Do you want to Delete Extra Images? Free up - "+str(space_free)+" MB \n Yes/No : ")
    if is_delete.lower() == "yes":
        for image in not_used_images:
            os.remove(image)
            print('Removed - ', image )
        print(space_free,"MB","got free!")