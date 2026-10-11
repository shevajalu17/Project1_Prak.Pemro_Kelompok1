from datetime import date, timedelta
from .entities import Transaksi, ItemPinjam, StatusTransaksi, KondisiAlat


class TransaksiManager:
    def __init__(self, mahasiswaMgr, alatMgr):
        self.data: dict[str, Transaksi] = {}
        self.mhsMgr = mahasiswaMgr
        self.alatMgr = alatMgr
        self.counter = 1

    def buatTransaksi(self, nim: str, listKodeAlat: list[str], lamaHari: int = 7):
        mahasiswa = self.mhsMgr.getByNim(nim)
        if mahasiswa is None:
            return None, "Mahasiswa tidak ditemukan."
        if not mahasiswa.bisaMeminjam():
            return None, "Mahasiswa sudah memiliki maksimal 2 transaksi aktif."
        if not listKodeAlat:
            return None, "Pilih minimal satu alat."
        if len(set(listKodeAlat)) != len(listKodeAlat):
            return None, "Kode alat tidak boleh duplikat dalam satu transaksi."
        if not isinstance(lamaHari, int) or not 1 <= lamaHari <= 7:
            return None, "Lama peminjaman harus antara 1 sampai 7 hari."

        alat_dipilih = []
        for kode in listKodeAlat:
            alat = self.alatMgr.data.get(kode)
            if alat is None:
                return None, f"Alat {kode} tidak ditemukan."
            if not alat.isTersedia():
                return None, f"Alat {kode} tidak tersedia untuk dipinjam."
            alat_dipilih.append(alat)

        hari_ini = date.today()
        id_trx = f"TRX{self.counter:03d}"
        transaksi = Transaksi(
            idTransaksi=id_trx, mahasiswa=mahasiswa,
            daftarItem=[ItemPinjam(a) for a in alat_dipilih],
            tanggalPinjam=hari_ini, batasKembali=hari_ini + timedelta(days=lamaHari)
        )
        self.data[id_trx] = transaksi
        self.counter += 1
        mahasiswa.tambahTransaksiAktif(id_trx)
        for alat in alat_dipilih:
            alat.tandaiDipinjam()
        return transaksi, "Transaksi berhasil dibuat."

    def prosesPengembalian(self, idTrx: str, kodeAlat: str, kondisi: KondisiAlat):
        transaksi = self.data.get(idTrx)
        if transaksi is None or not transaksi.isAktif():
            return False, "Transaksi aktif tidak ditemukan."
        if not isinstance(kondisi, KondisiAlat):
            return False, "Kondisi alat tidak valid."
        for item in transaksi.daftarItem:
            if item.alat.kodeAlat == kodeAlat and not item.sudahKembali():
                item.kembalikan(kondisi, date.today())
                transaksi.perbaruiStatus()
                return True, "Pengembalian alat berhasil dicatat."
        return False, "Alat tidak ditemukan pada transaksi atau sudah dikembalikan."

    def tampilSemua(self) -> list[Transaksi]:
        return list(self.data.values())

    def cariByMahasiswa(self, nim: str) -> list[Transaksi]:
        return [t for t in self.data.values() if t.mahasiswa.nim == nim]

    def riwayatMahasiswa(self, nim: str) -> list[Transaksi]:
        return self.cariByMahasiswa(nim)

    def adaAlatDalamTransaksiAktif(self, kodeAlat: str) -> bool:
        return any(t.isAktif() and any(i.alat.kodeAlat == kodeAlat for i in t.daftarItem)
                   for t in self.data.values())

    def statistik(self) -> dict:
        hitung_alat, hitung_mhs = {}, {}
        for trx in self.data.values():
            nim = trx.mahasiswa.nim
            hitung_mhs[nim] = hitung_mhs.get(nim, 0) + 1
            for item in trx.daftarItem:
                kode = item.alat.kodeAlat
                hitung_alat[kode] = hitung_alat.get(kode, 0) + 1
        return {
            "alat": hitung_alat,
            "mahasiswa": hitung_mhs,
            "selesai": sum(t.status == StatusTransaksi.SELESAI for t in self.data.values()),
            "aktif": sum(t.isAktif() for t in self.data.values()),
        }
