from css_html_js_minify import process_single_html_file, process_single_js_file, \
    process_single_css_file
import os
import shutil
from bs4 import BeautifulSoup
import sys



def OptimizeProject(REAL_CODE_DIRECTORY=r"./code/", CLONE_CODE_DIRECTORY=r"./Optimized Code/",
                    images_extentions=('.png', '.jpeg', '.jpg', '.gif'), COMPRESS_HTML=True, COMPRESS_CSS=True,
                    COMPRESS_JS=True, OPTIMIZE_HTML_IMAGE_CODE=True, COMPRESS_IMAGE=False):
    global JS_COMPRESS_ERROR, JS_COMPRESS_ERROR, HTML_READ_ERROR, CODE_IMAGE_OPTIMIZED
    try:
        shutil.rmtree(CLONE_CODE_DIRECTORY)
    except:
        pass

    print("Cloning the Code...")
    shutil.copytree(REAL_CODE_DIRECTORY, CLONE_CODE_DIRECTORY)

    print("Searching for HTML Files...")
    all_html = [os.path.join(dirpath, filename) for dirpath, _, filenames in os.walk(CLONE_CODE_DIRECTORY) for filename
                in filenames if filename.endswith(('.html'))]
    print("Searching for CSS Files...")
    all_css = [os.path.join(dirpath, filename) for dirpath, _, filenames in os.walk(CLONE_CODE_DIRECTORY) for filename
               in filenames if filename.endswith(('.css'))]
    print("Searching for JS Files...")
    all_js = [os.path.join(dirpath, filename) for dirpath, _, filenames in os.walk(CLONE_CODE_DIRECTORY) for filename in
              filenames if filename.endswith(('.js'))]
    print("Searching All Images....")
    all_images = [os.path.join(dirpath, filename) for dirpath, _, filenames in os.walk('.') for filename in filenames if
                  filename.endswith(images_extentions)]
    all_files = [os.path.join(dirpath, filename) for dirpath, _, filenames in os.walk('.') for filename in filenames if
                 filename.endswith(('.html'))]
    all_images = list(set(all_images))

    images_not_found = []
    images_used = []
    images_not_used = []

    total_html_file_size = 0
    total_css_file_size = 0
    total_js_file_size = 0

    HTML_COMPRESS_ERROR = False

    if COMPRESS_HTML:
        print("Compressing HTML Files...")
        try:
            for html_file in all_html:
                total_html_file_size += os.path.getsize(html_file) / float(1 << 20)
                process_single_html_file(html_file, overwrite=True, comments=False)
        except Exception as e:
            HTML_COMPRESS_ERROR = True
            print("HTML ERROR", e, file=sys.stderr)

    CSS_COMPRESS_ERROR = False

    if COMPRESS_CSS:
        print("Compressing CSS Files...")
        try:
            for css_file in all_css:
                total_css_file_size += os.path.getsize(css_file) / float(1 << 20)
                process_single_css_file(css_file, overwrite=True, comments=False)
        except Exception as e:
            CSS_COMPRESS_ERROR = True
            print("CSS ERROR", e, file=sys.stderr)

    if COMPRESS_JS:
        JS_COMPRESS_ERROR = False
        print("Compressing JS Files...")
        try:
            for js_file in all_js:
                total_js_file_size += os.path.getsize(js_file) / float(1 << 20)
                process_single_js_file(js_file, overwrite=True)
        except Exception as e:
            JS_COMPRESS_ERROR = True
            print("JS ERROR", e, file=sys.stderr)

    if OPTIMIZE_HTML_IMAGE_CODE:
        HTML_READ_ERROR = False
        print("Reading All HTML Files...")
        try:
            for file in all_files:
                page = open(file)
                print("Opening - ", file)
                soup = BeautifulSoup(page.read(), "html.parser")
                html_images = soup.find_all('img')
                for h_images in html_images:
                    accurate_image = ".\\website\\" + h_images.get("src").replace("/", "\\")
                    if accurate_image in all_images:
                        images_used.append(accurate_image)
                    else:
                        images_not_found.append(accurate_image)
        except Exception as e:
            HTML_READ_ERROR = True
            print("HTML READING ERROR: ", e, file=sys.stderr)

        space_free = 0
        not_used_images = []
        if not HTML_READ_ERROR and OPTIMIZE_HTML_IMAGE_CODE:
            images_used = list(set(images_used))
            images_not_found = list(set(images_not_found))
            not_used_images = list(set(all_images) - set(images_used))
            total_not_used_images_filesize = [(os.path.getsize(image_filesize) / float(1 << 20)) for image_filesize in
                                              not_used_images]
            space_free = round(sum(total_not_used_images_filesize), 2)

            print("Total Images - ", len(all_images), all_images)
            print("Images Used in HTML Code - ", len(images_used), images_used)
            print("Images Not Found - ", len(images_not_found), images_not_found)
            print("Extra Images - ", len(not_used_images), not_used_images)
            print("Extra Images Total Size - ", space_free, "MB")

        CODE_IMAGE_OPTIMIZED = False
        if space_free != 0:
            is_delete = input("Do you want to Delete Extra Images? Free up - " + str(space_free) + " MB \n Yes/No : ")
            if is_delete.lower() == "yes":
                CODE_IMAGE_OPTIMIZED = True
                for image in not_used_images:
                    os.remove(image)
                    print('Removed - ', image)
                print(space_free, "MB", "got free!")

    total_compressed_html_file_size = [0]
    total_compressed_css_file_size = [0]
    total_compressed_js_file_size = [0]

    if not HTML_COMPRESS_ERROR and COMPRESS_HTML:
        total_compressed_html_file_size = [(os.path.getsize(html_file) / float(1 << 20)) for html_file in all_html]
    if not CSS_COMPRESS_ERROR and COMPRESS_CSS:
        total_compressed_css_file_size = [(os.path.getsize(css_file) / float(1 << 20)) for css_file in all_css]
    if not JS_COMPRESS_ERROR and COMPRESS_JS:
        total_compressed_js_file_size = [(os.path.getsize(js_file) / float(1 << 20)) for js_file in all_js]

    total_html_file_size = round(total_html_file_size, 2)
    total_css_file_size = round(total_css_file_size, 2)
    total_js_file_size = round(total_js_file_size, 2)

    total_compressed_html_file_size = round(sum(total_compressed_html_file_size), 2)
    total_compressed_css_file_size = round(sum(total_compressed_css_file_size), 2)
    total_compressed_js_file_size = round(sum(total_compressed_js_file_size), 2)

    total_real_filesize = total_html_file_size + total_css_file_size + total_js_file_size
    total_compressed_filesize = total_compressed_html_file_size + total_compressed_css_file_size + total_compressed_js_file_size
    total_filesize_difference = total_real_filesize - total_compressed_filesize

    print("Real HTML File Size:", total_html_file_size, "MB")
    print("Real CSS File Size:", total_css_file_size, "MB")
    print("Real JS File Size:", total_js_file_size, "MB")
    print("")
    print("Compressed HTML File Size:", total_compressed_html_file_size, "MB")
    print("Compressed CSS File Size:", total_compressed_css_file_size, "MB")
    print("Compressed JS File Size:", total_compressed_js_file_size, "MB")
    print("Total Compressed File Size:", total_compressed_filesize, "MB")
    print("")
    print("Total Real Code File Size:", total_real_filesize, "MB")
    print("Code Bandwidth Saved :", total_filesize_difference, "MB")
    print("Total(Code + Images) Bandwidth Saved / Free Up Space :", total_filesize_difference + space_free, "MB")

    if HTML_COMPRESS_ERROR and COMPRESS_HTML:
        print("HTML FILE NOT COMPRESSED DUE TO SOME ERROR, PLEASE SCROLL TO SEE THE ERROR", file=sys.stderr)

    if CSS_COMPRESS_ERROR and COMPRESS_CSS:
        print("CSS FILE NOT COMPRESSED DUE TO SOME ERROR, PLEASE SCROLL TO SEE THE ERROR", file=sys.stderr)

    if JS_COMPRESS_ERROR and COMPRESS_JS:
        print("JS FILE NOT COMPRESSED DUE TO SOME ERROR, PLEASE SCROLL TO SEE THE ERROR", file=sys.stderr)

    if HTML_READ_ERROR and OPTIMIZE_HTML_IMAGE_CODE:
        print("HTML FILE READING ERROR , PLEASE SCROLL TO SEE THE ERROR", file=sys.stderr)

    if not HTML_COMPRESS_ERROR and COMPRESS_HTML:
        print("HTML COMPRESSED SUCESSFULLY")
    if not CSS_COMPRESS_ERROR and COMPRESS_CSS:
        print("CSS COMPRESSED SUCCESSFULLY")
    if not JS_COMPRESS_ERROR and COMPRESS_JS:
        print("JS COMPRESSED SUCCESSFULLY")
    if not HTML_READ_ERROR and CODE_IMAGE_OPTIMIZED and OPTIMIZE_HTML_IMAGE_CODE:
        print("CODE IMAGES OPTIMIZED SUCCESSFULLY")


OptimizeProject()
