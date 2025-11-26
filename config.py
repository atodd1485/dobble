class Config:

    CONFIG_FILENAME = 'dobble.conf'

    def __init__(self):

        with open(self.CONFIG_FILENAME) as file:
            for line in file.readlines():

                key,val = line.split('=')
                key = key.strip()
                val = val.strip()
                print(key,val)
                if val in ('True','False'):
                    setattr(self, key, val == 'True')
                    continue
                try:
                    setattr(self,key,int(val))
                    continue
                except ValueError:
                    pass
                try:
                    setattr(self,key,float(val))
                    continue
                except ValueError:
                    pass