# TST-MicroserviceDeployment
Aditya Inas Hamidah (18221172)

## Core Service
Menampilkan media (foto/video) yang diupload oleh penyedia layanan performance

## Teknologi yang digunakan
- fastapi 0.104.1
- pydantic 2.4.2
- uvicorn 0.24.0
- python-multipart 0.0.6

## Fitur
- CRUD Media
- Upload Media
- Edit Caption

## How to Use
1. Gunakan link performaremedia.azurewebsites.net/docs#
2. Coba fungsi-fungsi yang tersedia dengan try it out
3. Ikuti langkah-langkahnya sehingga dapat berhasil

## API Endpoint
- GET '/' -> menampilkan semua data
- GET '/{option_FileName}' -> menampilkan data sesuai nama
- POST '/acceptdata' -> input data media
- POST '/uploadfile' -> upload media
- PUT '/updatedesc' -> mengupdate judul dan caption media
- DELETE '/{FileName}' -> menghapus media berdasarkan nama file
