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
('MALIO-A01', 1, 'Small', 8000, 'Malioboro Mall, Yogyakarta', 'READY', -7.7927290, 110.3666990),
('MALIO-A02', 1, 'Medium', 12000, 'Malioboro Mall, Yogyakarta', 'READY', -7.7925290, 110.3668990),
('MALIO-A03', 1, 'Large', 18000, 'Malioboro Mall, Yogyakarta', 'READY', -7.7929290, 110.3664990),
('AMPLAZ-B01', 2, 'Small', 9000, 'Ambarrukmo Plaza, Yogyakarta', 'READY', -7.7828250, 110.4018170),
('AMPLAZ-B02', 2, 'Medium', 14000, 'Ambarrukmo Plaza, Yogyakarta', 'READY', -7.7830250, 110.4020170),
('JCM-C01', 3, 'Small', 8500, 'Jogja City Mall, Yogyakarta', 'READY', -7.7513390, 110.3616480),
('JCM-C02', 3, 'Large', 20000, 'Jogja City Mall, Yogyakarta', 'READY', -7.7515390, 110.3618480),
('GALERIA-D01', 4, 'Medium', 13000, 'Galeria Mall, Yogyakarta', 'READY', -7.7838780, 110.3792000),
('PAKUWON-E01', 5, 'Small', 10000, 'Pakuwon Mall Jogja, Yogyakarta', 'READY', -7.7587380, 110.3999840),
('MALIO-M01', 1, 'Small', 7000, 'Malioboro Mall, Yogyakarta', 'MAINTENANCE', -7.7931290, 110.3662990)
ON CONFLICT (id_loker) DO UPDATE SET
    id_usaha = EXCLUDED.id_usaha,
    tipe_loker = EXCLUDED.tipe_loker,
    harga_per_jam = EXCLUDED.harga_per_jam,
    lokasi = EXCLUDED.lokasi,
    status = EXCLUDED.status,
    latitude = EXCLUDED.latitude,
    longitude = EXCLUDED.longitude;
