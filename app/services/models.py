from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute

from app.settings.settings import get_config_dict_env


class URLShortener(Model):
    class Meta:
        config = get_config_dict_env()
        table_name = config["DYNDB_TABLE_LINK"]
        host = "http://" + config["DYNDB_HOST"] + ":" + config["DYNDB_PORT"]
        aws_access_key_id = config["DYNDB_KEY"]
        aws_secret_access_key = config["DYNDB_SECRET"]
        region = config["REGION"]
    index_link = UnicodeAttribute(hash_key=True)
    long_link = UnicodeAttribute()
    creation_date = UTCDateTimeAttribute()

    def __repr__(self):
        return "<Short-link {}, Long-link:{}, creation-date:{}>".format(self.index_link, self.long_link, self.creation_date)


class LogInternal(Model):
    class Meta:
        config = get_config_dict_env()
        table_name = config["DYNDB_TABLE_LOG"]
        host = "http://" + config["DYNDB_HOST"] + ":" + config["DYNDB_PORT"]
        aws_access_key_id = config["DYNDB_KEY"]
        aws_secret_access_key = config["DYNDB_SECRET"]
        region = config["REGION"]

    date_event = UTCDateTimeAttribute(hash_key=True)
    type_event = UnicodeAttribute()
    index_link = UnicodeAttribute()
    long_link = UnicodeAttribute()
    type_client = UnicodeAttribute()
