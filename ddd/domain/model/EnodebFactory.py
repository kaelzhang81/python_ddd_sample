import Singleton
import Enodeb
import Factory
import CcBoard
import Bpl
import FsBoard
import RRU


@Singleton
class EnodebFactory(object):

    @staticmethod
    def create(self, alias, cc, rru_list, bpl_list, fs_list):
        enodeb = Enodeb(alias)
        enodeb.add_device([CcBoard(cc)])
        enodeb.add_device(RRU(x) for x in rru_list)
        enodeb.add_device([Bpl(x) for x in bpl_list])
        enodeb.add_device(FsBoard(x) for x in fs_list)
        return enodeb


Factory.register(EnodebFactory)

