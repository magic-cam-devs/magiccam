import argparse
from zipfile import ZipFile
from fileutils import get_all_file_paths

from googleapiclient import discovery
from googleapiclient.http import MediaFileUpload
from oauth2client import file, client, tools


import httplib2
import os

check_point_dir = os.path.join('checkpoint',
                               'StarGAN_celebA_wgan-gp_6resblock_6dis')

SCOPES = 'https://www.googleapis.com/auth/drive'

# https://drive.google.com/drive/u/2/folders/1Hxosl5LZrxSn3LcDYm1JgPjuabHtjiQy
STARGAN_MODEL_FOLDER_ID = '1Hxosl5LZrxSn3LcDYm1JgPjuabHtjiQy'

store = file.Storage('storage.json')
# httplib2.debuglevel = 2                             # Enable debug log


parser = argparse.ArgumentParser(description='Upload all file in directory to GDrive')

parser.add_argument('--dir', type=str, default='.',
                    help='The directory contain the file you want to upload')


def init():
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
        creds = tools.run_flow(flow, store)
    DRIVE = discovery.build('drive', 'v3', http=creds.authorize(httplib2.Http()))
    return DRIVE


def upload_to_gdrive(drive, file_path: str):
    file_name = os.path.basename(file_path)
    DRIVE = drive

    file_metadata = {
        'name': file_name,
        'parents': [STARGAN_MODEL_FOLDER_ID]
    }
    media = MediaFileUpload(filename=file_path, resumable=True)

    uploaded = DRIVE.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
    print('File {} uploaded with ID: {}'.format(file_name, uploaded['id']))


if __name__ == '__main__':
    args = parser.parse_args()
    file_paths = get_all_file_paths(args.dir)

    print('Following files will be zipped and upload to GDrive:')
    for file_path in file_paths:
        print(file_path)

    dir_basename = os.path.basename(args.dir)
    zip_file = '{}.zip'.format(dir_basename)
    with ZipFile(zip_file, 'w') as zf:
        for file_path in file_paths:
            zf.write(file_path)

    drive = init()
    upload_to_gdrive(drive, zip_file)

    os.remove(zip_file)
