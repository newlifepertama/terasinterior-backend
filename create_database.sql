-- ============================================
-- CREATE DATABASE SCHEMA - TERAS INTERIOR
-- Sesuai dengan kebutuhan Frontend
-- ============================================

-- 1. CREATE TABLE: admin_users
CREATE TABLE admin_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. CREATE TABLE: services
CREATE TABLE services (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    icon VARCHAR(100) NOT NULL,
    features TEXT[],
    display_order INTEGER DEFAULT 0,
    published BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. CREATE TABLE: portfolio
CREATE TABLE portfolio (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100) NOT NULL,
    image_url TEXT NOT NULL,
    published BOOLEAN DEFAULT false,
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. CREATE TABLE: contacts
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    message TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'new',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. CREATE TABLE: settings
CREATE TABLE settings (
    id SERIAL PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    value TEXT,
    category VARCHAR(50) NOT NULL,
    label VARCHAR(200) NOT NULL,
    description TEXT,
    input_type VARCHAR(20) DEFAULT 'text',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- INSERT SAMPLE DATA: services
-- ============================================
INSERT INTO services (title, description, icon, features, display_order, published) VALUES
('Desain Interior Rumah', 'Desain interior rumah tinggal yang nyaman, fungsional, dan sesuai dengan gaya hidup Anda. Kami menciptakan ruang yang tidak hanya indah tetapi juga praktis untuk kehidupan sehari-hari.', 'home', ARRAY['Konsultasi desain gratis', 'Gambar 3D rendering', 'Pemilihan material berkualitas', 'Pengawasan proyek'], 1, true),
('Desain Interior Kantor', 'Ciptakan ruang kerja yang produktif dan profesional. Desain kantor modern yang meningkatkan efisiensi dan kenyamanan karyawan dengan tetap memperhatikan estetika.', 'briefcase', ARRAY['Layout ruang kerja optimal', 'Furniture ergonomis', 'Pencahayaan yang tepat', 'Branding interior'], 2, true),
('Desain Interior Cafe & Restaurant', 'Desain interior cafe dan restaurant yang menarik dan memorable. Ciptakan atmosfer yang tepat untuk meningkatkan pengalaman pelanggan dan identitas brand Anda.', 'coffee', ARRAY['Konsep tema unik', 'Layout efisien', 'Lighting mood', 'Instagram-worthy spots'], 3, true),
('Renovasi & Remodeling', 'Ubah ruangan lama menjadi ruang impian Anda. Layanan renovasi lengkap dari perencanaan hingga eksekusi dengan hasil maksimal dan tepat waktu.', 'hammer', ARRAY['Survey dan konsultasi', 'Desain renovasi', 'Manajemen proyek', 'Garansi hasil'], 4, true),
('Custom Furniture', 'Furniture custom sesuai kebutuhan dan ukuran ruangan Anda. Dibuat dengan material berkualitas dan craftsmanship terbaik untuk hasil yang tahan lama.', 'chair', ARRAY['Desain custom', 'Material premium', 'Finishing berkualitas', 'Instalasi profesional'], 5, true);

-- ============================================
-- INSERT SAMPLE DATA: portfolio
-- ============================================
INSERT INTO portfolio (title, description, category, image_url, published, order_index) VALUES
('Modern Minimalist Living Room', 'Desain ruang tamu minimalis modern dengan nuansa hangat dan nyaman. Menggunakan palet warna netral dengan aksen kayu natural untuk menciptakan suasana yang tenang dan elegan.', 'Residential', 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800', true, 1),
('Scandinavian Bedroom', 'Kamar tidur bergaya Scandinavian dengan konsep simple, clean, dan fungsional. Dominasi warna putih dengan sentuhan kayu memberikan kesan fresh dan cozy.', 'Residential', 'https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=800', true, 2),
('Industrial Office Space', 'Ruang kantor bergaya industrial modern dengan exposed brick dan metal elements. Menciptakan atmosfer kerja yang kreatif dan produktif.', 'Commercial', 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=800', true, 3),
('Contemporary Kitchen', 'Dapur kontemporer dengan island counter dan storage yang optimal. Desain yang memaksimalkan fungsi dengan estetika modern yang timeless.', 'Residential', 'https://images.unsplash.com/photo-1556912173-3bb406ef7e77?w=800', true, 4),
('Cozy Cafe Interior', 'Interior cafe dengan konsep warm and cozy. Kombinasi material kayu, tanaman, dan pencahayaan hangat menciptakan suasana yang nyaman untuk bersantai.', 'Commercial', 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800', true, 5),
('Luxury Master Bedroom', 'Kamar tidur utama mewah dengan walk-in closet dan ensuite bathroom. Desain elegan dengan material premium dan detail yang sempurna.', 'Residential', 'https://images.unsplash.com/photo-1617806118233-18e1de247200?w=800', true, 6),
('Modern Restaurant', 'Restaurant modern dengan open kitchen concept. Layout yang efisien dengan desain yang menarik untuk meningkatkan dining experience.', 'Commercial', 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800', true, 7),
('Kids Playroom', 'Ruang bermain anak yang fun, colorful, dan aman. Desain yang merangsang kreativitas dengan storage yang rapi untuk mainan.', 'Residential', 'https://images.unsplash.com/photo-1587845750216-13825c3c6b1d?w=800', true, 8);

-- ============================================
-- INSERT SAMPLE DATA: settings
-- ============================================
INSERT INTO settings (key, value, category, label, description, input_type) VALUES
-- Contact Settings
('contact_phone', '+62 812-3456-7890', 'contact', 'Phone Number', 'Nomor telepon utama perusahaan', 'text'),
('contact_whatsapp', '+62 812-3456-7890', 'contact', 'WhatsApp Number', 'Nomor WhatsApp untuk chat', 'text'),
('contact_email', 'info@terasinterior.com', 'contact', 'Email Address', 'Email utama perusahaan', 'email'),
('contact_address', 'Jl. Contoh No. 123, Jakarta Selatan', 'contact', 'Office Address', 'Alamat kantor lengkap', 'textarea'),

-- Company Settings
('company_name', 'Teras Interior', 'company', 'Company Name', 'Nama perusahaan', 'text'),
('company_tagline', 'Wujudkan Ruang Impian Anda', 'company', 'Company Tagline', 'Tagline perusahaan', 'text'),
('company_description', 'Teras Interior adalah perusahaan desain interior profesional yang berpengalaman dalam menciptakan ruang yang indah, fungsional, dan sesuai dengan kepribadian Anda.', 'company', 'Company Description', 'Deskripsi singkat perusahaan', 'textarea'),

-- Social Media Settings
('social_instagram', 'https://instagram.com/terasinterior', 'social', 'Instagram URL', 'Link Instagram', 'url'),
('social_facebook', 'https://facebook.com/terasinterior', 'social', 'Facebook URL', 'Link Facebook', 'url'),
('social_youtube', '', 'social', 'YouTube URL', 'Link YouTube (optional)', 'url'),
('social_tiktok', '', 'social', 'TikTok URL', 'Link TikTok (optional)', 'url'),

-- SEO Settings
('seo_title', 'Teras Interior - Jasa Desain Interior Profesional', 'seo', 'SEO Title', 'Title untuk SEO', 'text'),
('seo_description', 'Jasa desain interior profesional untuk rumah, kantor, cafe, dan restaurant. Wujudkan ruang impian Anda bersama Teras Interior.', 'seo', 'SEO Description', 'Meta description untuk SEO', 'textarea'),
('seo_keywords', 'desain interior, jasa interior, interior rumah, interior kantor, interior cafe', 'seo', 'SEO Keywords', 'Keywords untuk SEO', 'text'),

-- Business Hours
('hours_weekday', 'Senin - Jumat: 09.00 - 18.00 WIB', 'business', 'Weekday Hours', 'Jam operasional hari kerja', 'text'),
('hours_weekend', 'Sabtu: 09.00 - 15.00 WIB (Minggu Tutup)', 'business', 'Weekend Hours', 'Jam operasional akhir pekan', 'text');

-- ============================================
-- GRANT PERMISSIONS
-- ============================================
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO terasadmin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO terasadmin;

-- ============================================
-- VERIFY
-- ============================================
SELECT 'Database created successfully!' as status;

-- Show table counts
SELECT 'services' as table_name, COUNT(*) as row_count FROM services
UNION ALL
SELECT 'portfolio', COUNT(*) FROM portfolio
UNION ALL
SELECT 'settings', COUNT(*) FROM settings
UNION ALL
SELECT 'contacts', COUNT(*) FROM contacts
UNION ALL
SELECT 'admin_users', COUNT(*) FROM admin_users;
