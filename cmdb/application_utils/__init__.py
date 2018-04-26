from cmdb.application_utils.system_reader import SystemConfigReader, SystemSettingsReader
from cmdb.data_storage.database_connection import MongoConnector
from cmdb.data_storage.database_manager import DatabaseManagerMongo
SYSTEM_CONFIG_READER = SystemConfigReader(
    config_name=SystemConfigReader.DEFAULT_CONFIG_NAME,
    config_location=SystemConfigReader.DEFAULT_CONFIG_LOCATION
)

SYSTEM_SETTINGS_READER = SystemSettingsReader(
    database_manager=DatabaseManagerMongo(
        connector=MongoConnector(
            host=SYSTEM_CONFIG_READER.get_value('host', 'Database'),
            port=int(SYSTEM_CONFIG_READER.get_value('port', 'Database')),
            database_name=SYSTEM_CONFIG_READER.get_value('database_name', 'Database'),
            timeout=MongoConnector.DEFAULT_CONNECTION_TIMEOUT
        )
    )

)
