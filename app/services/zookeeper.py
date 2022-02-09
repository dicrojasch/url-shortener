import time

from kazoo.client import KazooState
from kazoo.client import KazooClient
from kazoo.exceptions import BadVersionError
from kazoo.protocol.states import KeeperState

from app.utils import constants
from app.utils.utils import int_to_bytes, bytes_to_int


class ZookeeperURL:

    def __init__(self, host, port):
        self.zk = KazooClient(hosts=host + ":" + port)
        self.main_node_zk = "/" + constants.ZK_ROOT_NODE + "/"

    def get_range(self):
        if self.zk.state != KeeperState.CONNECTED:
            self.zk.start()

        if not self.zk.exists(self.main_node_zk):
            self.zk.create(self.main_node_zk,  int_to_bytes(0))

        first_number_range, last_number_range = self._apart_range(self.main_node_zk, constants.RANGE_CAPACITY)
        application_node_zk = self.main_node_zk + str(first_number_range)
        self.zk.create(application_node_zk, int_to_bytes(first_number_range))
        return first_number_range

    def get_new_link_number(self, application_node_zk, last_number_link):
        if application_node_zk >= last_number_link:
            raise RuntimeError('Reached range number links assigned')
        counter = self.zk.Counter(self.main_node_zk + str(application_node_zk))
        counter += 1
        return counter.value

    def _apart_range(self, path, increment):
        if self.zk.state != KeeperState.CONNECTED:
            self.zk.start()
        counter = self.zk.Counter(path)
        exceeded_start = (counter.value % increment)

        start_value = counter.value
        counter += (increment - exceeded_start)
        final_value = (start_value - exceeded_start) + increment
        return start_value, final_value
