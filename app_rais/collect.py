# package for dowloading data from the web
import wget
import os
from itertools import product
import glob
import py7zr


def download_rais(list_ufs, list_year):
    '''
    Downloads data files from RAIS ftp server to their respective subdirectories in "data\\rais_original\\".
    '''

    modulepath = os.path.dirname(__file__)

    for year, uf in product(list_year, list_ufs):
        year = str(year)
        if year == '2018':
            break
        else:
            directory = os.path.join(modulepath, f'data/rais_original/{year}/')
            os.makedirs(directory, exist_ok=True)
            
            if not os.path.isfile(os.path.join(directory, uf + year[:] + '.7z')):
                year = str(year) + '/'
                link = 'ftp://ftp.mtps.gov.br/pdet/microdados/RAIS/' + year + uf + year[:-1] + '.7z'

                zipfile = os.path.join(directory, uf.upper() + year[:-1] + '.7z')
                wget.download(url=link, 
                            out=zipfile)

                print(f' - {zipfile} downloaded.')


def extract_rais_original(path_pattern, remove_7z=True):
    """
    Extracts all available 7zip files inside the rais_original subdirectories.
    
    """
#    modulepath = os.path.dirname(__file__)

#    path_pattern = modulepath + 'data/rais_original/**/*.7z'

    list_files = glob.glob(path_pattern, recursive=True)
    for file in list_files:
        base = os.path.splitext(file)[0]
        
        if not os.path.isfile(base + '.txt'):
            
            try:
                with py7zr.SevenZipFile(file, mode='r') as z: 
                    z.extractall(path=os.path.dirname(file))
                if remove_7z == True: 
                    os.remove(file)
                
                print(f'"{base}.txt" extracted.')

            except:
                print(f'"{base}.txt" could not be extracted')
        else:
            if remove_7z == True:
                os.remove(file)
            print(f'"{base}.txt" already present.')