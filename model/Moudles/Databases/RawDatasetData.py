import uuid

from Moudles.Storage.StorageFactory import StorageFactory


class RawDatasetData:
    _id = 0
    _name = 0
    _jsonData = 0
    _data = 0

    def __init__(
            self,
            name,
            dataFrame=None
    ):
        if dataFrame is not None:
            self._name = name
            self._id = str(uuid.uuid1())
            self._data = dataFrame.values.tolist()
            self._jsonData = {
                "name": self._name,
                "id": self._id,
                "data": self._data
            }
            self.SaveDataset()
        else:
            self._name = name
            self._jsonData = self.LoadDataset()
            self._id = self._jsonData['id']
            self._data = self._jsonData['data']

    @property
    def Id(self):
        return self._id

    @property
    def Name(self):
        return self._name

    @property
    def Data(self):
        return self._data

    @property
    def JsonData(self):
        return self._jsonData

    def SaveDataset(self):
        operationFactory = StorageFactory()
        saver = operationFactory.CreateOperationItem()
        saver.Save(self._name, self._jsonData, "RAW_DATASET")

    def LoadDataset(self):
        operationFactory = StorageFactory()
        loader = operationFactory.CreateOperationItem()
        jsonData = loader.Load(self._name, "RAW_DATASET")
        return jsonData

    @property
    def name(self):
        return self._name

    @property
    def jsonData(self):
        return self._jsonData

    def __str__(self):
        return f"The Raw dataset name is {self._name}"
