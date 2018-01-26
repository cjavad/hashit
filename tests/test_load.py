class load_api_1:
    name="hash1"
    def __init__(self, data=b''):
        self.data = data

    def update(self, data=b''):
        self.data += data

    def digest(self):
        return 1516152524156352132515252551426

    def hexdigest(self):
        return hex(self.digest())

class load_api_2:
    name="hash2"
    def __init__(self, data=b''):
        self.data = data

    def update(self, data=b''):
        self.data += data

    def digest(self):
        return 1234567876543234567897654324562

    def hexdigest(self):
        return hex(self.digest())

class load_api_3:
    name="hash3"
    def __init__(self, data=b''):
        self.data = data

    def update(self, data=b''):
        self.data += data

    def digest(self):
        return 5232348239489234823948203294829 

    def hexdigest(self):
        return hex(self.digest())
