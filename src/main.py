import os
import shutil
import sys

from generate_page import generate_pages_recursive

def main():

    basepath = '/'

    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    initiate_public_folder('static', 'docs')
    generate_pages_recursive('content/', 'template.html', 'docs/', basepath)



def initiate_public_folder(src, dst):
    #src = os.path.abspath(src)
    #dst = os.path.abspath(dst)

    if not os.path.exists(src) or not os.path.isdir(src):
        print("Source path is not a directory or it doesn't exists")
        sys.exit(1)

    if os.path.exists(dst) and os.path.isdir(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)

    _recursive_copy(src,dst)


def _recursive_copy(src, dst):

    current_dir_items = os.listdir(src)
    
    for item in current_dir_items:
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f'Copying {src_path} to {dst_path}')
            
        elif os.path.isdir(src_path):
            os.mkdir(dst_path)
            _recursive_copy(src_path, dst_path)


if __name__ == "__main__":
    main()