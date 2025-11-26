class Config:

    CONFIG_FILENAME = 'dobble.conf'

    def __init__(self):

        with open(self.CONFIG_FILENAME) as file:
            for line in file.readlines():

                key,val = line.split('=')
                key = key.strip().lower()
                val = val.strip().lower()
                print(key,val)
                if val in ('true','false'):
                    setattr(self, key, val == 'true')
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