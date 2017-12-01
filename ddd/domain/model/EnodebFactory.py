import Singleton
import Enodeb
import Factory


@Singleton
class EnodebFactory(object):

    @staticmethod
    def create(self, name, rrus, base_band_boards, fs_boards):
        enodeb = Enodeb(name)
        enodeb.add_device(rrus)
        enodeb.add_device(base_band_boards)
        enodeb.add_device(fs_boards)
        return enodeb


Factory.register(EnodebFactory)

