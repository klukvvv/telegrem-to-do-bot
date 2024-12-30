class TaskIterator:
    def __init__(self, tasks):
        self.tasks = tasks
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.tasks):
            task = self.tasks[self.index]
            self.index += 1
            return task
        else:
            raise StopIteration
