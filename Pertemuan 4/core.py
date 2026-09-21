import hashlib
import time

class Block:
    def __init__(self, index, data, prev_hash="0"):
        self.index = index
        self.timestamp = time.time()
        self.timestamp_readable = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp))
        self.data = data
        self.prev_hash = str(prev_hash)
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # PASTIKAN PARAMETER YANG DI-HASH SELALU SAMA
        value = f"{self.index}{self.timestamp}{self.data}{self.prev_hash}"
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(1, "Genesis Block (Awal Mula)", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        prev_block = self.get_latest_block()
        new_block = Block(len(self.chain) + 1, data, prev_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i-1]

            # 1. Cek apakah hash blok saat ini sesuai dengan isi datanya
            if current_block.hash != current_block.calculate_hash():
                return False

            # 2. Cek apakah prev_hash menunjuk ke hash blok sebelumnya
            if current_block.prev_hash != prev_block.hash:
                return False

        # Cek Genesis Block
        if self.chain[0].hash != self.chain[0].calculate_hash():
            return False

        return True