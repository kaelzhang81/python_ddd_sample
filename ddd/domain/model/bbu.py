import Singleton
import Enodeb
import Factory
import CcBoard
import Bpl
import FsBoard
import BBU


@Singleton
class BBUFactory(object):

    @staticmethod
    def create(self, alias, cc, bpl_list, fs_list):
        bbu = BBU(alias)
        bbu.add_device([CcBoard(cc)])
        bbu.add_device([Bpl(x) for x in bpl_list])
        bbu.add_device(FsBoard(x) for x in fs_list)
        return bbu


Factory.register(BBUFactory)

