from datetime import datetime

from flask import Flask, redirect, request, abort, jsonify
from app.services.models import URLShortener
from app.services.zookeeper import ZookeeperURL
from app import create_app
import validators
from app.utils.utils import get_current_link


app = create_app()


@app.route("/<short_link>", methods=['GET'])
def get_large_link(short_link):
    stored_link = URLShortener.get(short_link)
    return redirect(stored_link.long_link, code=302)


@app.route("/api/v1/create", methods=['POST'])
def get_short_link():
    link = request.form['link']
    if not validators.url(link):
        abort(500, 'URL invalid.')

    zk_url = ZookeeperURL(app.config["ZK_HOST"], app.config["ZK_PORT"])
    zk_url.zk.start()
    number_link_obtained = zk_url.get_new_link_number(app.config["APPLICATION_ID_ZK"], app.config["FINAL_NUMBER_RANGE"])
    zk_url.zk.stop()

    short_link = get_current_link(number_link_obtained, 62)

    link = URLShortener(index_link=short_link, long_link=link, creation_date=datetime.now())
    link.save()
    response = {'short-link': request.url_root + short_link}
    return jsonify(response)


@app.route("/api/v1/delete/<short_link>", methods=['DELETE'])
def delete_link(short_link):
    stored_link = URLShortener.get(short_link)
    stored_link.delete()
    response = {'message': 'success'}
    return jsonify(response)


@app.route("/test")
def test():
    return jsonify({'message': 'enpoint for testing'})

