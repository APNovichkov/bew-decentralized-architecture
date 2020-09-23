total: int128

event AddToTotalEvent: pass

@external
def addToTotal(_number: int128):
    self.total += _number
    log AddToTotalEvent()