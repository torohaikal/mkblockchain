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
        st.session_state.my_blockchain.add_block(data_transaksi)
        st.sidebar.success("Data distribusi berhasil ditambahkan ke blok!")
        st.rerun() # Memuat ulang halaman agar data langsung muncul
    else:
        st.sidebar.error("Mohon lengkapi semua data utama (Produk, Bets, dan Lokasi)!")

# --- MAIN AREA: VISUALISASI RANTAI ---
st.subheader("📜 Ledger Rantai Pasok Farmasi (Immutable Log)")

is_valid = st.session_state.my_blockchain.is_chain_valid()
if is_valid:
    st.success("✔ Status Jaringan: Rantai Valid (Keamanan & Integritas Produk Terjamin)")
else:
    st.error("❌ PERINGATAN BARA: Rantai Terdeteksi Dimanipulasi! (Potensi Pemalsuan Obat)")

for block in st.session_state.my_blockchain.chain:
    with st.expander(f"📦 Blok Batch #{block.index} | Hash ID: {block.hash[:15]}..."):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Detail Logistik & Produk:**")
            st.info(block.data)
            st.write(f"**Waktu Penatatan (Timestamp):** {block.timestamp_readable}")
            
        with col2:
            st.write("**Integritas Kriptografi:**")
            st.write("**Hash Blok Saat Ini:**")
            st.code(block.hash, language="python")
            st.write("**Hash Blok Sebelumnya (Pointer):**")
            st.code(block.prev_hash, language="python")