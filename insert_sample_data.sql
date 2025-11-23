-- Insert sample data for Portfolio and Services

-- Insert sample services
INSERT INTO services (title, description, icon, features, display_order, published) VALUES
('Desain Interior Rumah', 'Desain interior rumah tinggal yang nyaman, fungsional, dan sesuai dengan gaya hidup Anda. Kami menciptakan ruang yang tidak hanya indah tetapi juga praktis untuk kehidupan sehari-hari.', 'home', ARRAY['Konsultasi desain gratis', 'Gambar 3D rendering', 'Pemilihan material berkualitas', 'Pengawasan proyek'], 1, true),
('Desain Interior Kantor', 'Ciptakan ruang kerja yang produktif dan profesional. Desain kantor modern yang meningkatkan efisiensi dan kenyamanan karyawan dengan tetap memperhatikan estetika.', 'briefcase', ARRAY['Layout ruang kerja optimal', 'Furniture ergonomis', 'Pencahayaan yang tepat', 'Branding interior'], 2, true),
('Desain Interior Cafe & Restaurant', 'Desain interior cafe dan restaurant yang menarik dan memorable. Ciptakan atmosfer yang tepat untuk meningkatkan pengalaman pelanggan dan identitas brand Anda.', 'coffee', ARRAY['Konsep tema unik', 'Layout efisien', 'Lighting mood', 'Instagram-worthy spots'], 3, true),
('Renovasi & Remodeling', 'Ubah ruangan lama menjadi ruang impian Anda. Layanan renovasi lengkap dari perencanaan hingga eksekusi dengan hasil maksimal dan tepat waktu.', 'hammer', ARRAY['Survey dan konsultasi', 'Desain renovasi', 'Manajemen proyek', 'Garansi hasil'], 4, true),
('Custom Furniture', 'Furniture custom sesuai kebutuhan dan ukuran ruangan Anda. Dibuat dengan material berkualitas dan craftsmanship terbaik untuk hasil yang tahan lama.', 'chair', ARRAY['Desain custom', 'Material premium', 'Finishing berkualitas', 'Instalasi profesional'], 5, true);

-- Insert sample portfolio
INSERT INTO portfolio (title, description, category, image_url, published, order_index) VALUES
('Modern Minimalist Living Room', 'Desain ruang tamu minimalis modern dengan nuansa hangat dan nyaman. Menggunakan palet warna netral dengan aksen kayu natural untuk menciptakan suasana yang tenang dan elegan.', 'Residential', 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800', true, 1),
('Scandinavian Bedroom', 'Kamar tidur bergaya Scandinavian dengan konsep simple, clean, dan fungsional. Dominasi warna putih dengan sentuhan kayu memberikan kesan fresh dan cozy.', 'Residential', 'https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=800', true, 2),
('Industrial Office Space', 'Ruang kantor bergaya industrial modern dengan exposed brick dan metal elements. Menciptakan atmosfer kerja yang kreatif dan produktif.', 'Commercial', 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=800', true, 3),
('Contemporary Kitchen', 'Dapur kontemporer dengan island counter dan storage yang optimal. Desain yang memaksimalkan fungsi dengan estetika modern yang timeless.', 'Residential', 'https://images.unsplash.com/photo-1556912173-3bb406ef7e77?w=800', true, 4),
('Cozy Cafe Interior', 'Interior cafe dengan konsep warm and cozy. Kombinasi material kayu, tanaman, dan pencahayaan hangat menciptakan suasana yang nyaman untuk bersantai.', 'Commercial', 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800', true, 5),
('Luxury Master Bedroom', 'Kamar tidur utama mewah dengan walk-in closet dan ensuite bathroom. Desain elegan dengan material premium dan detail yang sempurna.', 'Residential', 'https://images.unsplash.com/photo-1617806118233-18e1de247200?w=800', true, 6),
('Modern Restaurant', 'Restaurant modern dengan open kitchen concept. Layout yang efisien dengan desain yang menarik untuk meningkatkan dining experience.', 'Commercial', 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800', true, 7),
('Kids Playroom', 'Ruang bermain anak yang fun, colorful, dan aman. Desain yang merangsang kreativitas dengan storage yang rapi untuk mainan.', 'Residential', 'https://images.unsplash.com/photo-1587845750216-13825c3c6b1d?w=800', true, 8);

-- Verify inserts
SELECT 'Services inserted: ' || COUNT(*) FROM services;
SELECT 'Portfolio items inserted: ' || COUNT(*) FROM portfolio;
