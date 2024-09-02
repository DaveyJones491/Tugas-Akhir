from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


'''
List Command : 
- Soal / Baca Soal (TTS)
- Jawaban / Baca Jawaban (TTS)
- Selanjutnya / Maju / Soal Selanjutnya (NAV), baca soal saat pindah
- Sebelumnya / Mundur / Soal Selanjutnya (NAV), baca soal saat pindah
- Nomor Soal (NAV), baca soal saat pindah
- Simpan (NAV), Jawaban berhasi disimpan (TTS)
- Selesai (NAV), Konfirmasi (TTS), Ujian berhasil disubmit (TTS)

Extra :

Hold :

Short Term :

To do :
- Baca Soal dan Jawaban saat pindah
- Perintah tidak dikenal, silahkan coba lagi
- Ujian telah selesai
- Menjawab A,B,C,D

Extra : 
- Cek baru bisa masuk exam ketika sudah waktunya
- Deteksi ubah tab / window
- Mark Answer
- Halaman Melihat seluruh soal yang ada dalam exam (admin)
- Buat gak bisa delete account sendiri, account admin terakhir
- Fitur search
- Otomatis submit kalau waktu habis (?)
- Acak Soal
- Timer
- Fancy pagination (Boxed layout, mark answered, mark flagged)
- Delete question ketika examnya di delete

Done :
- Sign Up hanya bisa diakses admin (DONE)
- Halaman account list (DONE)
- Halaman Assign Class (Abandoned)
- Halaman Assign Exam (Abandoned)
- Jenis User (DONE) 
- Halaman Bikin soal (admin)
- Question List (DONE)
- Edit Question (DONE)
- Pagination List (DONE)
- Fix value input field gak bisa diupdate (Edit pake text area, jangan input. Yang harus pake input jangan prefilled) (DONE)
- Fix edit account deteksi email sendiri (Email jadi gak bisa diedit) (DONE)
- Benerin Edit (Liat contoh di edit_account) (DONE)
- Pagination (pake URL buat pagination kayak edit dsb)
- Cek apakah user adalah admin saat mengakses
- Delete button rusak karena ganti url pas pagination
- Setiap user mulai exam, cek apakah udah pernah ngerjain, kalau belum maka isi tabel UserAnswer
- Masukin kolom answer UserAnswer ke db_question (cancelled)
- Selalu kedetect ada UserAnswer
- questionID dapet darimana
- Auto select jawaban yang ada di database (inner join?)
- Saat mulai exam, isi UserAnswer sesuai user (jadinya isi saat submit answer). cancel, bikin langsung semua ajah
- Fetch data di UserAnswer sesuai userid, examid, questionid, lalu edit datanya
- Next/Previous/Number soal button jadi submit dan end exam jadi redirect?
- Simpan jawaban jadi submit dan end exam jadi redirect?
- End Exam
- Final Score
- Cek hanya bisa mengerjakan exam sekali
- List hasil ujian (masukin di ujian?)
- Result list for admin and user

Notes :
flask
flask_sqlalchemy 
flask_login
'''