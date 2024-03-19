from css_html_js_minify import process_single_html_file, process_single_js_file, \
    process_single_css_file
import os
import shutil
from bs4 import BeautifulSoup
import sys


class ProjectOptimizer:
    def __init__(self, CODE_DIRECTORY, OPTIMIZED_DIRECTORY):
        self.HTML_REMOVE_UNUSED_IMAGES_ERROR_MSG = None
        self.HTML_REMOVE_UNUSED_IMAGES_ERROR = False
        self.total_not_used_images_filesize = 0
        self.not_used_images = []
        self.space_free = 0
        self.all_images = []
        self.HTML_READ_ERROR_MSG = None
        self.JS_COMPRESS_ERROR_MSG = None
        self.CSS_COMPRESS_ERROR_MSG = None
        self.images_not_found = []
        self.images_used = []
        self.images_extentions = ('.png', '.jpeg', '.jpg', '.gif')
        self.HTML_READ_ERROR = False
        self.total_js_file_size = 0
        self.CSS_COMPRESS_ERROR = False
        self.JS_COMPRESS_ERROR = False
        self.all_css = []
        self.total_css_file_size = 0
        self.HTML_COMPRESS_ERROR_MSG = None
        self.total_html_file_size = 0
        self.all_html = []
        self.all_js = []
        self.HTML_COMPRESS_ERROR = False
        self.REAL_CODE_DIRECTORY = CODE_DIRECTORY
        self.CLONE_CODE_DIRECTORY = OPTIMIZED_DIRECTORY
        self.CreateClone()

    def CreateClone(self) -> bool:
        try:
            shutil.rmtree(self.CLONE_CODE_DIRECTORY)
        except:
            pass
        print("Cloning the Code...")
        shutil.copytree(self.REAL_CODE_DIRECTORY, self.CLONE_CODE_DIRECTORY)
        return True

    def FindAllHTML(self) -> list:
        print("Searching for HTML Files...")
        self.all_html = [os.path.join(dirpath, filename) for dirpath, _, filenames in
                         os.walk(self.CLONE_CODE_DIRECTORY)
                         for
                         filename in filenames if filename.endswith('.html')]
        return self.all_html

    def FindAllCSS(self) -> list:
        print("Searching for HTML Files...")
        self.all_css = [os.path.join(dirpath, filename) for dirpath, _, filenames in
                        os.walk(self.CLONE_CODE_DIRECTORY)
                        for
                        filename in filenames if filename.endswith('.css')]
        return self.all_css

    def FindAllJS(self) -> list:
        print("Searching for HTML Files...")
        self.all_js = [os.path.join(dirpath, filename) for dirpath, _, filenames in
                       os.walk(self.CLONE_CODE_DIRECTORY)
                       for
                       filename in filenames if filename.endswith('.js')]
        return self.all_js

    def CompressHTML(self, comments=False) -> bool:
        try:
            print("Compressing HTML Files...")
            for html_file in self.all_html:
                self.total_html_file_size += os.path.getsize(html_file) / float(1 << 20)
                process_single_html_file(html_file, overwrite=True, comments=comments)
            return True
        except Exception as e:
            self.HTML_COMPRESS_ERROR = True
            self.HTML_COMPRESS_ERROR_MSG = e
            print("HTML ERROR", e, file=sys.stderr)
            return False

    def CompressCSS(self, comments=False) -> bool:
        try:
            print("Compressing CSS Files...")
            for css_file in self.all_css:
                self.total_css_file_size += os.path.getsize(css_file) / float(1 << 20)
                process_single_css_file(css_file, overwrite=True, comments=comments)
                return True
        except Exception as e:
            self.CSS_COMPRESS_ERROR = True
            self.CSS_COMPRESS_ERROR_MSG = e
            print("CSS ERROR", e, file=sys.stderr)
            return False

    def CompressJS(self) -> bool:
        try:
            print("Compressing JS Files...")
            for js_file in self.all_js:
                self.total_js_file_size += os.path.getsize(js_file) / float(1 << 20)
                process_single_js_file(js_file, overwrite=True)
            return True
        except Exception as e:
            self.JS_COMPRESS_ERROR = True
            self.JS_COMPRESS_ERROR_MSG = e
            print("JS ERROR", e, file=sys.stderr)
            return False

    def FindImagesInProjectHTML(self) -> bool:
        try:
            self.all_images = [os.path.join(dirpath, filename) for dirpath, _, filenames in
                               os.walk(self.CLONE_CODE_DIRECTORY)
                               for
                               filename in filenames if filename.endswith(self.images_extentions)]
            self.all_images = list(set(self.all_images))

            print("Reading All HTML Files...")
            for file in self.all_html:
                page = open(file)
                print("Opening - ", file)
                soup = BeautifulSoup(page.read(), "html.parser")
                html_images = soup.find_all('img')
                for h_images in html_images:
                    accurate_image = ".\\website\\" + h_images.get("src").replace("/", "\\")
                    print(accurate_image)
                    if accurate_image in self.all_images:
                        self.images_used.append(accurate_image)
                    else:
                        self.images_not_found.append(accurate_image)
            return True
        except Exception as e:
            self.HTML_READ_ERROR = True
            self.HTML_READ_ERROR_MSG = e
            print("HTML READING ERROR: ", e, file=sys.stderr)
            return False

    def RemoveUnUsedImages(self):
        try:
            print("Searching UnUsed Images...")
            self.space_free = 0
            self.not_used_images = []
            if not self.HTML_READ_ERROR:
                self.images_used = list(set(self.images_used))
                self.images_not_found = list(set(self.images_not_found))
                self.not_used_images = list(set(self.all_images) - set(self.images_used))
                self.total_not_used_images_filesize = [(os.path.getsize(image_filesize) / float(1 << 20)) for
                                                       image_filesize in
                                                       self.not_used_images]
                self.space_free = round(sum(self.total_not_used_images_filesize), 2)

            if self.space_free > 0:
                print("Removing UnUsed Images...")
                for image in self.not_used_images:
                    os.remove(image)
                    print('Removed - ', image)
                print(self.space_free, "MB", "got free!")
            return True
        except Exception as e:
            self.HTML_REMOVE_UNUSED_IMAGES_ERROR = True
            self.HTML_REMOVE_UNUSED_IMAGES_ERROR_MSG = e
            print("HTML READING ERROR: ", e, file=sys.stderr)
            return False


test = ProjectOptimizer(r"./code/", r"./optimized/")

test.CreateClone()
test.FindAllHTML()
test.FindAllJS()
test.FindAllCSS()
test.FindImagesInProjectHTML()
test.RemoveUnUsedImages()
test.CompressHTML()
test.CompressJS()
test.CompressCSS()


