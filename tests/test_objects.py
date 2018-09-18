import pytest
import json
import os
from cmdb.object_framework import CmdbObjectManager, CmdbTypeCategory, CmdbObjectStatus, CmdbObject, CmdbObjectLog

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'fixtures',
)

ALL_JSON = pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, 'objects.data.logs.json'),
    os.path.join(FIXTURE_DIR, 'objects.data.json')
)


@pytest.fixture
def database_manager():
    import os
    from cmdb.data_storage.database_connection import MongoConnector
    from cmdb.data_storage.database_manager import DatabaseManagerMongo
    return DatabaseManagerMongo(
        connector=MongoConnector(
            host=os.environ["TEST_HOST"],
            port=int(os.environ["TEST_PORT"]),
            database_name=os.environ['TEST_DATABASE'],
            timeout=100
        )
    )


@pytest.fixture
def object_manager(database_manager):
    return CmdbObjectManager(
        database_manager=database_manager
    )


@ALL_JSON
@pytest.fixture
def objects_data_json(datafiles):
    datalist = {}
    for j in datafiles.listdir():
        with open(j) as json_file:
            datalist.update({
                json_file.name.rsplit('/', 1)[1]: json.load(json_file)
            })
    return datalist


@ALL_JSON
def test_cmdb_object(objects_data_json):
    test_object = CmdbObject(**objects_data_json['objects.data.json'][0])
    assert type(test_object) == CmdbObject


@ALL_JSON
def test_cmdb_object_logs(objects_data_json):
    from cmdb.object_framework.cmdb_object import ActionNotPossibleError
    from datetime import datetime
    test_log = CmdbObjectLog(**objects_data_json['objects.data.logs.json'][0])
    assert test_log._action == 'create'
    assert test_log.editor == 1
    assert test_log.message == "Default"
    assert len(test_log.log) == 0
    assert type(test_log.date) == str

    with pytest.raises(ActionNotPossibleError):
        CmdbObjectLog(**objects_data_json['objects.data.logs.json'][1])


def test_object_categories(object_manager):
    default_category = CmdbTypeCategory(
        public_id=object_manager.dbm.get_highest_id(CmdbTypeCategory.COLLECTION) + 1,
        name='default',
        label='Default',
    )
    assert default_category.is_empty() is True

    inserted_id = object_manager.insert_category(default_category.to_database())
    assert inserted_id == 1
    del_ack = object_manager.delete_category(inserted_id)
    assert del_ack.acknowledged is True

    d1 = CmdbTypeCategory(
        public_id=object_manager.dbm.get_highest_id(CmdbTypeCategory.COLLECTION) + 1,
        name='default',
        label='Default',
    )
    assert d1.get_name() == 'default'
    assert d1.get_label() == 'Default'
    assert d1.has_icon() is False
    object_manager.insert_category(d1.to_database())
    d2 = CmdbTypeCategory(
        public_id=object_manager.dbm.get_highest_id(CmdbTypeCategory.COLLECTION) + 1,
        name='archive',
        label='Archive',
        icon='fas fa-archive'
    )
    assert d2.has_icon() is True
    object_manager.insert_category(d2.to_database())
    d3 = CmdbTypeCategory(
        public_id=object_manager.dbm.get_highest_id(CmdbTypeCategory.COLLECTION) + 1,
        name='infrastructure',
        label='Infrastructure',
        icon='fas fa-layer-group'
    )
    inf_id = object_manager.insert_category(d3.to_database())
    d4 = CmdbTypeCategory(
        public_id=object_manager.dbm.get_highest_id(CmdbTypeCategory.COLLECTION) + 1,
        name='locations',
        label='Locations',
        icon='fas fa-map-marked-alt',
        parent_id=inf_id
    )
    object_manager.insert_category(d4.to_database())

    d5 = CmdbTypeCategory(
        public_id=object_manager.dbm.get_highest_id(CmdbTypeCategory.COLLECTION) + 1,
        name='hardware',
        label='Hardware',
        icon='far fa-hdd',
        parent_id=inf_id
    )
    object_manager.insert_category(d5.to_database())

    d6 = CmdbTypeCategory(
        public_id=object_manager.dbm.get_highest_id(CmdbTypeCategory.COLLECTION) + 1,
        name='customers',
        label='Customers',
        icon='far fa-address-card',
    )
    object_manager.insert_category(d6.to_database())
    count_cats = len(object_manager.get_all_categories())
    assert count_cats == 6
    object_manager.dbm.delete_collection(CmdbTypeCategory.COLLECTION)
    # count_cats2 = len(object_manager.get_all_categories())
    # assert count_cats2 == 0


def test_object_status():
    default_stati = CmdbObjectStatus(
        name='default',
        label='Default',
        color='#F0F'
    )

    assert default_stati.get_color() == '#F0F'
    assert default_stati.get_name() == 'default'
    assert default_stati.get_label() == 'Default'


def test_object_manager(object_manager):
    assert object_manager.is_ready() is True
