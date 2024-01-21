import os


class OSSStorage:
    def __init__(self):
        self.data_path = "/data/"

    def list(self, path=""):
        full_path = os.path.join(self.data_path, path)
        return [
            f
            for f in os.listdir(full_path)
            if os.path.isfile(os.path.join(full_path, f))
        ]

    def put(self, content, path):
        full_path = os.path.join(self.data_path, path)
        with open(full_path, "wb") as file:
            file.write(content)

    def delete(self, path):
        full_path = os.path.join(self.data_path, path)
        if os.path.exists(full_path):
            os.remove(full_path)

    def get(self, path):
        full_path = os.path.join(self.data_path, path)
        with open(full_path, "rb") as file:
            return file.read()


# Example usage:
# storage = OSSStorage()
# storage.put(b'Hello, OSS!', 'example.txt')
# print(storage.get('example.txt'))
# storage.delete('example.txt')
