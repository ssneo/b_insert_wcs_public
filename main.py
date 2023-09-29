import os, sys


os.system("docker stop b_insert_wcs")
os.system("docker rm b_insert_wcs")

os.system("docker image rm b_insert_wcs")

os.system("docker build . --platform linux/x86_64 -t b_insert_wcs")

#
if sys.platform == 'darwin':
    os.system("docker run -t -d --platform linux/amd64 --expose=5432 -v ~/research/dap:/dap -v ~/research/dap_data:/dap_data -v ~/research/dap_index_files:/dap_index_files --name b_insert_wcs b_insert_wcs")
else:
    os.system("docker run -d -v C:\\Users\\tlind\\research\\dap:/dap -v C:\\Users\\tlind\\research\\dap_data:/dap_data C:\\Users\\tlind\\research\\dap_index_files:/dap_index_files --name dap dap")
os.system("docker exec -it b_insert_wcs bash")

#os.system("docker run -it -v ~/research/dap:/dap -v ~/research/dap_data:/dap_data --name dap dap")