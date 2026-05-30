ALTER TABLE loker
ADD COLUMN IF NOT EXISTS latitude NUMERIC(10,7),
ADD COLUMN IF NOT EXISTS longitude NUMERIC(10,7);

INSERT INTO loker (
    id_loker,
    id_usaha,
    tipe_loker,
    harga_per_jam,
    lokasi,
    status,
    latitude,
    longitude
)
VALUES
('KC-A01', 1, 'Small', 10000, 'Kuningan City Mall, Jakarta Selatan', 'READY', -6.2231653, 106.8277260),
('KC-A02', 1, 'Medium', 15000, 'Kuningan City Mall, Jakarta Selatan', 'READY', -6.2233653, 106.8279260),
('KC-A03', 1, 'Large', 20000, 'Kuningan City Mall, Jakarta Selatan', 'READY', -6.2229653, 106.8275260),
('AMB-B01', 2, 'Small', 12000, 'Mall Ambasador, Jakarta Selatan', 'READY', -6.2242340, 106.8267220),
('AMB-B02', 2, 'Medium', 16000, 'Mall Ambasador, Jakarta Selatan', 'READY', -6.2244340, 106.8269220),
('KOKAS-C01', 3, 'Small', 11000, 'Kota Kasablanka, Jakarta Selatan', 'READY', -6.2246400, 106.8420700),
('KOKAS-C02', 3, 'Large', 22000, 'Kota Kasablanka, Jakarta Selatan', 'READY', -6.2248400, 106.8422700),
('SET-D01', 4, 'Medium', 17000, 'Setiabudi One, Jakarta Selatan', 'READY', -6.2168600, 106.8304600),
('LOTTE-E01', 5, 'Small', 13000, 'Lotte Shopping Avenue, Jakarta Selatan', 'READY', -6.2241000, 106.8229000),
('KC-M01', 1, 'Small', 9000, 'Kuningan City Mall, Jakarta Selatan', 'MAINTENANCE', -6.2235653, 106.8281260)
ON CONFLICT (id_loker) DO UPDATE SET
    id_usaha = EXCLUDED.id_usaha,
    tipe_loker = EXCLUDED.tipe_loker,
    harga_per_jam = EXCLUDED.harga_per_jam,
    lokasi = EXCLUDED.lokasi,
    status = EXCLUDED.status,
    latitude = EXCLUDED.latitude,
    longitude = EXCLUDED.longitude;
