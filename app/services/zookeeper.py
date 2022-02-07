import time

from kazoo.client import KazooState
from kazoo.client import KazooClient
from kazoo.exceptions import BadVersionError
from app.utils import constants
from app.utils.utils import int_to_bytes, bytes_to_int


class ZookeeperURL:

    def __init__(self, host, port):
        self.zk = KazooClient(hosts=host + ":" + port)
        self.main_node_zk = "/" + constants.ZK_ROOT_NODE + "/"

    def get_range(self):
        if self.zk.state != "CONNECTED":
            self.zk.start()

        if not self.zk.exists(self.main_node_zk):
            self.zk.create(self.main_node_zk,  int_to_bytes(0))

        last_number_range = self._apart_value(self.main_node_zk, constants.RANGE_CAPACITY)

        first_number_range = last_number_range - constants.RANGE_CAPACITY

        application_node_zk = self.main_node_zk + str(first_number_range)

        self.zk.create(application_node_zk, int_to_bytes(first_number_range))

        return first_number_range

    def get_new_link_number(self, application_node_zk, last_number_link):
        if application_node_zk >= last_number_link:
            raise RuntimeError('Reached range number links assigned')
        value_assigned = self._apart_value(self.main_node_zk + str(application_node_zk), 1)
        return value_assigned

    def _apart_value(self, path, increment):
        if self.zk.state != "CONNECTED":
            self.zk.start()
        ok_set = False
        value_to_update = -1
        for i in range(constants.MAX_RETRY_WRITE_ZK):
            value, stat = self.zk.get(path)
            value_to_update = bytes_to_int(value) + increment
            try:
                self.zk.set(path, int_to_bytes(value_to_update), stat.version)
                ok_set = True
            except BadVersionError as e:
                print(str(e) + ' - Bad version error, trying to set again...')
                self.zk.restart()

            if ok_set:
                break

        if not ok_set:
            print('Tryings to set Zookeeper exceed Max_tryings="' + str(constants.MAX_RETRY_WRITE_ZK) + '", Path="' +
                  path + '", Value="' + str(value_to_update) + '"')
            value_to_update = -1

        return value_to_update

    def _my_listener(state):
        if state == KazooState.LOST:
            print("session lost")  # Register somewhere that the session was lost
        elif state == KazooState.SUSPENDED:
            print("session suspended")  # Handle being disconnected from Zookeeper
        else:
            print("connected")


# from app.utils import config as config_app, constants
#
# zk1 = ZookeeperURL("127.0.0.1", "2181")
# zk1.zk.start()
# zk1.get_range()
# zk1.zk.stop()





# def my_listener(state):
#     if state == KazooState.LOST:
#         print("session lost")               # Register somewhere that the session was lost
#     elif state == KazooState.SUSPENDED:
#         print("session suspended")          # Handle being disconnected from Zookeeper
#     else:
#         print("connected")
#
# logging.basicConfig()
# zk = KazooClient(hosts="127.0.0.1:2181")
# zk.start()
#
#
# zk.add_listener(my_listener)
# # Determine if a node exists
# if zk.exists("/my/favorite"):
#     print("exists")
# else:
#     print(" not exists")
#     zk.ensure_path("/my/favorite")
#     print("setted")
#
# # Do something
# # Print the version of a node and its data
#
# print("before get")
# data, stat = zk.get("/my/favorite")
# print("after get")
# print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
#
# # List the children
# children = zk.get_children("/my/favorite")
# print("There are %s children with names %s" % (len(children), children))
#
# zk.stop()
#
#
# print(" -------------------------------------------- ")
#
#
# zk.start()
#
#
# zk.add_listener(my_listener)
# # Determine if a node exists
# if zk.exists("/my/favorite"):
#     print("exists")
# else:
#     print(" not exists")
#     zk.ensure_path("/my/favorite")
#     print("setted")
#
# # Do something
# # Print the version of a node and its data
#
# print("before get")
# data, stat = zk.get("/my/favorite")
# print("after get")
# print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
#
# # List the children
# children = zk.get_children("/my/favorite")
# print("There are %s children with names %s" % (len(children), children))
#
# zk.stop()
