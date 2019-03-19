from pathlib import Path
from .ranges import Ranges
class Seqnames():
    def __init__(self, values, levels):
        self.values = np.array(values, dtype=np.uint8)
        self.levels = list(set(values))
    
class Track(Ranges):
    def __init__(self, path, name=None, data=None
                 , comment_char=["#"], sep=["\t", " "]
                 , header=None, comment=None, track_line=None):
        self._path = Path(path)
        self._name = name
        self._header = header
        self._comment_char = comment_char
        self._sep = sep
        if data is not None:
            self.start = data.start
            self.end = data.end
            self.seqname = np.
        self._data = list() if data is None  else data

    @classmethod
    def from_range(cls,range, *args, **kwargs):
        self = cls.__new__(cls, *args, **kwargs)
        self.start = range._start
        self.end  = range._end
        
        self = cls(*args, **kwargs, data=range)
        return self

    def get_name(self):
        return self._name
    
    def get_path(self):
        return self._name

    def read(path):
        pass

class BedTrack(Track):
    pass

class DelimTrack(Track):
    pass

def register_track(name, suffix, constructor):
    pass


register_track("BED", ["bed"], BedTrack)
register_track("DELIM", ["tab", "delim"], DelimTrack)
                         
