import paramiko
from logger import Logger

class SFTPClient:

    def __init__(self, host, port, username, password):

        self.host = host
        self.port = port
        self.username = username
        self.password = password

        self.transport = None
        self.client = None
        self.logger = Logger()

    def connect(self):

        self.logger.info("Conectando al servidor SFTP...")

        self.transport = paramiko.Transport(
            (self.host, self.port)
        )

        self.transport.connect(
            username=self.username,
            password=self.password
        )

        self.client = paramiko.SFTPClient.from_transport(
            self.transport
        )

        self.logger.info("Conexión establecida.")

    def disconnect(self):

        if self.client:
            self.client.close()

        if self.transport:
            self.transport.close()

        self.logger.info("Conexión cerrada.")

    def list_files(self, remote_path):
        return self.client.listdir(remote_path)
    
    def download_file(self, remote_file, local_file):
        self.client.get(remote_file, local_file)
        self.logger.info(f"Archivo {remote_file} descargado.")

    def delete_file(self, remote_file):
        self.client.remove(remote_file)
        self.logger.info(f"Archivo remoto eliminado: {remote_file}.")