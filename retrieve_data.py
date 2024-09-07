import requests


def get_source_material(source_url, file_path, file_format):
    # set query parameters:
    query_params = {'downloadformat': file_format}
    # retrieve data from url:
    response = requests.get(source_url, params=query_params)
    # save data to harddisk:
    if response.ok:
        with open(file_path, mode='wb') as file:
            file.write(response.content)
            print('saved requested data in:', file_path)
    else:
        print('unable to retrieve requested data from:', url)