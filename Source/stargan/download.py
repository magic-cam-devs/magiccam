import os
import zipfile
import argparse
import requests

from tqdm import tqdm

parser = argparse.ArgumentParser(description='Download dataset, labels, model checkpoint for StarGAN')

parser.add_argument('--type', choices=['dataset', 'labels', 'checkpoint'], default='labels',
                    help='Available type: dataset, labels, checkpoint')

parser.add_argument('--name', metavar='N', type=str, nargs='+', choices=['celebA'],
                    help='name of dataset to download [celebA]')


def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None


def save_response_content(response, destination, chunk_size=32 * 1024):
    total_size = int(response.headers.get('content-length', 0))
    with open(destination, "wb") as f:
        for chunk in tqdm(response.iter_content(chunk_size), total=total_size,
                          unit='B', unit_scale=True, desc=destination):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


def prepare_data_dir(path='./dataset'):
    if not os.path.exists(path):
        os.makedirs(path)


def create_dir_if_not_exists(dir_path: str):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def download_labels(dataset_name: str):
    dataset_dir = os.path.join('dataset', dataset_name)
    create_dir_if_not_exists(dataset_dir)

    celebA_label_file, file_id = 'list_attr_celeba.txt', '1MzjafP6o7TRVtf-_tn-q4fj6C5903uaq'
    celebA_label_file_path = os.path.join(dataset_dir, celebA_label_file)

    if os.path.exists(celebA_label_file_path):
        print('[*] {} already exists'.format(celebA_label_file_path))
    else:
        download_file_from_google_drive(file_id, celebA_label_file_path)
        print('[*] Download {} complete.'.format(celebA_label_file))


def download_checkpoint():
    file_name = "checkpoint.zip"
    save_path = os.path.join(".", file_name)
    download_file_from_google_drive("1ezwtU1O_rxgNXgJaHcAynVX8KjMt0Ua-", save_path)

    with zipfile.ZipFile(save_path) as zf:
        zf.extractall(".")


def download_dataset(dataset_name: str):
    if not dataset_name == 'celebA':
        return

    dirpath = 'dataset'

    data_dir = 'celebA'
    celebA_dir = os.path.join(dirpath, data_dir)
    prepare_data_dir(celebA_dir)

    file_name, drive_id = "img_align_celeba.zip", "1S2WCmNlNC2INXy2g8qf5vqgjqYmR0wvi"
    save_path = os.path.join(dirpath, file_name)

    if os.path.exists(save_path):
        print('[*] {} already exists'.format(save_path))
    else:
        download_file_from_google_drive(drive_id, save_path)

    with zipfile.ZipFile(save_path) as zf:
        zf.extractall(celebA_dir)

    # os.remove(save_path)
    os.rename(os.path.join(celebA_dir, 'img_align_celeba'), os.path.join(celebA_dir, 'train'))

    custom_data_dir = os.path.join(celebA_dir, 'test')
    prepare_data_dir(custom_data_dir)


if __name__ == '__main__':
    args = parser.parse_args()
    dataset_name = args.name

    if args.type == 'labels':
        download_labels(dataset_name)

    if args.type == 'checkpoint':
        download_checkpoint()

    if args.type == 'dataset':
        download_dataset(dataset_name)
