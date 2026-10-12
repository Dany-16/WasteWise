from flask import Flask, render_template, request, redirect, url_for
from datetime import date

app = Flask(__name__)

# Memori penyimpanan sementara
data_sampah = []

@app.route("/")
def index():
    total_berat = sum(item["berat"] for item in data_sampah)
    jumlah_catatan = len(data_sampah)
    tanggal_hari_ini = date.today().isoformat()
    
    return render_template(
        "index.html", 
        daftar_sampah=data_sampah, 
        total_berat=total_berat, 
        jumlah_catatan=jumlah_catatan,
        tanggal_hari_ini=tanggal_hari_ini
    )

@app.route("/tambah", methods=["POST"])
def tambah_sampah():
    nama = request.form.get("namaSampah", "").strip()
    kategori = request.form.get("kategori")
    berat_str = request.form.get("berat")
    tanggal = request.form.get("tanggal")
    
    try:
        berat = float(berat_str)
        if nama and kategori and tanggal and berat > 0:
            sampah_baru = {
                "id": len(data_sampah) + 1,
                "nama": nama,
                "kategori": kategori,
                "berat": berat,
                "tanggal": tanggal
            }
            data_sampah.append(sampah_baru)
    except (ValueError, TypeError):
        pass
        
    return redirect(url_for("index"))

@app.route("/hapus/<int:sampah_id>", methods=["POST"])
def hapus_sampah(sampah_id):
    global data_sampah
    data_sampah = [s for s in data_sampah if s["id"] != sampah_id]
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)