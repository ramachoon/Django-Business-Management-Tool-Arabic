import random
import os


def upload_path(path):
    def wrapper(instance, filename):
        extension = "." + filename.split('.')[-1]
        filename = str(random.randint(10, 99)) + str(random.randint(10, 99)) + str(random.randint(10, 99)) + str(
            random.randint(10, 99)) + extension
        return os.path.join(path, filename)

    return wrapper
