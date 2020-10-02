import wget # package for dowloading data from the web
import os
from itertools import product


def obtain_rais(list_ufs = ['PR', 'RS', 'PE'], list_year=['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']):
    '''
    Downloads RAIS files from ftp to their respective directories
    It doesn't work for 2018
    '''
    for year, uf in product(list_year, list_ufs):
        if year == '2018':
            break
        directory = os.path.join(os.getcwd(), 'data\\rais\\', str(year) + '\\')
        os.makedirs(directory, exist_ok=True)
        if not os.path.isfile(os.path.join(directory, uf + year[:] + '.7z')):
            year = str(year) + '/'
            link = 'ftp://ftp.mtps.gov.br/pdet/microdados/RAIS/' + year + uf + year[:-1] + '.7z'
            wget.download(url=link, 
                        out= os.path.join(directory, uf + year[:-1] + '.7z'))