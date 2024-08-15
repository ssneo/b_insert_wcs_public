import os, sys




os.system("docker stop b_insert_wcs")


os.system("docker rm b_insert_wcs")


os.system("docker image rm b_insert_wcs")

os.system("docker build . --platform linux/x86_64 -t b_insert_wcs")


os.system("docker run -t -d --platform linux/amd64 -v ~/research/dap:/dap -v ~/research/dap_data:/dap_data -v ~/research/dap_index_files:/dap_index_files --name b_insert_wcs b_insert_wcs")


os.system("docker exec -it b_insert_wcs bash")


