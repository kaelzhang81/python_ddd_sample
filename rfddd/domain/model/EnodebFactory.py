class EnodebFactory(Singleton):
    enodebList = []

    def create(self, name):
        print self
        enodeb = Enodeb(name)
        EnodebFactory.enodebList.append(enodeb)
        return enodeb
    
    def get(self, name):
        print self
        return filter(lambda enodeb: name == enodeb.get_name(), EnodebFactory.enodebList)[0]
        
