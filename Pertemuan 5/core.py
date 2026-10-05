import hashlib
import time

class Block:
    def __init__(self, index, data, prev_hash="0"):
        self.index = index
        self.timestamp = time.time()
        self.timestamp_readable = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp))
        self.data = data
        self.prev_hash = str(prev_hash)
        self.nonce = 0  # 1. Menambahkan nonce (angka acak/increment untuk mining)
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # 2. Pastikan nonce ikut dimasukkan ke dalam string yang akan di-hash
        value = f"{self.index}{self.timestamp}{self.data}{self.prev_hash}{self.nonce}"
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    # 3. Menambahkan fungsi mine_block (Proof of Work)
    def mine_block(self, difficulty):
        target = '0' * difficulty # Target hash harus diawali dengan 0 sebanyak nilai difficulty
        
        # Selama hash belum diawali dengan target '0'x, iterasi nonce dan hitung ulang hash
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
            
        print(f"Blok {self.index} berhasil ditambang: {self.hash} (Nonce: {self.nonce})")

class Blockchain:
    def __init__(self, difficulty=2):
        self.difficulty = difficulty  # Menambahkan tingkat kesulitan (jumlah 0 di awal hash)
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        genesis = Block(1, "Genesis Block (Awal Mula)", "0")
        genesis.mine_block(self.difficulty) # Genesis block juga bisa ditambang
        return genesis

    def get_latest_block(self):
        return self.chain[-1]

    # 4. Memperbarui fungsi add_block
    def add_block(self, data):
        prev_block = self.get_latest_block()
        new_block = Block(len(self.chain) + 1, data, prev_block.hash)
        
        # Jalankan proses mining sebelum blok ditambahkan ke rantai
        new_block.mine_block(self.difficulty)
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