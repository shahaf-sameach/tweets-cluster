import time

from settings import TwitterSettings


class TwitterUsersIterator:

    def __init__(self, users, delay=0):
        self.users = users
        self.indx = 0
        self.delay = delay

    def __iter__(self):
        return self

    def next(self):
        if self.indx == len(self.users):
            self.indx = 0
            time.sleep(self.delay)

        user = self.users[self.indx]
        self.indx += 1

        return user




if __name__ == "__main__":
    a = TwitterSettings.all_users
    for i in TwitterUsersIterator(a, delay=5):
        print(i.access_key)