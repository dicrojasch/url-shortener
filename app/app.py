from datetime import datetime

from flask import Flask, redirect, request, abort, jsonify
from app.services.models import URLShortener
from app.services.zookeeper import ZookeeperURL
from app import init_app, Producer
import validators
from app.utils.utils import get_current_link
from app.utils import constants

app = init_app()


@app.route("/<short_link>", methods=['GET'])
def get_large_link(short_link):
    response = {}
    try:
        stored_link = URLShortener.get(short_link)
        app.logger.info(" obtained  long-link: '" + stored_link.long_link + "' from short-link: '" + short_link + "'")
        send_kafka_event(datetime.now().timestamp(), constants.EVENT_GET, short_link,
                         stored_link.long_link, constants.CLIENT_FREE)

        return redirect(stored_link.long_link, code=302)

    except Exception as e:
        msg = "An exception occurred: " + str(e)
        send_kafka_event(datetime.now().timestamp(), constants.EVENT_ERROR + "_" + constants.EVENT_GET, short_link, msg, constants.CLIENT_FREE)
        response = {'error': msg}

    return jsonify(response)


@app.route("/api/v1/create", methods=['POST'])
def get_short_link():
    long_link = request.form['link']
    if not validators.url(long_link):
        abort(500, 'URL invalid.')

    response = {}
    try:
        zk_url = ZookeeperURL(app.config["ZK_HOST"], app.config["ZK_PORT"])
        zk_url.zk.start()
        number_link_obtained = zk_url.get_new_link_number(app.config["APPLICATION_ID_ZK"],
                                                          app.config["FINAL_NUMBER_RANGE"])
        zk_url.zk.stop()

        short_link = get_current_link(number_link_obtained, 62)

        app.logger.info(" number obtained from Zookeeper: '" + str(number_link_obtained) +
                        "' and short-link obtained: ''" + short_link + "'")

        long_link_stored = URLShortener(index_link=short_link, long_link=long_link, creation_date=datetime.now())
        long_link_stored.save()
        app.logger.info(" short-link: ''" + short_link + "' saved in database.")

        send_kafka_event(datetime.now().timestamp(), constants.EVENT_SAVE, short_link,
                         long_link, constants.CLIENT_FREE)

        root_url = request.url_root
        if app.config[constants.DEPLOY_TYPE] == constants.PRODUCTION:
            root_url = app.config["URL_PUBLIC"]

        response = {'short-link': root_url + short_link, 'long-link': long_link}

    except Exception as e:
        msg = "An exception occurred: " + str(e)
        send_kafka_event(datetime.now().timestamp(), constants.EVENT_ERROR + "_" + constants.EVENT_SAVE, msg, long_link, constants.CLIENT_FREE)
        response = {'error': msg}

    return jsonify(response)


@app.route("/api/v1/delete/<short_link>", methods=['DELETE'])
def delete_link(short_link):
    response = {}
    try:
        stored_link = URLShortener.get(short_link)
        app.logger.info(" short-link: '" + short_link + "' to delete, long-link: '" + stored_link.long_link + "'")
        stored_link.delete()
        send_kafka_event(datetime.now().timestamp(), constants.EVENT_DEL, short_link, "-", constants.CLIENT_FREE)

        response = {'message': 'success'}
    except Exception as e:
        msg = "An exception occurred: " + str(e)
        send_kafka_event(datetime.now().timestamp(), constants.EVENT_ERROR + "_" + constants.EVENT_DEL, short_link, msg, constants.CLIENT_FREE)
        response = {'error': msg}

    return jsonify(response)


@app.route("/api/v1/test")
def test():
    return jsonify({'message': 'enpoint for testing'})


def send_kafka_event(date_event, type_event, short_link, long_link, type_client):
    kafka_producer = Producer(app.config["KAFKA_TOPIC"], app.config["KAFKA_HOST"], app.config["KAFKA_PORT"])
    kafka_producer.send_event(date_event, type_event, short_link, long_link, type_client)
    msg = " event sent to Kafka: date_event : '" + str(datetime.fromtimestamp(date_event)) + "'; type_event: '" + \
          type_event + "'; short_link : '" + short_link + "'; long_link : '" + long_link + \
          "'; type_client: '" + type_client + "'"
    if constants.EVENT_ERROR in type_event:
        app.logger.error(msg)
    else:
        app.logger.info(msg)




