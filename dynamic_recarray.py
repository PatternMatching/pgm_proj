import numpy as np

class DynamicRecArray(object):
    def __init__(self, dtype):
        self.dtype = np.dtype(dtype)
        self.length = 0
        self.size = 10
        self._data = np.empty(self.size, dtype=self.dtype)

    def __len__(self):
        return self.length

    def append(self, rec):
        if self.length == self.size:
            self.size = int(1.5*self.size)
            self._data = np.resize(self._data, self.size)
        self._data[self.length] = rec
        self.length += 1

    def extend(self, recs):
        for rec in recs:
            self.append(rec)

    def sort(self, field, desc=False):
        self._data.sort(order=field)
        if desc:
            self._data = self._data[::-1]

    @property
    def data(self):
        return self._data[:self.length]


if __name__ == "__main__":

    dt = [('name', 'a25'), ('prob', 'f4')]
    ra = DynamicRecArray(dt)

    ra.append(("Michael Jordan", 0.25))
    ra.append(("Ray Rice", 0.5))
    ra.append(("Adrian Peterson", 0.9))

    print ra.data

    ra.sort('prob', desc=True)

    print ra.data
