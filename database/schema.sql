CREATE TABLE IF NOT EXISTS volunteers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    gender TEXT,
    place TEXT,
    phone TEXT NOT NULL,
    message TEXT,
    area_interest TEXT,
    document_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    event_date TEXT NOT NULL,
    location TEXT NOT NULL,
    image_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS funds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    donor_name TEXT NOT NULL,
    amount REAL NOT NULL,
    purpose TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS expenditures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    amount REAL NOT NULL,
    purpose TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS recent_works (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    image_path TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

INSERT OR IGNORE INTO admins (id, username, password)
VALUES (1, 'admin', 'scrypt:32768:8:1$irOn7cpHR3ScVH32$9db3f1c14a5658d8349c1b298765dd69f92078668cf727bb07b728a0dac2565b289696a466559636af16e616ff6fe8b66cde8c69b2db41eb32065608cf28b804');

INSERT OR IGNORE INTO volunteers (id, name, email, gender, place, phone, message, area_interest, document_path, created_at) VALUES
(1, 'Aarav Sharma', 'aarav.sharma@example.org', 'Male', 'Hyderabad', '+91-9000001001', 'I want to help with food drives on weekends.', 'Social Awareness', 'uploads/volunteer_docs/aarav_id.pdf', '2026-04-01 09:00:00'),
(2, 'Diya Patel', 'diya.patel@example.org', 'Female', 'Secunderabad', '+91-9000001002', 'Interested in teaching and children support programs.', 'Education Support', 'uploads/volunteer_docs/diya_resume.pdf', '2026-04-02 10:15:00'),
(3, 'Rohan Mehta', 'rohan.mehta@example.org', 'Male', 'Madhapur', '+91-9000001003', 'Can support logistics and transport coordination.', 'Fund Raising', 'uploads/volunteer_docs/rohan_profile.pdf', '2026-04-03 11:30:00'),
(4, 'Ananya Iyer', 'ananya.iyer@example.org', 'Female', 'Kukatpally', '+91-9000001004', 'Available for health camp registrations and outreach.', 'Medical Wing', 'uploads/volunteer_docs/ananya_doc.pdf', '2026-04-04 12:00:00'),
(5, 'Kabir Singh', 'kabir.singh@example.org', 'Male', 'Begumpet', '+91-9000001005', 'Happy to assist in event setup and coordination.', 'Nature Protection', 'uploads/volunteer_docs/kabir_card.pdf', '2026-04-05 13:20:00'),
(6, 'Meera Nair', 'meera.nair@example.org', 'Female', 'Ameerpet', '+91-9000001006', 'Would like to volunteer in women wellness initiatives.', 'Medical Wing', 'uploads/volunteer_docs/meera_doc.pdf', '2026-04-06 09:45:00'),
(7, 'Vihaan Gupta', 'vihaan.gupta@example.org', 'Male', 'Gachibowli', '+91-9000001007', 'Can support donor communication and follow-ups.', 'Fund Raising', 'uploads/volunteer_docs/vihaan_form.pdf', '2026-04-07 14:10:00'),
(8, 'Ishita Verma', 'ishita.verma@example.org', 'Female', 'Tolichowki', '+91-9000001008', 'Interested in social media and campaign awareness.', 'Social Awareness', 'uploads/volunteer_docs/ishita_cv.pdf', '2026-04-08 15:00:00'),
(9, 'Arjun Rao', 'arjun.rao@example.org', 'Male', 'Miyapur', '+91-9000001009', 'Would love to volunteer for education support sessions.', 'Education Support', 'uploads/volunteer_docs/arjun_doc.pdf', '2026-04-09 16:25:00'),
(10, 'Saanvi Kapoor', 'saanvi.kapoor@example.org', 'Female', 'Jubilee Hills', '+91-9000001010', 'Can help organize supplies and volunteer attendance.', 'Nature Protection', 'uploads/volunteer_docs/saanvi_sheet.pdf', '2026-04-10 17:30:00'),
(11, 'Aditya Joshi', 'aditya.joshi@example.org', 'Male', 'LB Nagar', '+91-9000001011', 'Available for rural outreach trips twice a month.', 'Social Awareness', 'uploads/volunteer_docs/aditya_id.pdf', '2026-04-11 09:05:00'),
(12, 'Priya Menon', 'priya.menon@example.org', 'Female', 'Hitech City', '+91-9000001012', 'Interested in documenting impact stories and photos.', 'Animal Welfare', 'uploads/volunteer_docs/priya_portfolio.pdf', '2026-04-12 10:40:00'),
(13, 'Dev Malhotra', 'dev.malhotra@example.org', 'Male', 'Mehdipatnam', '+91-9000001013', 'Can support technology, registration, and reporting.', 'Fund Raising', 'uploads/volunteer_docs/dev_doc.pdf', '2026-04-13 11:50:00'),
(14, 'Nisha Reddy', 'nisha.reddy@example.org', 'Female', 'Banjara Hills', '+91-9000001014', 'Available for elderly support visits and events.', 'Social Awareness', 'uploads/volunteer_docs/nisha_file.pdf', '2026-04-14 13:35:00'),
(15, 'Yash Chawla', 'yash.chawla@example.org', 'Others', 'Foundation Main Office', '+91-9000001015', 'Would like to assist with weekend community classes.', 'Education Support', 'uploads/volunteer_docs/yash_proof.pdf', '2026-04-15 14:55:00');

INSERT OR IGNORE INTO events (id, title, description, event_date, location, image_path, created_at) VALUES
(1, 'Community Breakfast Drive', 'Serving fresh breakfast packs to daily wage workers and nearby families.', '2026-06-01', 'Hyderabad Central Hall', 'images/events/breakfast_drive.jpg', '2026-04-01 08:00:00'),
(2, 'School Supply Donation Camp', 'Collecting notebooks, pens, and school kits for under-resourced students.', '2026-06-03', 'Secunderabad Learning Center', 'images/events/school_supplies.jpg', '2026-04-02 08:00:00'),
(3, 'Women Wellness Workshop', 'A wellness and awareness session focused on preventive care and nutrition.', '2026-06-05', 'Banjara Hills Community Space', 'images/events/women_wellness.jpg', '2026-04-03 08:00:00'),
(4, 'Medical Checkup Camp', 'General health screening camp with volunteer registration support.', '2026-06-07', 'Madhapur Clinic Grounds', 'images/events/medical_camp.jpg', '2026-04-04 08:00:00'),
(5, 'Youth Career Guidance Session', 'Mentoring event for students exploring career and scholarship options.', '2026-06-10', 'Kukatpally Resource Hub', 'images/events/career_guidance.jpg', '2026-04-05 08:00:00'),
(6, 'Clothes Distribution Day', 'Sorting and distributing donated clothing for families in need.', '2026-06-12', 'Begumpet Outreach Point', 'images/events/clothes_distribution.jpg', '2026-04-06 08:00:00'),
(7, 'Senior Citizen Care Visit', 'Volunteer visits focused on companionship and support for elders.', '2026-06-14', 'Ameerpet Senior Center', 'images/events/senior_care.jpg', '2026-04-07 08:00:00'),
(8, 'Nutrition Awareness Program', 'Session on low-cost healthy meal planning for local families.', '2026-06-16', 'Mehdipatnam Community Hall', 'images/events/nutrition_program.jpg', '2026-04-08 08:00:00'),
(9, 'Blood Donation Camp', 'Partnered donation camp with local hospitals and volunteer coordination.', '2026-06-18', 'Gachibowli Public Ground', 'images/events/blood_donation.jpg', '2026-04-09 08:00:00'),
(10, 'Evening Study Circle', 'Education support and tutoring for middle school students.', '2026-06-20', 'Tolichowki Study Center', 'images/events/study_circle.jpg', '2026-04-10 08:00:00'),
(11, 'Monsoon Relief Preparation', 'Packing emergency kits ahead of seasonal rain impacts.', '2026-06-22', 'LB Nagar Distribution Hub', 'images/events/relief_prep.jpg', '2026-04-11 08:00:00'),
(12, 'Community Clean-Up Drive', 'Public cleanliness and awareness activity with resident volunteers.', '2026-06-24', 'Hitech City Lake Area', 'images/events/cleanup_drive.jpg', '2026-04-12 08:00:00'),
(13, 'Parents Counseling Meet', 'Guidance session for parents on education continuity and support.', '2026-06-26', 'Miyapur Family Center', 'images/events/parents_meet.jpg', '2026-04-13 08:00:00'),
(14, 'Fundraising Dinner', 'A donor appreciation and fundraising evening for ongoing projects.', '2026-06-28', 'Jubilee Hills Banquet Hall', 'images/events/fundraising_dinner.jpg', '2026-04-14 08:00:00'),
(15, 'Volunteer Orientation Day', 'Introductory session for new volunteers across foundation programs.', '2026-06-30', 'Foundation Main Office', 'images/events/orientation_day.jpg', '2026-04-15 08:00:00');

INSERT OR IGNORE INTO funds (id, donor_name, amount, purpose, created_at) VALUES
(1, 'Ritika Foundation', 25000.00, 'Medical Awareness Camp', '2026-04-01 10:00:00'),
(2, 'Suresh Kumar', 5000.00, 'Plantation for Nature', '2026-04-02 10:00:00'),
(3, 'Anita Rao', 7500.00, 'Social Welfare Kits', '2026-04-03 10:00:00'),
(4, 'Bright Future Trust', 30000.00, 'Education Support Program', '2026-04-04 10:00:00'),
(5, 'Neha Agarwal', 4200.00, 'Animal Welfare Feeding Drive', '2026-04-05 10:00:00'),
(6, 'Rahul Bansal', 6100.00, 'Fund Raising Event Support', '2026-04-06 10:00:00'),
(7, 'CareBridge Pvt Ltd', 18000.00, 'Medical Awareness Camp', '2026-04-07 10:00:00'),
(8, 'Pooja Sethi', 3500.00, 'Tree Plantation Activity', '2026-04-08 10:00:00'),
(9, 'Harish Reddy', 8000.00, 'Community Relief Materials', '2026-04-09 10:00:00'),
(10, 'Unity Housing Group', 22000.00, 'Social Welfare Outreach', '2026-04-10 10:00:00'),
(11, 'Sneha Kulkarni', 5600.00, 'Volunteer Orientation Support', '2026-04-11 10:00:00'),
(12, 'Vardhan Textiles', 14500.00, 'Clothing and Essentials Distribution', '2026-04-12 10:00:00'),
(13, 'Amit Desai', 9000.00, 'Education Materials', '2026-04-13 10:00:00'),
(14, 'GreenLeaf Organics', 12750.00, 'Nature Protection Initiative', '2026-04-14 10:00:00'),
(15, 'Kiran Varma', 6400.00, 'Animal Welfare Support', '2026-04-15 10:00:00');

INSERT OR IGNORE INTO expenditures (id, event_name, amount, purpose, created_at) VALUES
(1, 'Community Breakfast Drive', 4200.00, 'Food packets and logistics', '2026-04-01 12:00:00'),
(2, 'School Supply Donation Camp', 5600.00, 'School kits and transport', '2026-04-02 12:00:00'),
(3, 'Women Wellness Workshop', 6800.00, 'Awareness materials and setup', '2026-04-03 12:00:00'),
(4, 'Medical Checkup Camp', 12500.00, 'Medical supplies and registrations', '2026-04-04 12:00:00'),
(5, 'Youth Career Guidance Session', 3500.00, 'Printed materials and refreshments', '2026-04-05 12:00:00'),
(6, 'Clothes Distribution Day', 7100.00, 'Packaging and local transport', '2026-04-06 12:00:00'),
(7, 'Senior Citizen Care Visit', 2900.00, 'Care packs and volunteer travel', '2026-04-07 12:00:00'),
(8, 'Nutrition Awareness Program', 4800.00, 'Educational kits and venue support', '2026-04-08 12:00:00'),
(9, 'Blood Donation Camp', 8400.00, 'Medical assistance and banners', '2026-04-09 12:00:00'),
(10, 'Evening Study Circle', 2600.00, 'Study materials and snacks', '2026-04-10 12:00:00'),
(11, 'Monsoon Relief Preparation', 9300.00, 'Emergency kit preparation', '2026-04-11 12:00:00'),
(12, 'Community Clean-Up Drive', 3900.00, 'Gloves, bags, and signage', '2026-04-12 12:00:00'),
(13, 'Parents Counseling Meet', 3100.00, 'Session setup and stationery', '2026-04-13 12:00:00'),
(14, 'Fundraising Dinner', 15200.00, 'Venue and hospitality', '2026-04-14 12:00:00'),
    (15, 'Volunteer Orientation Day', 4400.00, 'Welcome kits and presentation setup', '2026-04-15 12:00:00');
