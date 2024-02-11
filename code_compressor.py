from css_html_js_minify import process_single_html_file, process_single_js_file,\
    process_single_css_file
import os
import shutil


def OptimizeCode(REAL_CODE_DIRECTORY=r"./website/",CLONE_CODE_DIRECTORY=r"./Optimized Code/"):

    try:
        shutil.rmtree(CLONE_CODE_DIRECTORY)
    except:
        pass

    shutil.copytree(REAL_CODE_DIRECTORY, CLONE_CODE_DIRECTORY)

    all_html = [os.path.join(dirpath,filename) for dirpath, _, filenames in os.walk(CLONE_CODE_DIRECTORY) for filename in filenames if filename.endswith(('.html'))]
    all_css = [os.path.join(dirpath,filename) for dirpath, _, filenames in os.walk(CLONE_CODE_DIRECTORY) for filename in filenames if filename.endswith(('.css'))]
    all_js = [os.path.join(dirpath,filename) for dirpath, _, filenames in os.walk(CLONE_CODE_DIRECTORY) for filename in filenames if filename.endswith(('.js'))]

    total_html_file_size = 0
    total_css_file_size = 0
    total_js_file_size = 0

    for html_file in all_html:
        total_html_file_size += os.path.getsize(html_file)/float(1<<20)
        process_single_html_file(html_file, overwrite=True, comments=False)

    for css_file in all_css:
        total_css_file_size += os.path.getsize(css_file) / float(1 << 20)
        process_single_css_file(css_file, overwrite=True)

    for js_file in all_js:
        total_js_file_size += os.path.getsize(js_file) / float(1 << 20)
        process_single_js_file(js_file, overwrite=True)

    total_compressed_html_file_size = [(os.path.getsize(html_file)/float(1<<20)) for html_file in all_html]
    total_compressed_css_file_size = [(os.path.getsize(css_file)/float(1<<20)) for css_file in all_css]
    total_compressed_js_file_size = [(os.path.getsize(js_file)/float(1<<20)) for js_file in all_js]

    total_html_file_size = round(total_html_file_size,2)
    total_css_file_size = round(total_css_file_size,2)
    total_js_file_size = round(total_js_file_size,2)

    total_compressed_html_file_size = round(sum(total_compressed_html_file_size),2)
    total_compressed_css_file_size = round(sum(total_compressed_css_file_size),2)
    total_compressed_js_file_size = round(sum(total_compressed_js_file_size),2)

    total_real_filesize = total_html_file_size + total_css_file_size + total_js_file_size
    total_compressed_filesize = total_compressed_html_file_size + total_compressed_css_file_size + total_compressed_js_file_size
    total_filesize_difference = total_real_filesize - total_compressed_filesize

    print("Real HTML File Size:",total_html_file_size,"MB")
    print("Real CSS File Size:",total_css_file_size,"MB")
    print("Real JS File Size:",total_js_file_size,"MB")
    print("\n")
    print("Compressed HTML File Size:",total_compressed_html_file_size,"MB")
    print("Compressed CSS File Size:",total_compressed_css_file_size,"MB")
    print("Compressed JS File Size:",total_compressed_js_file_size,"MB")
    print("Total Compressed File Size:",total_compressed_filesize,"MB")
    print("\n")
    print("Total Real Code File Size:",total_real_filesize,"MB")
    print("Compressed Code File Size:",total_filesize_difference,"MB")

OptimizeCode(REAL_CODE_DIRECTORY="code")