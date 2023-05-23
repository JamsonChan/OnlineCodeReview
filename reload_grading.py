import autograding, importlib, os
from func_timeout import func_set_timeout
@func_set_timeout(3)
def reload_homework_autograding(studentid, filename, hwnum):
    autograding.receive(studentid, filename, hwnum)
    os.chdir(autograding.first)
    importlib.reload(autograding)
    Score = autograding.Score
    Time = autograding.Time
    Memory = autograding.Memory
    Sheet = autograding.sheet
    return Score, Time, Memory, Sheet