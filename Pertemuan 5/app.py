import streamlit as st
from core import Blockchain

st.set_page_config(page_title="Pharma Chain Explorer", page_icon="💊", layout="wide")
st.title("💊 Blockchain Rantai Pasok Obat & Vaksin")

if 'my_blockchain' not in st.session_state:
    st.session_state.my_blockchain = Blockchain()

# --- SIDEBAR: INPUT DATA MENGGUNAKAN FORM ---
st.sidebar.header("➕ Catat Distribusi Obat/Vaksin")

with st.sidebar.form(key="add_block_form", clear_on_submit=True):
    nama_produk = st.text_input("Nama Obat / Vaksin:", placeholder="Contoh: Vaksin Covid-19 / Paracetamol")
    nomor_batch = st.text_input("Nomor Bets (Batch ID):", placeholder="Contoh: BATCH-9982")
    jumlah_dosis = st.number_input("Jumlah Unit/Dosis:", min_value=1, value=100)
    suhu_penyimpanan = st.number_input("Suhu Storage (°C):", value=4.0, format="%.1f")
    lokasi = st.text_input("Fasilitas / Lokasi Saat Ini:", placeholder="Contoh: Gudang Bio Farma Bandung")
    
    submit_button = st.form_submit_button(label="Daftarkan ke Buku Besar")

if submit_button:
    if nama_produk and nomor_batch and lokasi:
        data_transaksi = (
            f"Produk: {nama_produk} | Bets: {nomor_batch} | Jumlah: {jumlah_dosis} Unit | "
            f"Suhu: {suhu_penyimpanan}°C | Lokasi: {lokasi}"
        )
        # Menambahkan peringatan loading karena mining butuh waktu
        with st.spinner("Menambang blok baru... Mohon tunggu!"):
            st.session_state.my_blockchain.add_block(data_transaksi)
        st.sidebar.success("Data distribusi berhasil ditambahkan ke blok!")
        st.rerun() 
    else:
        st.sidebar.error("Mohon lengkapi semua data utama (Produk, Bets, dan Lokasi)!")

# --- SIDEBAR: SIMULASI SERANGAN (HACKING) ---
st.sidebar.markdown("---")
st.sidebar.header("⚠️ Simulasi Serangan (Hacking)")
if st.sidebar.button("💀 HACK BLOK 1 (Manipulasi Data)"):
    # Cek apakah sudah ada blok selain genesis block
    if len(st.session_state.my_blockchain.chain) > 1:
        # Mengubah data secara paksa pada blok indeks 1
        st.session_state.my_blockchain.chain[1].data = "DATA PALSU! (Obat Telah Dipalsukan/Diganti)"
        st.sidebar.success("Berhasil! Blok 1 telah diretas secara paksa.")
    else:
        st.sidebar.warning("Silakan 'Daftarkan ke Buku Besar' minimal 1 data terlebih dahulu sebelum meretas!")


# --- MAIN AREA: VISUALISASI RANTAI ---
st.subheader("📜 Ledger Rantai Pasok Farmasi (Immutable Log)")

# Tombol Validasi Jaringan
if st.button("🛡️ Cek Integritas Rantai"):
    is_valid = st.session_state.my_blockchain.is_chain_valid()
    if is_valid:
        st.success("✔ Status Jaringan: Rantai Valid (Keamanan & Integritas Produk Terjamin)")
    else:
        st.error("❌ PERINGATAN BAHAYA: Rantai Terdeteksi Dimanipulasi! (Potensi Pemalsuan Obat)")
else:
    st.info("Klik tombol 'Cek Integritas Rantai' untuk memverifikasi keaslian data logistik.")

for block in st.session_state.my_blockchain.chain:
    with st.expander(f"📦 Blok Batch #{block.index} | Hash ID: {block.hash[:15]}..."):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Detail Logistik & Produk:**")
            if "DATA PALSU!" in block.data:
                st.error(block.data) # Highlight merah jika isinya data palsu
            else:
                st.info(block.data)
            st.write(f"**Waktu Pencatatan (Timestamp):** {block.timestamp_readable}")
            
        with col2:
            st.write("**Integritas Kriptografi:**")
            
            st.write("**Nonce (Angka Bukti Kerja):**")
            st.code(block.nonce, language="python")
            
            st.write("**Hash Blok Saat Ini:**")
            st.code(block.hash, language="python")
            
            st.write("**Hash Blok Sebelumnya (Pointer):**")
            st.code(block.prev_hash, language="python")