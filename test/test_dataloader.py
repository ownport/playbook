import os
import pytest

from playbook.dataloader import DataLoader
from playbook.errors import PlaybookFileNotFound

ONE_PLAY_DUMP = [
    { 'vars': { 'http_port': 80, 'max_clients': 200, },
      'tasks': [
        {'name': 'ensure apache is at the latest version', 'yum': 'name=httpd state=latest'},
        {'name': 'write the apache config file', 'template': 'src=/srv/httpd.j2 dest=/etc/httpd.conf'},
        {'name': 'ensure apache is running (and enable it at boot)', 'service': 'name=httpd state=started enabled=yes'}]}
]

FEW_PLAYS_DUMP = [
    { 'vars': { 'http_port': 80, 'max_clients': 200,},
      'tasks': [ {'name': 'ensure apache is at the latest version', 'yum': 'name=httpd state=latest'} ] },
    { 'vars': { 'http_port': 80, 'max_clients': 200,},
      'tasks': [ {'name': 'ensure apache is at the latest version', 'yum': 'name=httpd state=latest'} ] }
]

def get_resource_path(filename):
    return  os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


def test_dataloader_load_non_exists_file():

    with pytest.raises(PlaybookFileNotFound):
        assert DataLoader().load_from_file('non-exists.json') == None


def test_dataloader_load_file_one_play_yaml():

    resource_path = get_resource_path('resources/one-play.yaml')
    dl = DataLoader()
    assert  dl.load_from_file(resource_path) == ONE_PLAY_DUMP
    assert  dl.load_from_file(resource_path) == ONE_PLAY_DUMP


def test_dataloader_load_file_one_play_json():

    assert DataLoader().load_from_file(get_resource_path('resources/one-play.json')) == ONE_PLAY_DUMP


def test_dataloader_load_str_unicode():

    assert DataLoader().load(u'---\n[]') == []
    assert DataLoader().load(u'---\n') == []


def test_dataloader_load_none():

    assert DataLoader().load(None) == None


def test_dataloader_load_empty_str():

    assert DataLoader().load('') == None


def test_dataloader_load_file_few_plays_yaml():

    assert DataLoader().load_from_file(get_resource_path('resources/few-plays.yaml')) == FEW_PLAYS_DUMP


def test_dataloader_load_file_few_plays_json():

    assert DataLoader().load_from_file(get_resource_path('resources/few-plays.json')) == FEW_PLAYS_DUMP


def test_dataloader_load_file_with_incorrect_format():

    assert DataLoader().load_from_file(get_resource_path('resources/incorrect-file-format.json')) == None
