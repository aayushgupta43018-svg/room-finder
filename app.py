
# from flask import session, redirect, url_for
# from werkzeug.security import generate_password_hash, check_password_hash
# import os
# import uuid
# from flask import (
#     Flask, jsonify, request, send_from_directory,
#     render_template_string
# )
# from werkzeug.utils import secure_filename
# from db import get_db_connection

# app = Flask(__name__)
# app.secret_key = os.environ.get(
#     "FLASK_SECRET_KEY",
#     "dev-only-change-this-secret-before-deployment"
# )
# UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
# ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

# os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# @app.route("/")
# def home():
#     logged_in = "user_id" in session
#     user_name = session.get("user_name", "")
#     user_role = session.get("user_role", "")

#     return render_template_string("""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1">
#         <title>Room Finder | Find a place to call home</title>
#         <style>
#             :root { --navy: #132238; --blue: #315efb; --muted: #68758a; --bg: #f5f7fb; --line: #e5eaf2; }
#             * { box-sizing: border-box; }
#             body { margin: 0; font-family: Inter, Arial, sans-serif; color: var(--navy); background: var(--bg); }
#             a { text-decoration: none; }
#             .nav { max-width: 1160px; margin: auto; padding: 22px 24px; display: flex; align-items: center; justify-content: space-between; gap: 18px; }
#             .brand { color: var(--navy); font-size: 23px; font-weight: 800; letter-spacing: -.7px; }
#             .brand span { color: var(--blue); }
#             .navlinks { display: flex; align-items: center; flex-wrap: wrap; gap: 18px; }
#             .navlinks a { color: #46546a; font-size: 14px; font-weight: 650; }
#             .navlinks .nav-cta { background: var(--blue); color: white; padding: 11px 16px; border-radius: 11px; }
#             .hero-wrap { padding: 28px 24px 58px; }
#             .hero { max-width: 1112px; margin: auto; min-height: 390px; border-radius: 28px; padding: 56px; color: white; overflow: hidden; position: relative; background: linear-gradient(120deg, #142944 0%, #234d8e 62%, #3979d7 100%); box-shadow: 0 24px 60px rgba(26, 58, 104, .16); }
#             .hero:after { content: ''; position: absolute; width: 360px; height: 360px; border: 1px solid rgba(255,255,255,.17); border-radius: 50%; right: -70px; top: 20px; box-shadow: 0 0 0 36px rgba(255,255,255,.035), 0 0 0 72px rgba(255,255,255,.025); }
#             .eyebrow { display: inline-block; color: #dce7ff; background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.18); border-radius: 999px; padding: 8px 13px; font-size: 12px; font-weight: 750; letter-spacing: .8px; text-transform: uppercase; }
#             h1 { max-width: 610px; margin: 22px 0 15px; font-size: clamp(36px, 5vw, 58px); line-height: 1.05; letter-spacing: -1.8px; }
#             .hero p { max-width: 540px; color: #e0e9f8; line-height: 1.7; font-size: 16px; margin: 0 0 28px; }
#             .actions { display: flex; flex-wrap: wrap; gap: 12px; }
#             .btn { display: inline-flex; justify-content: center; align-items: center; border-radius: 12px; padding: 14px 19px; font-weight: 750; font-size: 14px; }
#             .btn-light { background: white; color: #18345d; }
#             .btn-outline { border: 1px solid rgba(255,255,255,.48); color: white; background: rgba(255,255,255,.07); }
#             .content { max-width: 1112px; margin: 0 auto; padding: 0 24px 58px; }
#             .section-head { display: flex; align-items: end; justify-content: space-between; gap: 16px; margin: 0 0 22px; }
#             .section-head h2 { font-size: 25px; letter-spacing: -.6px; margin: 0 0 7px; }
#             .section-head p { color: var(--muted); margin: 0; font-size: 14px; }
#             .cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
#             .card { background: white; border: 1px solid var(--line); border-radius: 18px; padding: 24px; box-shadow: 0 8px 26px rgba(22, 41, 71, .035); }
#             .icon { width: 44px; height: 44px; border-radius: 13px; display: grid; place-items: center; background: #edf2ff; color: var(--blue); font-size: 21px; margin-bottom: 18px; }
#             .card h3 { margin: 0 0 9px; font-size: 17px; }
#             .card p { margin: 0 0 17px; color: var(--muted); line-height: 1.6; font-size: 14px; }
#             .card a { color: var(--blue); font-weight: 750; font-size: 14px; }
#             .welcome { max-width: 1112px; margin: 0 auto 20px; padding: 0 24px; color: #36516e; font-size: 14px; }
#             footer { border-top: 1px solid var(--line); padding: 22px 24px; text-align: center; color: var(--muted); font-size: 12px; }
#             @media (max-width: 760px) { .nav { align-items: flex-start; flex-direction: column; } .navlinks { gap: 13px; } .hero { padding: 34px 25px; min-height: auto; } .hero:after { right: -230px; opacity: .7; } .cards { grid-template-columns: 1fr; } .section-head { align-items: flex-start; flex-direction: column; } }
#         </style>
#     </head>
#     <body>
#         <header class="nav">
#             <a class="brand" href="/">Room<span>Finder</span></a>
#             <nav class="navlinks">
#                 <a href="/browse-rooms">Browse rooms</a>
#                 {% if logged_in %}
#                     <a href="/dashboard">Dashboard</a>
#                     {% if user_role == 'OWNER' %}<a href="/add-room-page">Add a room</a>{% endif %}
#                     <a class="nav-cta" href="/logout">Logout</a>
#                 {% else %}
#                     <a href="/login">Login</a>
#                     <a class="nav-cta" href="/register">Create account</a>
#                 {% endif %}
#             </nav>
#         </header>

#         {% if logged_in %}<div class="welcome">Welcome back, <strong>{{ user_name }}</strong> · Account type: {{ user_role|title }}</div>{% endif %}

#         <main>
#             <section class="hero-wrap">
#                 <div class="hero">
#                     <span class="eyebrow">A simpler way to find your space</span>
#                     <h1>Find a room that feels like home.</h1>
#                     <p>Explore rooms by city, PIN code and budget. Compare rent, check room photos and contact the owner to take the next step.</p>
#                     <div class="actions">
#                         <a class="btn btn-light" href="/browse-rooms">Explore available rooms &nbsp; →</a>
#                         {% if logged_in and user_role == 'OWNER' %}
#                             <a class="btn btn-outline" href="/add-room-page">List your room</a>
#                         {% elif not logged_in %}
#                             <a class="btn btn-outline" href="/register">Join Room Finder</a>
#                         {% else %}
#                             <a class="btn btn-outline" href="/dashboard">Open dashboard</a>
#                         {% endif %}
#                     </div>
#                 </div>
#             </section>

#             <section class="content">
#                 <div class="section-head">
#                     <div><h2>Everything you need to get started</h2><p>Simple tools for room seekers and property owners.</p></div>
#                 </div>
#                 <div class="cards">
#                     <article class="card">
#                         <div class="icon">⌕</div><h3>Browse rooms</h3>
#                         <p>Search available rooms by city, PIN code and maximum rent, then open a listing to see its details.</p>
#                         <a href="/browse-rooms">Search rooms →</a>
#                     </article>
#                     <article class="card">
#                         <div class="icon">⌂</div><h3>List your room</h3>
#                         <p>Room owners can sign in, add a listing with location details and share photos of the room.</p>
#                         {% if logged_in and user_role == 'OWNER' %}<a href="/add-room-page">Add a room →</a>{% elif not logged_in %}<a href="/register">Create an owner account →</a>{% else %}<a href="/dashboard">Open dashboard →</a>{% endif %}
#                     </article>
#                     <article class="card">
#                         <div class="icon">◎</div><h3>Your account</h3>
#                         <p>Use your dashboard to access account features. Sign in to continue or create an account to get started.</p>
#                         {% if logged_in %}<a href="/dashboard">Go to dashboard →</a>{% else %}<a href="/login">Login or register →</a>{% endif %}
#                     </article>
#                 </div>
#             </section>
#         </main>
#         <footer>Room Finder · Search smarter. Find your space.</footer>
#     </body>
#     </html>
#     """, logged_in=logged_in, user_name=user_name, user_role=user_role)

# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         name = request.form.get("name", "").strip()
#         email = request.form.get("email", "").strip().lower()
#         phone = request.form.get("phone", "").strip()
#         password = request.form.get("password", "")
#         confirm_password = request.form.get("confirm_password", "")
#         role = request.form.get("role", "").upper()

#         if not name or not email or not phone or not password:
#             return "Please fill in all fields.", 400

#         if password != confirm_password:
#             return "Passwords do not match.", 400

#         if len(password) < 8:
#             return "Password must be at least 8 characters.", 400

#         if role not in ("OWNER", "TENANT"):
#             return "Please select a valid role.", 400

#         connection = get_db_connection()
#         cursor = connection.cursor(dictionary=True)

#         try:
#             cursor.execute(
#                 "SELECT user_id FROM users WHERE email = %s",
#                 (email,)
#             )
#             if cursor.fetchone():
#                 return "This email is already registered.", 409

#             hashed_password = generate_password_hash(password)

#             cursor.execute("""
#                 INSERT INTO users (name, email, phone, password, role)
#                 VALUES (%s, %s, %s, %s, %s)
#             """, (name, email, phone, hashed_password, role))

#             connection.commit()

#             return """
#                 <h2>Registration successful!</h2>
#                 <p>Your account has been created.</p>
#                 <a href="/login">Go to Login</a>
#                 <br><br><a href="/">Home</a>
#             """, 201

#         except Exception:
#             connection.rollback()
#             app.logger.exception("Registration failed")
#             return "Registration failed. Please check the server log.", 500

#         finally:
#             cursor.close()
#             connection.close()

#     return """
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1">
#         <title>Register - Room Finder</title>
#     </head>
#     <body>
#         <h1>Create Your Account</h1>

#         <form method="POST" action="/register">
#             <label>Full Name</label><br>
#             <input type="text" name="name" required maxlength="100">
#             <br><br>

#             <label>Email</label><br>
#             <input type="email" name="email" required maxlength="255">
#             <br><br>

#             <label>Phone</label><br>
#             <input type="tel" name="phone" required maxlength="20">
#             <br><br>

#             <label>Password (minimum 8 characters)</label><br>
#             <input type="password" name="password"
#                    minlength="8" required>
#             <br><br>

#             <label>Confirm Password</label><br>
#             <input type="password" name="confirm_password"
#                    minlength="8" required>
#             <br><br>

#             <label>Account Type</label><br>
#             <select name="role" required>
#                 <option value="">Choose account type</option>
#                 <option value="OWNER">Room Owner</option>
#                 <option value="TENANT">Room Seeker (Tenant)</option>
#             </select>
#             <br><br>

#             <button type="submit">Register</button>
#         </form>

#         <p>Already have an account? <a href="/login">Login</a></p>
#         <a href="/">Home</a>
#     </body>
#     </html>
#     """


# # Return available rooms as JSON
# @app.route("/rooms")
# def get_rooms():
#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)

#     try:
#         cursor.execute("""
#             SELECT r.room_id, r.title, r.description,
#                    r.rent, r.room_type, r.furnished,
#                    l.city, l.state, l.colony,
#                    l.address, l.pincode
#             FROM rooms r
#             LEFT JOIN locations l ON r.room_id = l.room_id
#             WHERE r.available = TRUE
#             ORDER BY r.room_id DESC
#         """)
#         rooms = cursor.fetchall()

#         for room in rooms:
#             cursor.execute(
#                 "SELECT photo_path FROM room_photos WHERE room_id = %s",
#                 (room["room_id"],)
#             )
#             photos = cursor.fetchall()
#             room["photos"] = [
#                 f"/uploads/{photo['photo_path']}" for photo in photos
#             ]

#         return jsonify(rooms)
#     finally:
#         cursor.close()
#         connection.close()


# # Display uploaded photos
# @app.route("/uploads/<path:filename>")
# def uploaded_file(filename):
#     return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# # Page to add a room
# @app.route("/add-room-page")
# def add_room_page():
#     if "user_id" not in session:
#         return redirect(url_for("login"))

#     if session.get("user_role") != "OWNER":
#         return "Only room owners can access this page.", 403

#     return """
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <title>Add Room</title>
#         <meta name="viewport" content="width=device-width, initial-scale=1">
#     </head>
#     <body>
#         <h2>Add New Room</h2>
#         <form action="/add-room" method="POST">
#             Room Title:
#             <input type="text" name="title" required>
#             <br><br>

#             Description:
#             <input type="text" name="description">
#             <br><br>

#             Monthly Rent (Rs):
#             <input type="number" name="rent" min="0" required>
#             <br><br>

#             Room Type:
#             <input type="text" name="room_type"
#                    placeholder="Single room, flat, PG" required>
#             <br><br>

#             City:
#             <input type="text" name="city" required>
#             <br><br>

#             State:
#             <input type="text" name="state" required>
#             <br><br>

#             Colony:
#             <input type="text" name="colony">
#             <br><br>

#             Full Address:
#             <input type="text" name="address">
#             <br><br>

#             Pincode:
#             <input type="text" name="pincode"
#                    pattern="[0-9]{6}"
#                    title="Enter a 6-digit pincode">
#             <br><br>

#             Furnished:
#             <input type="checkbox" name="furnished" value="true">
#             <br><br>

#             <button type="submit">Add Room</button>
#         </form>

#         <br><a href="/browse-rooms">Browse Rooms</a>
#     </body>
#     </html>
#     """


# # Save room and its location in MySQL
# @app.route("/add-room", methods=["POST"])
# def add_room():
#     if "user_id" not in session:
#         return redirect(url_for("login"))

#     if session.get("user_role") != "OWNER":
#         return "Only room owners can add rooms.", 403

#     owner_id = session["user_id"]
#     title = request.form.get("title", "").strip()
#     description = request.form.get("description", "").strip() or None
#     rent = request.form.get("rent", type=float)
#     room_type = request.form.get("room_type", "").strip()
#     furnished = request.form.get("furnished") == "true"

#     city = request.form.get("city", "").strip()
#     state = request.form.get("state", "").strip()
#     colony = request.form.get("colony", "").strip() or None
#     address = request.form.get("address", "").strip() or None
#     pincode = request.form.get("pincode", "").strip() or None

#     if not owner_id or not title or rent is None or rent < 0:
#         return "Please enter a valid owner, title and rent.", 400

#     if not room_type or not city or not state:
#         return "Room type, city and state are required.", 400

#     if pincode and (
#         len(pincode) != 6 or not pincode.isdigit()
#     ):
#         return "Pincode must contain exactly 6 digits.", 400

#     connection = get_db_connection()
#     cursor = connection.cursor()

#     try:
#         cursor.execute("""
#             INSERT INTO rooms
#                 (owner_id, title, description, rent,
#                  room_type, furnished)
#             VALUES (%s, %s, %s, %s, %s, %s)
#         """, (
#             owner_id, title, description, rent,
#             room_type, furnished
#         ))

#         room_id = cursor.lastrowid

#         cursor.execute("""
#             INSERT INTO locations
#                 (room_id, city, state, colony, address, pincode)
#             VALUES (%s, %s, %s, %s, %s, %s)
#         """, (
#             room_id, city, state, colony, address, pincode
#         ))

#         connection.commit()

#         return f"""
#         <!DOCTYPE html>
#         <html>
#         <body>
#             <h2>Room added successfully!</h2>
#             <p>Your Room ID is: {room_id}</p>
#             <p>Remember this ID to upload its photo.</p>
#             <a href="/upload-photo-page">Upload Room Photo</a><br><br>
#             <a href="/browse-rooms">Browse Rooms</a><br><br>
#             <a href="/">Home</a>
#         </body>
#         </html>
#         """, 201

#     except Exception as error:
#         connection.rollback()
#         app.logger.exception("Unable to add room")
#         return f"Database error: {error}", 400

#     finally:
#         cursor.close()
#         connection.close()


# # Page to upload a room photo
# @app.route("/upload-photo-page")
# def upload_photo_page():
#     if "user_id" not in session:
#         return redirect(url_for("login"))

#     if session.get("user_role") != "OWNER":
#         return "Only room owners can upload room photos.", 403

#     return """
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <title>Upload Room Photo</title>
#     </head>
#     <body>
#         <h2>Upload Room Photo</h2>
#         <form action="/upload-photo" method="POST"
#               enctype="multipart/form-data">
#             Room ID:
#             <input type="number" name="room_id" min="1" required>
#             <br><br>

#             Select Photo:
#             <input type="file" name="photo"
#                    accept=".jpg,.jpeg,.png,.webp" required>
#             <br><br>

#             <button type="submit">Upload Photo</button>
#         </form>
#         <p>Allowed formats: JPG, JPEG, PNG, WEBP. Maximum size: 5 MB.</p>
#         <a href="/browse-rooms">Browse Rooms</a>
#     </body>
#     </html>
#     """


# # Save photo to uploads folder and filename to MySQL
# @app.route("/upload-photo", methods=["POST"])
# def upload_photo():
#     if "user_id" not in session:
#         return redirect(url_for("login"))

#     if session.get("user_role") != "OWNER":
#         return "Only room owners can upload room photos.", 403

#     room_id = request.form.get("room_id", type=int)
#     photo = request.files.get("photo")

#     if not room_id or not photo or not photo.filename:
#         return "Please provide a valid Room ID and photo.", 400

#     original_name = secure_filename(photo.filename)

#     if "." not in original_name:
#         return "Invalid photo filename.", 400

#     extension = original_name.rsplit(".", 1)[1].lower()

#     if extension not in ALLOWED_EXTENSIONS:
#         return "Only JPG, JPEG, PNG and WEBP images are allowed.", 400

#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)
#     saved_path = None

#     try:
#         cursor.execute(
#             "SELECT room_id FROM rooms WHERE room_id = %s AND owner_id = %s",
#             (room_id, session["user_id"])
#         )

#         if cursor.fetchone() is None:
#             return "Room not found, or this room does not belong to your account.", 404

#         filename = f"{uuid.uuid4().hex}.{extension}"
#         saved_path = os.path.join(
#             app.config["UPLOAD_FOLDER"], filename
#         )

#         photo.save(saved_path)

#         cursor.execute("""
#             INSERT INTO room_photos (room_id, photo_path)
#             VALUES (%s, %s)
#         """, (room_id, filename))

#         connection.commit()

#         return f"""
#         <!DOCTYPE html>
#         <html>
#         <body>
#             <h2>Photo uploaded successfully!</h2>
#             <img src="/uploads/{filename}"
#                  width="350" alt="Uploaded room photo">
#             <br><br>
#             <a href="/browse-rooms">Browse Rooms</a><br><br>
#             <a href="/upload-photo-page">Upload Another Photo</a>
#         </body>
#         </html>
#         """

#     except Exception as error:
#         connection.rollback()

#         if saved_path and os.path.exists(saved_path):
#             os.remove(saved_path)

#         app.logger.exception("Photo upload failed")
#         return f"Photo upload failed: {error}", 400

#     finally:
#         cursor.close()
#         connection.close()


# # Browse rooms and filter by city, pincode and maximum rent
# @app.route("/browse-rooms")
# def browse_rooms():
#     city = request.args.get("city", "").strip()
#     pincode = request.args.get("pincode", "").strip()
#     max_rent_text = request.args.get("max_rent", "").strip()

#     if pincode and (
#         len(pincode) != 6 or not pincode.isdigit()
#     ):
#         return "Pincode must contain exactly 6 digits.", 400

#     max_rent = None

#     if max_rent_text:
#         try:
#             max_rent = float(max_rent_text)
#             if max_rent < 0:
#                 return "Maximum rent cannot be negative.", 400
#         except ValueError:
#             return "Please enter a valid maximum rent.", 400

#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)

#     try:
#         query = """
#             SELECT
#                 r.room_id,
#                 r.title,
#                 r.description,
#                 r.rent,
#                 r.room_type,
#                 r.furnished,
#                 l.city,
#                 l.state,
#                 l.colony,
#                 l.address,
#                 l.pincode,
#                 (
#                     SELECT rp.photo_path
#                     FROM room_photos rp
#                     WHERE rp.room_id = r.room_id
#                     ORDER BY rp.photo_id DESC
#                     LIMIT 1
#                 ) AS photo_path
#             FROM rooms r
#             LEFT JOIN locations l ON l.room_id = r.room_id
#             WHERE r.available = TRUE
#         """

#         conditions = []
#         values = []

#         if city:
#             conditions.append("l.city LIKE %s")
#             values.append(f"%{city}%")

#         if pincode:
#             conditions.append("l.pincode = %s")
#             values.append(pincode)

#         if max_rent is not None:
#             conditions.append("r.rent <= %s")
#             values.append(max_rent)

#         if conditions:
#             query += " AND " + " AND ".join(conditions)

#         query += " ORDER BY r.room_id DESC"

#         cursor.execute(query, tuple(values))
#         rooms = cursor.fetchall()

#         return render_template_string("""
#         <!DOCTYPE html>
#         <html lang="en">
#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport"
#                   content="width=device-width, initial-scale=1">
#             <title>Find Your Room</title>

#             <style>
#                 * {
#                     box-sizing: border-box;
#                 }

#                 body {
#                     font-family: Arial, sans-serif;
#                     background: #f3f5f8;
#                     margin: 0;
#                     padding: 24px;
#                     color: #202938;
#                 }

#                 h1 {
#                     text-align: center;
#                 }

#                 .top-links {
#                     text-align: center;
#                     margin: 18px;
#                 }

#                 .top-links a {
#                     margin: 8px;
#                     color: #1769e0;
#                 }

#                 .filters {
#                     background: white;
#                     padding: 20px;
#                     border-radius: 12px;
#                     margin: 22px auto;
#                     display: flex;
#                     flex-wrap: wrap;
#                     gap: 14px;
#                     align-items: end;
#                     max-width: 1100px;
#                     box-shadow: 0 3px 12px #0001;
#                 }

#                 .filters label {
#                     display: block;
#                     margin-bottom: 7px;
#                     font-weight: bold;
#                 }

#                 .filters input {
#                     padding: 11px;
#                     border: 1px solid #cbd2dc;
#                     border-radius: 7px;
#                     width: 190px;
#                     max-width: 100%;
#                 }

#                 button {
#                     padding: 12px 18px;
#                     background: #1769e0;
#                     color: white;
#                     border: 0;
#                     border-radius: 7px;
#                     cursor: pointer;
#                 }

#                 button:hover {
#                     background: #0e50b5;
#                 }

#                 .reset {
#                     padding: 12px 4px;
#                     color: #1769e0;
#                 }

#                 .count {
#                     max-width: 1100px;
#                     margin: 20px auto;
#                 }

#                 .rooms {
#                     max-width: 1100px;
#                     margin: auto;
#                     display: grid;
#                     grid-template-columns:
#                         repeat(auto-fit, minmax(260px, 1fr));
#                     gap: 20px;
#                 }

#                 .card {
#                     background: white;
#                     padding: 15px;
#                     border-radius: 12px;
#                     box-shadow: 0 3px 12px #0001;
#                     overflow-wrap: anywhere;
#                 }

#                 .card img {
#                     width: 100%;
#                     height: 195px;
#                     object-fit: cover;
#                     border-radius: 8px;
#                     background: #e8edf3;
#                 }

#                 .rent {
#                     color: #087443;
#                     font-size: 22px;
#                     font-weight: bold;
#                 }

#                 .no-photo {
#                     height: 195px;
#                     display: grid;
#                     place-items: center;
#                     background: #eef1f5;
#                     border-radius: 8px;
#                     color: #626b78;
#                 }

#                 .empty {
#                     background: white;
#                     padding: 24px;
#                     border-radius: 12px;
#                     grid-column: 1 / -1;
#                 }

#                 @media (max-width: 600px) {
#                     body {
#                         padding: 14px;
#                     }

#                     .filters {
#                         align-items: stretch;
#                     }

#                     .filters input {
#                         width: 100%;
#                     }

#                     .filters > div {
#                         width: 100%;
#                     }
#                 }
#             </style>
#         </head>

#         <body>
#             <h1>Find Your Room</h1>

#             <div class="top-links">
#                 <a href="/">Home</a>
#                 <a href="/add-room-page">Add Room</a>
#                 <a href="/upload-photo-page">Upload Photo</a>
#             </div>

#             <form class="filters" action="/browse-rooms" method="GET">
#                 <div>
#                     <label for="city">City</label>
#                     <input id="city" type="text" name="city"
#                            placeholder="e.g. Indore"
#                            value="{{ city }}">
#                 </div>

#                 <div>
#                     <label for="pincode">Pincode</label>
#                     <input id="pincode" type="text" name="pincode"
#                            inputmode="numeric" pattern="[0-9]{6}"
#                            placeholder="6-digit pincode"
#                            value="{{ pincode }}">
#                 </div>

#                 <div>
#                     <label for="max_rent">Maximum monthly rent (Rs)</label>
#                     <input id="max_rent" type="number" name="max_rent"
#                            min="0" step="any" placeholder="e.g. 6000"
#                            value="{{ max_rent_text }}">
#                 </div>

#                 <button type="submit">Search Rooms</button>
#                 <a class="reset" href="/browse-rooms">Clear filters</a>
#             </form>

#             <p class="count">
#                 Rooms found: <strong>{{ rooms|length }}</strong>
#             </p>

#             <div class="rooms">
#                 {% for room in rooms %}
#                 <article class="card">
#                     {% if room.photo_path %}
#                     <img
#                         src="{{ url_for('uploaded_file', filename=room.photo_path) }}"
#                         alt="Photo of {{ room.title }}">
#                     {% else %}
#                     <div class="no-photo">Photo not uploaded yet</div>
#                     {% endif %}

#                     <h2>{{ room.title }}</h2>

#                     <p class="rent">
#                         Rs {{ room.rent }} / month
#                     </p>

#                     <p>{{ room.description or '' }}</p>
#                     <p><b>Room type:</b> {{ room.room_type }}</p>
#                     <p><b>City:</b> {{ room.city or 'Not provided' }}</p>
#                     <p><b>State:</b> {{ room.state or 'Not provided' }}</p>
#                     <p><b>Colony:</b> {{ room.colony or 'Not provided' }}</p>
#                     <p><b>Address:</b> {{ room.address or 'Not provided' }}</p>
#                     <p><b>Pincode:</b> {{ room.pincode or 'Not provided' }}</p>
#                     <p>
#                         <b>Furnished:</b>
#                         {{ 'Yes' if room.furnished else 'No' }}
#                     </p>
#                     <p><b>Room ID:</b> {{ room.room_id }}</p>
#                     <a href="{{ url_for('room_details', room_id=room.room_id) }}"
#                        style="display:inline-block; background:#1769e0; color:white; padding:10px 14px; border-radius:7px; text-decoration:none;">
#                         View Details
#                     </a>
#                 </article>
#                 {% else %}
#                 <div class="empty">
#                     <h2>No rooms found</h2>
#                     <p>
#                         Try another city, pincode, or maximum rent.
#                     </p>
#                 </div>
#                 {% endfor %}
#             </div>
#         </body>
#         </html>
#         """,
#         rooms=rooms,
#         city=city,
#         pincode=pincode,
#         max_rent_text=max_rent_text
#         )

#     finally:
#         cursor.close()
#         connection.close()


# @app.errorhandler(413)
# def file_too_large(error):
#     return "Photo size must be 5 MB or less.", 413

# @app.route("/room/<int:room_id>")
# def room_details(room_id):
#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)

#     try:
#         cursor.execute("""
#             SELECT
#                 r.room_id,
#                 r.owner_id,
#                 r.title,
#                 r.description,
#                 r.rent,
#                 r.room_type,
#                 r.furnished,
#                 l.city,
#                 l.state,
#                 l.colony,
#                 l.address,
#                 l.pincode,
#                 u.name AS owner_name,
#                 u.email AS owner_email,
#                 u.phone AS owner_phone
#             FROM rooms r
#             LEFT JOIN locations l
#                 ON r.room_id = l.room_id
#             LEFT JOIN users u
#                 ON r.owner_id = u.user_id
#             WHERE r.room_id = %s
#               AND r.available = TRUE
#         """, (room_id,))

#         room = cursor.fetchone()

#         if room is None:
#             return "Room not found or no longer available.", 404

#         cursor.execute("""
#             SELECT photo_path
#             FROM room_photos
#             WHERE room_id = %s
#             ORDER BY photo_id DESC
#         """, (room_id,))

#         photos = cursor.fetchall()

#         return render_template_string("""
#         <!DOCTYPE html>
#         <html lang="en">
#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport"
#                   content="width=device-width, initial-scale=1">
#             <title>{{ room.title }} - Room Finder</title>
#             <style>
#                 body {
#                     font-family: Arial, sans-serif;
#                     background: #f3f5f8;
#                     margin: 0;
#                     padding: 24px;
#                     color: #202938;
#                 }
#                 .container {
#                     max-width: 850px;
#                     margin: auto;
#                     background: white;
#                     padding: 24px;
#                     border-radius: 14px;
#                 }
#                 .gallery {
#                     display: grid;
#                     grid-template-columns:
#                         repeat(auto-fit, minmax(220px, 1fr));
#                     gap: 12px;
#                 }
#                 .gallery img {
#                     width: 100%;
#                     height: 230px;
#                     object-fit: cover;
#                     border-radius: 10px;
#                 }
#                 .rent {
#                     color: #087443;
#                     font-size: 26px;
#                     font-weight: bold;
#                 }
#                 .owner {
#                     background: #f0f5ff;
#                     padding: 18px;
#                     border-radius: 10px;
#                     margin-top: 24px;
#                 }
#                 .contact {
#                     display: inline-block;
#                     background: #1769e0;
#                     color: white;
#                     padding: 11px 16px;
#                     border-radius: 7px;
#                     text-decoration: none;
#                     margin: 5px 5px 5px 0;
#                 }
#                 .back {
#                     display: inline-block;
#                     margin-bottom: 20px;
#                 }
#                 @media (max-width: 600px) {
#                     body { padding: 12px; }
#                     .container { padding: 16px; }
#                 }
#             </style>
#         </head>
#         <body>
#             <main class="container">
#                 <a class="back" href="/browse-rooms">
#                     &larr; Back to rooms
#                 </a>

#                 <h1>{{ room.title }}</h1>

#                 <div class="gallery">
#                     {% for photo in photos %}
#                         <img
#                             src="{{ url_for(
#                                 'uploaded_file',
#                                 filename=photo.photo_path
#                             ) }}"
#                             alt="Room photo">
#                     {% else %}
#                         <p>No photos available for this room.</p>
#                     {% endfor %}
#                 </div>

#                 <p class="rent">Rs {{ room.rent }} / month</p>
#                 <p><b>Room type:</b> {{ room.room_type }}</p>
#                 <p><b>Description:</b>
#                     {{ room.description or 'Not provided' }}</p>
#                 <p><b>Furnished:</b>
#                     {{ 'Yes' if room.furnished else 'No' }}</p>

#                 <h2>Location Details</h2>
#                 <p><b>City:</b> {{ room.city or 'Not provided' }}</p>
#                 <p><b>State:</b> {{ room.state or 'Not provided' }}</p>
#                 <p><b>Colony:</b> {{ room.colony or 'Not provided' }}</p>
#                 <p><b>Address:</b> {{ room.address or 'Not provided' }}</p>
#                 <p><b>Pincode:</b> {{ room.pincode or 'Not provided' }}</p>

#                 <section class="owner">
#                     <h2>Contact Room Owner</h2>
#                     <p><b>Name:</b> {{ room.owner_name }}</p>
#                     <p><b>Email:</b> {{ room.owner_email }}</p>
#                     <p><b>Phone:</b>
#                         {{ room.owner_phone or 'Not provided' }}</p>

#                     {% if room.owner_phone %}
#                         <a class="contact"
#                            href="tel:{{ room.owner_phone }}">
#                             Call Owner
#                         </a>
#                     {% endif %}

#                     <a class="contact"
#                        href="mailto:{{ room.owner_email }}">
#                         Email Owner
#                     </a>
#                 </section>
#             </main>
#         </body>
#         </html>
#         """, room=room, photos=photos)

#     finally:
#         cursor.close()
#         connection.close()

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         email = request.form.get("email", "").strip().lower()
#         password = request.form.get("password", "")

#         if not email or not password:
#             return "Please enter email and password.", 400

#         connection = get_db_connection()
#         cursor = connection.cursor(dictionary=True)

#         try:
#             cursor.execute(
#                 "SELECT user_id, name, email, password, role "
#                 "FROM users WHERE email = %s",
#                 (email,)
#             )
#             user = cursor.fetchone()

#             if not user or not check_password_hash(
#                 user["password"], password
#             ):
#                 return "Invalid email or password.", 401

#             session.clear()
#             session["user_id"] = user["user_id"]
#             session["user_name"] = user["name"]
#             session["user_role"] = user["role"]

#             return redirect(url_for("dashboard"))

#         finally:
#             cursor.close()
#             connection.close()

#     return """
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1">
#         <title>Login - Room Finder</title>
#     </head>
#     <body>
#         <h1>Login to Room Finder</h1>

#         <form method="POST" action="/login">
#             <label>Email</label><br>
#             <input type="email" name="email" required>
#             <br><br>

#             <label>Password</label><br>
#             <input type="password" name="password" required>
#             <br><br>

#             <button type="submit">Login</button>
#         </form>

#         <p>New user? <a href="/register">Create account</a></p>
#         <a href="/">Home</a>
#     </body>
#     </html>
#     """


# @app.route("/dashboard")
# def dashboard():
#     if "user_id" not in session:
#         return redirect(url_for("login"))

#     if session.get("user_role") == "OWNER":
#         return redirect(url_for("owner_dashboard"))

#     return render_template_string("""
#     <!DOCTYPE html><html lang="en"><head>
#       <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
#       <title>Dashboard | Room Finder</title>
#       <style>
#         body{margin:0;background:#f4f7fb;font-family:Arial,sans-serif;color:#17243a}
#         .wrap{max-width:850px;margin:45px auto;padding:24px}
#         .card{background:#fff;border:1px solid #e3e9f2;border-radius:18px;padding:28px;box-shadow:0 10px 30px #1422380d}
#         a{display:inline-block;margin:8px 8px 0 0;padding:12px 16px;border-radius:10px;text-decoration:none;background:#315efb;color:white;font-weight:bold}
#         a.secondary{background:#eaf0ff;color:#2448c7}
#       </style></head><body><main class="wrap"><section class="card">
#       <h1>Welcome, {{ user_name }}!</h1><p>Your account type: <b>{{ role|title }}</b></p>
#       <p>Browse available rooms and find a place that suits your needs.</p>
#       <a href="{{ url_for('browse_rooms') }}">Browse Rooms</a>
#       <a class="secondary" href="{{ url_for('home') }}">Home</a>
#       <a class="secondary" href="{{ url_for('logout') }}">Logout</a>
#       </section></main></body></html>
#     """, user_name=session.get("user_name", "User"), role=session.get("user_role", "TENANT"))


# @app.route("/logout")
# def logout():
#     session.clear()
#     return redirect(url_for("login"))

# # Owner dashboard: only show rooms owned by the logged-in owner.
# @app.route("/owner-dashboard")
# def owner_dashboard():
#     if "user_id" not in session:
#         return redirect(url_for("login"))
#     if session.get("user_role") != "OWNER":
#         return "Only room owners can access this page.", 403

#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)
#     try:
#         cursor.execute("""
#             SELECT r.room_id, r.title, r.description, r.rent,
#                    r.room_type, r.furnished, r.available, r.created_at,
#                    l.city, l.state, l.pincode,
#                    (SELECT rp.photo_path FROM room_photos rp
#                     WHERE rp.room_id = r.room_id
#                     ORDER BY rp.photo_id DESC LIMIT 1) AS cover_photo,
#                    (SELECT COUNT(*) FROM room_photos rp2
#                     WHERE rp2.room_id = r.room_id) AS photo_count
#             FROM rooms r
#             LEFT JOIN locations l ON l.room_id = r.room_id
#             WHERE r.owner_id = %s
#             ORDER BY r.room_id DESC
#         """, (session["user_id"],))
#         rooms = cursor.fetchall()
#         total = len(rooms)
#         available_count = sum(1 for room in rooms if room["available"])
#         unavailable_count = total - available_count
#         return render_template_string(r"""
#         <!DOCTYPE html><html lang="en"><head>
#           <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
#           <title>Owner Dashboard | Room Finder</title>
#           <style>
#             :root{--blue:#315efb;--navy:#17243a;--muted:#6b778b;--line:#e4eaf3;--bg:#f4f7fb}
#             *{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--navy);font-family:Arial,sans-serif}
#             header{background:#fff;border-bottom:1px solid var(--line)}.nav{max-width:1160px;margin:auto;padding:18px 22px;display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap}
#             .brand{font-size:22px;font-weight:800;color:var(--navy);text-decoration:none}.brand span{color:var(--blue)}.nav a.link{color:#42516a;text-decoration:none;margin-left:14px;font-weight:700;font-size:14px}
#             .wrap{max-width:1160px;margin:28px auto;padding:0 22px 50px}.top{display:flex;justify-content:space-between;align-items:center;gap:18px;flex-wrap:wrap;margin-bottom:22px}
#             h1{margin:0 0 8px;font-size:clamp(27px,4vw,36px)}.muted{color:var(--muted);margin:0;line-height:1.6}
#             .btn{display:inline-block;border:0;border-radius:10px;padding:11px 14px;background:var(--blue);color:#fff;text-decoration:none;font-weight:750;font-size:13px;cursor:pointer}.btn.light{background:#eaf0ff;color:#2448c7}.btn.danger{background:#fff0f0;color:#b42318}.btn.gray{background:#edf1f7;color:#344054}
#             .stats{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:20px 0 26px}.stat{background:#fff;border:1px solid var(--line);border-radius:15px;padding:20px}.stat span{display:block;color:var(--muted);font-size:13px;margin-bottom:9px}.stat strong{font-size:28px}
#             .room{display:grid;grid-template-columns:190px 1fr;gap:20px;background:#fff;border:1px solid var(--line);border-radius:17px;padding:16px;margin:14px 0;box-shadow:0 7px 20px #17243a08}.photo{width:100%;height:150px;object-fit:cover;border-radius:11px;background:#eef2f8}.placeholder{height:150px;border-radius:11px;background:#eef2f8;display:grid;place-items:center;color:#78869c;font-size:14px}
#             .roomhead{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;flex-wrap:wrap}.room h2{font-size:20px;margin:2px 0 8px}.rent{font-size:21px;font-weight:800;color:#087443;white-space:nowrap}.details{color:var(--muted);font-size:14px;line-height:1.7;margin:8px 0 14px}.badge{display:inline-block;border-radius:999px;padding:6px 9px;font-size:12px;font-weight:800}.yes{background:#e8f8ee;color:#087443}.no{background:#fff0e8;color:#a54800}.actions{display:flex;gap:8px;flex-wrap:wrap}.actions form{margin:0}.empty{background:#fff;border:1px dashed #cbd5e1;border-radius:16px;padding:34px;text-align:center}
#             @media(max-width:650px){.stats{grid-template-columns:1fr}.room{grid-template-columns:1fr}.photo,.placeholder{height:210px}.nav a.link{margin-left:0;margin-right:12px}}
#           </style></head><body>
#           <header><nav class="nav"><a class="brand" href="/">Room<span>Finder</span></a><div><a class="link" href="/browse-rooms">Browse rooms</a><a class="link" href="/add-room-page">Add room</a><a class="link" href="/upload-photo-page">Upload photo</a><a class="link" href="/logout">Logout</a></div></nav></header>
#           <main class="wrap"><div class="top"><div><h1>Owner Dashboard</h1><p class="muted">Welcome, {{ owner_name }}. Manage the rooms listed from your account.</p></div><a class="btn" href="/add-room-page">＋ Add new room</a></div>
#           <section class="stats"><div class="stat"><span>Total listings</span><strong>{{ total }}</strong></div><div class="stat"><span>Available now</span><strong>{{ available_count }}</strong></div><div class="stat"><span>Marked unavailable</span><strong>{{ unavailable_count }}</strong></div></section>
#           <h2>Your rooms</h2><p class="muted">You can edit a listing, change its availability, or delete it. Deleted listings cannot be restored.</p>
#           {% for room in rooms %}<article class="room"><div>{% if room.cover_photo %}<img class="photo" src="{{ url_for('uploaded_file', filename=room.cover_photo) }}" alt="Room photo">{% else %}<div class="placeholder">No photo yet</div>{% endif %}</div><div><div class="roomhead"><div><h2>{{ room.title }}</h2><span class="badge {{ 'yes' if room.available else 'no' }}">{{ 'Available' if room.available else 'Unavailable' }}</span></div><div class="rent">₹{{ '%.2f'|format(room.rent|float) }}<small style="font-size:12px;color:#6b778b;font-weight:500"> / month</small></div></div>
#           <p class="details"><b>Room type:</b> {{ room.room_type }} · <b>Furnished:</b> {{ 'Yes' if room.furnished else 'No' }}<br><b>Location:</b> {{ room.city or 'City not added' }}, {{ room.state or '' }} {% if room.pincode %}· PIN {{ room.pincode }}{% endif %}<br><b>Photos:</b> {{ room.photo_count }}<br>{{ room.description or 'No description added.' }}</p>
#           <div class="actions"><a class="btn" href="{{ url_for('edit_room', room_id=room.room_id) }}">Edit details</a><a class="btn light" href="{{ url_for('room_details', room_id=room.room_id) }}">View listing</a><a class="btn gray" href="/upload-photo-page?room_id={{ room.room_id }}">Upload photo</a>
#           <form method="post" action="{{ url_for('toggle_room_availability', room_id=room.room_id) }}"><button class="btn light" type="submit">Mark {{ 'unavailable' if room.available else 'available' }}</button></form>
#           <form method="post" action="{{ url_for('delete_room', room_id=room.room_id) }}" onsubmit="return confirm('Delete this room listing permanently?');"><button class="btn danger" type="submit">Delete</button></form></div></div></article>
#           {% else %}<div class="empty"><h3>You haven't listed any rooms yet.</h3><p class="muted">Add your first room and it will appear here.</p><br><a class="btn" href="/add-room-page">Add your first room</a></div>{% endfor %}
#           <p style="margin-top:25px"><a class="btn light" href="/">← Back to home</a></p></main></body></html>
#         """, owner_name=session.get("user_name", "Owner"), rooms=rooms, total=total,
#             available_count=available_count, unavailable_count=unavailable_count)
#     finally:
#         cursor.close()
#         connection.close()


# @app.route("/owner/room/<int:room_id>/edit", methods=["GET", "POST"])
# def edit_room(room_id):
#     if "user_id" not in session:
#         return redirect(url_for("login"))
#     if session.get("user_role") != "OWNER":
#         return "Only room owners can edit listings.", 403

#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)
#     try:
#         cursor.execute("""
#             SELECT r.room_id, r.title, r.description, r.rent, r.room_type,
#                    r.furnished, l.city, l.state, l.colony, l.address, l.pincode
#             FROM rooms r LEFT JOIN locations l ON l.room_id = r.room_id
#             WHERE r.room_id = %s AND r.owner_id = %s
#         """, (room_id, session["user_id"]))
#         room = cursor.fetchone()
#         if room is None:
#             return "Room not found, or it does not belong to your account.", 404

#         if request.method == "POST":
#             title = request.form.get("title", "").strip()
#             description = request.form.get("description", "").strip() or None
#             rent = request.form.get("rent", type=float)
#             room_type = request.form.get("room_type", "").strip()
#             furnished = request.form.get("furnished") == "true"
#             city = request.form.get("city", "").strip()
#             state = request.form.get("state", "").strip()
#             colony = request.form.get("colony", "").strip() or None
#             address = request.form.get("address", "").strip() or None
#             pincode = request.form.get("pincode", "").strip() or None

#             if not title or rent is None or rent < 0 or not room_type or not city or not state:
#                 return "Please enter a title, valid rent, room type, city and state.", 400
#             if pincode and (len(pincode) != 6 or not pincode.isdigit()):
#                 return "PIN code must contain exactly 6 digits.", 400

#             cursor.execute("""
#                 UPDATE rooms SET title=%s, description=%s, rent=%s,
#                     room_type=%s, furnished=%s
#                 WHERE room_id=%s AND owner_id=%s
#             """, (title, description, rent, room_type, furnished, room_id, session["user_id"]))
#             cursor.execute("""
#                 UPDATE locations SET city=%s, state=%s, colony=%s,
#                     address=%s, pincode=%s WHERE room_id=%s
#             """, (city, state, colony, address, pincode, room_id))
#             connection.commit()
#             return redirect(url_for("owner_dashboard"))

#         return render_template_string(r"""
#         <!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Edit room | Room Finder</title>
#         <style>body{margin:0;background:#f4f7fb;font-family:Arial,sans-serif;color:#17243a;padding:24px}.box{max-width:760px;margin:20px auto;background:#fff;padding:28px;border:1px solid #e3e9f2;border-radius:18px}h1{margin-top:0}.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}.field label{display:block;font-weight:700;font-size:14px;margin-bottom:7px}.field input,.field textarea,.field select{width:100%;padding:12px;border:1px solid #ccd5e2;border-radius:9px;font:inherit;box-sizing:border-box}.field.full{grid-column:1/-1}.actions{display:flex;gap:10px;margin-top:20px;flex-wrap:wrap}.btn{padding:12px 16px;border:0;border-radius:9px;background:#315efb;color:white;font-weight:bold;text-decoration:none;cursor:pointer}.btn.alt{background:#eaf0ff;color:#2448c7}@media(max-width:600px){.grid{grid-template-columns:1fr}.field.full{grid-column:auto}.box{padding:18px}}</style></head><body>
#         <main class="box"><h1>Edit room listing</h1><p>Update the details and save your changes.</p><form method="post"><div class="grid">
#         <div class="field full"><label>Room title *</label><input name="title" maxlength="150" required value="{{ room.title }}"></div>
#         <div class="field full"><label>Description</label><textarea name="description" rows="4">{{ room.description or '' }}</textarea></div>
#         <div class="field"><label>Monthly rent (₹) *</label><input type="number" name="rent" min="0" step="0.01" required value="{{ room.rent }}"></div>
#         <div class="field"><label>Room type *</label><input name="room_type" required value="{{ room.room_type }}"></div>
#         <div class="field"><label>City *</label><input name="city" required value="{{ room.city or '' }}"></div>
#         <div class="field"><label>State *</label><input name="state" required value="{{ room.state or '' }}"></div>
#         <div class="field"><label>Colony / area</label><input name="colony" value="{{ room.colony or '' }}"></div>
#         <div class="field"><label>PIN code</label><input name="pincode" pattern="[0-9]{6}" maxlength="6" value="{{ room.pincode or '' }}"></div>
#         <div class="field full"><label>Full address</label><input name="address" value="{{ room.address or '' }}"></div>
#         <div class="field"><label>Furnished?</label><select name="furnished"><option value="false" {{ 'selected' if not room.furnished else '' }}>No</option><option value="true" {{ 'selected' if room.furnished else '' }}>Yes</option></select></div>
#         </div><div class="actions"><button class="btn" type="submit">Save changes</button><a class="btn alt" href="{{ url_for('owner_dashboard') }}">Cancel</a></div></form></main></body></html>
#         """, room=room)
#     except Exception:
#         connection.rollback()
#         app.logger.exception("Room update failed")
#         return "Could not update this room. Check the server log.", 500
#     finally:
#         cursor.close()
#         connection.close()


# @app.route("/owner/room/<int:room_id>/availability", methods=["POST"])
# def toggle_room_availability(room_id):
#     if "user_id" not in session:
#         return redirect(url_for("login"))
#     if session.get("user_role") != "OWNER":
#         return "Only room owners can change availability.", 403
#     connection = get_db_connection()
#     cursor = connection.cursor()
#     try:
#         cursor.execute("""
#             UPDATE rooms SET available = NOT available
#             WHERE room_id = %s AND owner_id = %s
#         """, (room_id, session["user_id"]))
#         if cursor.rowcount == 0:
#             connection.rollback()
#             return "Room not found, or it does not belong to your account.", 404
#         connection.commit()
#         return redirect(url_for("owner_dashboard"))
#     except Exception:
#         connection.rollback()
#         app.logger.exception("Availability update failed")
#         return "Could not update room availability.", 500
#     finally:
#         cursor.close()
#         connection.close()


# @app.route("/owner/room/<int:room_id>/delete", methods=["POST"])
# def delete_room(room_id):
#     if "user_id" not in session:
#         return redirect(url_for("login"))
#     if session.get("user_role") != "OWNER":
#         return "Only room owners can delete listings.", 403
#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)
#     try:
#         cursor.execute("SELECT photo_path FROM room_photos WHERE room_id = %s", (room_id,))
#         photo_paths = [row["photo_path"] for row in cursor.fetchall()]
#         cursor.execute("DELETE FROM rooms WHERE room_id = %s AND owner_id = %s", (room_id, session["user_id"]))
#         if cursor.rowcount == 0:
#             connection.rollback()
#             return "Room not found, or it does not belong to your account.", 404
#         connection.commit()
#         # Remove the associated files after the database delete succeeds.
#         for photo_path in photo_paths:
#             safe_name = os.path.basename(photo_path)
#             file_path = os.path.join(app.config["UPLOAD_FOLDER"], safe_name)
#             if os.path.isfile(file_path):
#                 try:
#                     os.remove(file_path)
#                 except OSError:
#                     app.logger.warning("Could not remove old room photo: %s", safe_name)
#         return redirect(url_for("owner_dashboard"))
#     except Exception:
#         connection.rollback()
#         app.logger.exception("Room deletion failed")
#         return "Could not delete this room. Check the server log.", 500
#     finally:
#         cursor.close()
#         connection.close()


# if __name__ == "__main__":
#     app.run(debug=True)



# from flask import session, redirect, url_for
# from werkzeug.security import generate_password_hash, check_password_hash
# import os
# import uuid
# from flask import (
#     Flask, jsonify, request, send_from_directory,
#     render_template_string
# )
# from werkzeug.utils import secure_filename
# from db import get_db_connection

# app = Flask(__name__)
# app.secret_key = os.environ.get(
#     "FLASK_SECRET_KEY",
#     "dev-only-change-this-secret-before-deployment"
# )
# UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
# ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

# os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# @app.route("/")
# def home():
#     logged_in = "user_id" in session
#     user_name = session.get("user_name", "")
#     user_role = session.get("user_role", "")

#     return render_template_string("""
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1">
#         <title>Room Finder | Find a place to call home</title>
#         <style>
#             :root { --navy: #132238; --blue: #315efb; --muted: #68758a; --bg: #f5f7fb; --line: #e5eaf2; }
#             * { box-sizing: border-box; }
#             body { margin: 0; font-family: Inter, Arial, sans-serif; color: var(--navy); background: var(--bg); }
#             a { text-decoration: none; }
#             .nav { max-width: 1160px; margin: auto; padding: 22px 24px; display: flex; align-items: center; justify-content: space-between; gap: 18px; }
#             .brand { color: var(--navy); font-size: 23px; font-weight: 800; letter-spacing: -.7px; }
#             .brand span { color: var(--blue); }
#             .navlinks { display: flex; align-items: center; flex-wrap: wrap; gap: 18px; }
#             .navlinks a { color: #46546a; font-size: 14px; font-weight: 650; }
#             .navlinks .nav-cta { background: var(--blue); color: white; padding: 11px 16px; border-radius: 11px; }
#             .hero-wrap { padding: 28px 24px 58px; }
#             .hero { max-width: 1112px; margin: auto; min-height: 390px; border-radius: 28px; padding: 56px; color: white; overflow: hidden; position: relative; background: linear-gradient(120deg, #142944 0%, #234d8e 62%, #3979d7 100%); box-shadow: 0 24px 60px rgba(26, 58, 104, .16); }
#             .hero:after { content: ''; position: absolute; width: 360px; height: 360px; border: 1px solid rgba(255,255,255,.17); border-radius: 50%; right: -70px; top: 20px; box-shadow: 0 0 0 36px rgba(255,255,255,.035), 0 0 0 72px rgba(255,255,255,.025); }
#             .eyebrow { display: inline-block; color: #dce7ff; background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.18); border-radius: 999px; padding: 8px 13px; font-size: 12px; font-weight: 750; letter-spacing: .8px; text-transform: uppercase; }
#             h1 { max-width: 610px; margin: 22px 0 15px; font-size: clamp(36px, 5vw, 58px); line-height: 1.05; letter-spacing: -1.8px; }
#             .hero p { max-width: 540px; color: #e0e9f8; line-height: 1.7; font-size: 16px; margin: 0 0 28px; }
#             .actions { display: flex; flex-wrap: wrap; gap: 12px; }
#             .btn { display: inline-flex; justify-content: center; align-items: center; border-radius: 12px; padding: 14px 19px; font-weight: 750; font-size: 14px; }
#             .btn-light { background: white; color: #18345d; }
#             .btn-outline { border: 1px solid rgba(255,255,255,.48); color: white; background: rgba(255,255,255,.07); }
#             .content { max-width: 1112px; margin: 0 auto; padding: 0 24px 58px; }
#             .section-head { display: flex; align-items: end; justify-content: space-between; gap: 16px; margin: 0 0 22px; }
#             .section-head h2 { font-size: 25px; letter-spacing: -.6px; margin: 0 0 7px; }
#             .section-head p { color: var(--muted); margin: 0; font-size: 14px; }
#             .cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
#             .card { background: white; border: 1px solid var(--line); border-radius: 18px; padding: 24px; box-shadow: 0 8px 26px rgba(22, 41, 71, .035); }
#             .icon { width: 44px; height: 44px; border-radius: 13px; display: grid; place-items: center; background: #edf2ff; color: var(--blue); font-size: 21px; margin-bottom: 18px; }
#             .card h3 { margin: 0 0 9px; font-size: 17px; }
#             .card p { margin: 0 0 17px; color: var(--muted); line-height: 1.6; font-size: 14px; }
#             .card a { color: var(--blue); font-weight: 750; font-size: 14px; }
#             .welcome { max-width: 1112px; margin: 0 auto 20px; padding: 0 24px; color: #36516e; font-size: 14px; }
#             footer { border-top: 1px solid var(--line); padding: 22px 24px; text-align: center; color: var(--muted); font-size: 12px; }
#             @media (max-width: 760px) { .nav { align-items: flex-start; flex-direction: column; } .navlinks { gap: 13px; } .hero { padding: 34px 25px; min-height: auto; } .hero:after { right: -230px; opacity: .7; } .cards { grid-template-columns: 1fr; } .section-head { align-items: flex-start; flex-direction: column; } }
#         </style>
#     </head>
#     <body>
#         <header class="nav">
#             <a class="brand" href="/">Room<span>Finder</span></a>
#             <nav class="navlinks">
#                 <a href="/browse-rooms">Browse rooms</a>
#                 {% if logged_in %}
#                     <a href="/dashboard">Dashboard</a>
#                     {% if user_role == 'OWNER' %}<a href="/add-room-page">Add a room</a>{% endif %}
#                     <a class="nav-cta" href="/logout">Logout</a>
#                 {% else %}
#                     <a href="/login">Login</a>
#                     <a class="nav-cta" href="/register">Create account</a>
#                 {% endif %}
#             </nav>
#         </header>

#         {% if logged_in %}<div class="welcome">Welcome back, <strong>{{ user_name }}</strong> · Account type: {{ user_role|title }}</div>{% endif %}

#         <main>
#             <section class="hero-wrap">
#                 <div class="hero">
#                     <span class="eyebrow">A simpler way to find your space</span>
#                     <h1>Find a room that feels like home.</h1>
#                     <p>Explore rooms by city, PIN code and budget. Compare rent, check room photos and contact the owner to take the next step.</p>
#                     <div class="actions">
#                         <a class="btn btn-light" href="/browse-rooms">Explore available rooms &nbsp; →</a>
#                         {% if logged_in and user_role == 'OWNER' %}
#                             <a class="btn btn-outline" href="/add-room-page">List your room</a>
#                         {% elif not logged_in %}
#                             <a class="btn btn-outline" href="/register">Join Room Finder</a>
#                         {% else %}
#                             <a class="btn btn-outline" href="/dashboard">Open dashboard</a>
#                         {% endif %}
#                     </div>
#                 </div>
#             </section>

#             <section class="content">
#                 <div class="section-head">
#                     <div><h2>Everything you need to get started</h2><p>Simple tools for room seekers and property owners.</p></div>
#                 </div>
#                 <div class="cards">
#                     <article class="card">
#                         <div class="icon">⌕</div><h3>Browse rooms</h3>
#                         <p>Search available rooms by city, PIN code and maximum rent, then open a listing to see its details.</p>
#                         <a href="/browse-rooms">Search rooms →</a>
#                     </article>
#                     <article class="card">
#                         <div class="icon">⌂</div><h3>List your room</h3>
#                         <p>Room owners can sign in, add a listing with location details and share photos of the room.</p>
#                         {% if logged_in and user_role == 'OWNER' %}<a href="/add-room-page">Add a room →</a>{% elif not logged_in %}<a href="/register">Create an owner account →</a>{% else %}<a href="/dashboard">Open dashboard →</a>{% endif %}
#                     </article>
#                     <article class="card">
#                         <div class="icon">◎</div><h3>Your account</h3>
#                         <p>Use your dashboard to access account features. Sign in to continue or create an account to get started.</p>
#                         {% if logged_in %}<a href="/dashboard">Go to dashboard →</a>{% else %}<a href="/login">Login or register →</a>{% endif %}
#                     </article>
#                 </div>
#             </section>
#         </main>
#         <footer>Room Finder · Search smarter. Find your space.</footer>
#     </body>
#     </html>
#     """, logged_in=logged_in, user_name=user_name, user_role=user_role)

# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         name = request.form.get("name", "").strip()
#         email = request.form.get("email", "").strip().lower()
#         phone = request.form.get("phone", "").strip()
#         password = request.form.get("password", "")
#         confirm_password = request.form.get("confirm_password", "")
#         role = request.form.get("role", "").upper()

#         if not name or not email or not phone or not password:
#             return "Please fill in all fields.", 400

#         if password != confirm_password:
#             return "Passwords do not match.", 400

#         if len(password) < 8:
#             return "Password must be at least 8 characters.", 400

#         if role not in ("OWNER", "TENANT"):
#             return "Please select a valid role.", 400

#         connection = get_db_connection()
#         cursor = connection.cursor(dictionary=True)

#         try:
#             cursor.execute(
#                 "SELECT user_id FROM users WHERE email = %s",
#                 (email,)
#             )
#             if cursor.fetchone():
#                 return "This email is already registered.", 409

#             hashed_password = generate_password_hash(password)

#             cursor.execute("""
#                 INSERT INTO users (name, email, phone, password, role)
#                 VALUES (%s, %s, %s, %s, %s)
#             """, (name, email, phone, hashed_password, role))

#             connection.commit()

#             return """
#                 <h2>Registration successful!</h2>
#                 <p>Your account has been created.</p>
#                 <a href="/login">Go to Login</a>
#                 <br><br><a href="/">Home</a>
#             """, 201

#         except Exception:
#             connection.rollback()
#             app.logger.exception("Registration failed")
#             return "Registration failed. Please check the server log.", 500

#         finally:
#             cursor.close()
#             connection.close()

#     return """
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1">
#         <title>Register - Room Finder</title>
#     </head>
#     <body>
#         <h1>Create Your Account</h1>

#         <form method="POST" action="/register">
#             <label>Full Name</label><br>
#             <input type="text" name="name" required maxlength="100">
#             <br><br>

#             <label>Email</label><br>
#             <input type="email" name="email" required maxlength="255">
#             <br><br>

#             <label>Phone</label><br>
#             <input type="tel" name="phone" required maxlength="20">
#             <br><br>

#             <label>Password (minimum 8 characters)</label><br>
#             <input type="password" name="password"
#                    minlength="8" required>
#             <br><br>

#             <label>Confirm Password</label><br>
#             <input type="password" name="confirm_password"
#                    minlength="8" required>
#             <br><br>

#             <label>Account Type</label><br>
#             <select name="role" required>
#                 <option value="">Choose account type</option>
#                 <option value="OWNER">Room Owner</option>
#                 <option value="TENANT">Room Seeker (Tenant)</option>
#             </select>
#             <br><br>

#             <button type="submit">Register</button>
#         </form>

#         <p>Already have an account? <a href="/login">Login</a></p>
#         <a href="/">Home</a>
#     </body>
#     </html>
#     """


# # Return available rooms as JSON
# @app.route("/rooms")
# def get_rooms():
#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)

#     try:
#         cursor.execute("""
#             SELECT r.room_id, r.title, r.description,
#                    r.rent, r.room_type, r.furnished,
#                    l.city, l.state, l.colony,
#                    l.address, l.pincode
#             FROM rooms r
#             LEFT JOIN locations l ON r.room_id = l.room_id
#             WHERE r.available = TRUE
#             ORDER BY r.room_id DESC
#         """)
#         rooms = cursor.fetchall()

#         for room in rooms:
#             cursor.execute(
#                 "SELECT photo_path FROM room_photos WHERE room_id = %s",
#                 (room["room_id"],)
#             )
#             photos = cursor.fetchall()
#             room["photos"] = [
#                 f"/uploads/{photo['photo_path']}" for photo in photos
#             ]

#         return jsonify(rooms)
#     finally:
#         cursor.close()
#         connection.close()


# # Display uploaded photos
# @app.route("/uploads/<path:filename>")
# def uploaded_file(filename):
#     return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# # Page to add a room
# @app.route("/add-room-page")
# def add_room_page():
#     if "user_id" not in session:
#         return redirect(url_for("login"))

#     if session.get("user_role") != "OWNER":
#         return "Only room owners can access this page.", 403

#     return """
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <title>Add Room</title>
#         <meta name="viewport" content="width=device-width, initial-scale=1">
#     </head>
#     <body>
#         <h2>Add New Room</h2>
#         <form action="/add-room" method="POST">
#             Room Title:
#             <input type="text" name="title" required>
#             <br><br>

#             Description:
#             <input type="text" name="description">
#             <br><br>

#             Monthly Rent (Rs):
#             <input type="number" name="rent" min="0" required>
#             <br><br>

#             Room Type:
#             <input type="text" name="room_type"
#                    placeholder="Single room, flat, PG" required>
#             <br><br>

#             City:
#             <input type="text" name="city" required>
#             <br><br>

#             State:
#             <input type="text" name="state" required>
#             <br><br>

#             Colony:
#             <input type="text" name="colony">
#             <br><br>

#             Full Address:
#             <input type="text" name="address">
#             <br><br>

#             Pincode:
#             <input type="text" name="pincode"
#                    pattern="[0-9]{6}"
#                    title="Enter a 6-digit pincode">
#             <br><br>
#             Nearby College / University:
# <input
#     type="text"
#     name="nearby_college"
#     placeholder="Enter nearby college name"
# >
# <br><br>

# Nearby Office / Company:
# <input
#     type="text"
#     name="nearby_office"
#     placeholder="Enter nearby office name"
# >
# <br><br>

#             Furnished:
#             <input type="checkbox" name="furnished" value="true">
#             <br><br>

#             <button type="submit">Add Room</button>
#         </form>

#         <br><a href="/browse-rooms">Browse Rooms</a>
#     </body>
#     </html>
#     """


# # Save room and its location in MySQL
# @app.route("/add-room", methods=["POST"])
# def add_room():
#     if "user_id" not in session:
#         return redirect(url_for("login"))

#     if session.get("user_role") != "OWNER":
#         return "Only room owners can add rooms.", 403

#     owner_id = session["user_id"]
#     title = request.form.get("title", "").strip()
#     description = request.form.get("description", "").strip() or None
#     rent = request.form.get("rent", type=float)
#     room_type = request.form.get("room_type", "").strip()
#     furnished = request.form.get("furnished") == "true"

#     city = request.form.get("city", "").strip()
#     state = request.form.get("state", "").strip()
#     colony = request.form.get("colony", "").strip() or None
#     address = request.form.get("address", "").strip() or None
#     pincode = request.form.get("pincode", "").strip() or None

#     nearby_college = request.form.get(
#     "nearby_college", ""
#     ).strip() or None

#     nearby_office = request.form.get(
#     "nearby_office", ""
#     ).strip() or None

#     if not owner_id or not title or rent is None or rent < 0:
#         return "Please enter a valid owner, title and rent.", 400

#     if not room_type or not city or not state:
#         return "Room type, city and state are required.", 400

#     if pincode and (
#         len(pincode) != 6 or not pincode.isdigit()
#     ):
#         return "Pincode must contain exactly 6 digits.", 400

#     connection = get_db_connection()
#     cursor = connection.cursor()

#     try:
#         cursor.execute("""
#             INSERT INTO rooms
#                 (owner_id, title, description, rent,
#                  room_type, furnished)
#             VALUES (%s, %s, %s, %s, %s, %s)
#         """, (
#             owner_id, title, description, rent,
#             room_type, furnished
#         ))

#         room_id = cursor.lastrowid

#        cursor.execute("""
#     INSERT INTO locations
#         (
#             room_id,
#             city,
#             state,
#             colony,
#             address,
#             pincode,
#             nearby_college,
#             nearby_office
#         )
#     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
# """, (
#     room_id,
#     city,
#     state,
#     colony,
#     address,
#     pincode,
#     nearby_college,
#     nearby_office
# ))

#         connection.commit()

#         return f"""
#         <!DOCTYPE html>
#         <html>
#         <body>
#             <h2>Room added successfully!</h2>
#             <p>Your Room ID is: {room_id}</p>
#             <p>Remember this ID to upload its photo.</p>
#             <a href="/upload-photo-page">Upload Room Photo</a><br><br>
#             <a href="/browse-rooms">Browse Rooms</a><br><br>
#             <a href="/">Home</a>
#         </body>
#         </html>
#         """, 201

#     except Exception as error:
#         connection.rollback()
#         app.logger.exception("Unable to add room")
#         return f"Database error: {error}", 400

#     finally:
#         cursor.close()
#         connection.close()


# # Page to upload a room photo
# @app.route("/upload-photo-page")
# def upload_photo_page():
#     if "user_id" not in session:
#         return redirect(url_for("login"))

#     if session.get("user_role") != "OWNER":
#         return "Only room owners can upload room photos.", 403

#     return """
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <title>Upload Room Photo</title>
#     </head>
#     <body>
#         <h2>Upload Room Photo</h2>
#         <form action="/upload-photo" method="POST"
#               enctype="multipart/form-data">
#             Room ID:
#             <input type="number" name="room_id" min="1" required>
#             <br><br>

#             Select Photo:
#             <input type="file" name="photo"
#                    accept=".jpg,.jpeg,.png,.webp" required>
#             <br><br>

#             <button type="submit">Upload Photo</button>
#         </form>
#         <p>Allowed formats: JPG, JPEG, PNG, WEBP. Maximum size: 5 MB.</p>
#         <a href="/browse-rooms">Browse Rooms</a>
#     </body>
#     </html>
#     """


# # Save photo to uploads folder and filename to MySQL
# @app.route("/upload-photo", methods=["POST"])
# def upload_photo():
#     if "user_id" not in session:
#         return redirect(url_for("login"))

#     if session.get("user_role") != "OWNER":
#         return "Only room owners can upload room photos.", 403

#     room_id = request.form.get("room_id", type=int)
#     photo = request.files.get("photo")

#     if not room_id or not photo or not photo.filename:
#         return "Please provide a valid Room ID and photo.", 400

#     original_name = secure_filename(photo.filename)

#     if "." not in original_name:
#         return "Invalid photo filename.", 400

#     extension = original_name.rsplit(".", 1)[1].lower()

#     if extension not in ALLOWED_EXTENSIONS:
#         return "Only JPG, JPEG, PNG and WEBP images are allowed.", 400

#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)
#     saved_path = None

#     try:
#         cursor.execute(
#             "SELECT room_id FROM rooms WHERE room_id = %s AND owner_id = %s",
#             (room_id, session["user_id"])
#         )

#         if cursor.fetchone() is None:
#             return "Room not found, or this room does not belong to your account.", 404

#         filename = f"{uuid.uuid4().hex}.{extension}"
#         saved_path = os.path.join(
#             app.config["UPLOAD_FOLDER"], filename
#         )

#         photo.save(saved_path)

#         cursor.execute("""
#             INSERT INTO room_photos (room_id, photo_path)
#             VALUES (%s, %s)
#         """, (room_id, filename))

#         connection.commit()

#         return f"""
#         <!DOCTYPE html>
#         <html>
#         <body>
#             <h2>Photo uploaded successfully!</h2>
#             <img src="/uploads/{filename}"
#                  width="350" alt="Uploaded room photo">
#             <br><br>
#             <a href="/browse-rooms">Browse Rooms</a><br><br>
#             <a href="/upload-photo-page">Upload Another Photo</a>
#         </body>
#         </html>
#         """

#     except Exception as error:
#         connection.rollback()

#         if saved_path and os.path.exists(saved_path):
#             os.remove(saved_path)

#         app.logger.exception("Photo upload failed")
#         return f"Photo upload failed: {error}", 400

#     finally:
#         cursor.close()
#         connection.close()


# # Browse rooms with advanced search filters
# @app.route("/browse-rooms")
# def browse_rooms():
#     city = request.args.get("city", "").strip()
#     pincode = request.args.get("pincode", "").strip()
#     min_rent_text = request.args.get("min_rent", "").strip()
#     max_rent_text = request.args.get("max_rent", "").strip()
#     room_type = request.args.get("room_type", "").strip()
#     furnished = request.args.get("furnished", "").strip().lower()
#     availability = request.args.get("availability", "available").strip().lower()

#     if pincode and (len(pincode) != 6 or not pincode.isdigit()):
#         return "Pincode must contain exactly 6 digits.", 400

#     if furnished not in ("", "yes", "no"):
#         return "Please choose a valid furnishing filter.", 400

#     if availability not in ("available", "all"):
#         return "Please choose a valid availability filter.", 400

#     min_rent = None
#     max_rent = None
#     try:
#         if min_rent_text:
#             min_rent = float(min_rent_text)
#             if min_rent < 0:
#                 return "Minimum rent cannot be negative.", 400
#         if max_rent_text:
#             max_rent = float(max_rent_text)
#             if max_rent < 0:
#                 return "Maximum rent cannot be negative.", 400
#     except ValueError:
#         return "Please enter a valid rent amount.", 400

#     if min_rent is not None and max_rent is not None and min_rent > max_rent:
#         return "Minimum rent cannot be greater than maximum rent.", 400

#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)

#     try:
#         query = """
#             SELECT
#                 r.room_id,
#                 r.title,
#                 r.description,
#                 r.rent,
#                 r.room_type,
#                 r.furnished,
#                 r.available,
#                 l.city,
#                 l.state,
#                 l.colony,
#                 l.address,
#                 l.pincode,
#                 (
#                     SELECT rp.photo_path
#                     FROM room_photos rp
#                     WHERE rp.room_id = r.room_id
#                     ORDER BY rp.photo_id DESC
#                     LIMIT 1
#                 ) AS photo_path
#             FROM rooms r
#             LEFT JOIN locations l ON l.room_id = r.room_id
#             WHERE 1=1
#         """
#         conditions = []
#         values = []

#         if availability == "available":
#             conditions.append("r.available = TRUE")
#         if city:
#             conditions.append("l.city LIKE %s")
#             values.append(f"%{city}%")
#         if pincode:
#             conditions.append("l.pincode = %s")
#             values.append(pincode)
#         if min_rent is not None:
#             conditions.append("r.rent >= %s")
#             values.append(min_rent)
#         if max_rent is not None:
#             conditions.append("r.rent <= %s")
#             values.append(max_rent)
#         if room_type:
#             conditions.append("r.room_type LIKE %s")
#             values.append(f"%{room_type}%")
#         if furnished == "yes":
#             conditions.append("r.furnished = TRUE")
#         elif furnished == "no":
#             conditions.append("r.furnished = FALSE")

#         if conditions:
#             query += " AND " + " AND ".join(conditions)
#         query += " ORDER BY r.room_id DESC"

#         cursor.execute(query, tuple(values))
#         rooms = cursor.fetchall()

#         return render_template_string("""
#         <!DOCTYPE html>
#         <html lang="en">
#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport" content="width=device-width, initial-scale=1">
#             <title>Browse Rooms | Room Finder</title>
#             <style>
#                 :root { --ink:#17263c; --muted:#68778b; --blue:#315efb; --line:#e3e9f2; --bg:#f5f7fb; }
#                 * { box-sizing:border-box; }
#                 body { margin:0; padding:24px; background:var(--bg); color:var(--ink); font-family:Arial,sans-serif; }
#                 .wrap { max-width:1180px; margin:auto; }
#                 header { display:flex; justify-content:space-between; align-items:center; gap:16px; flex-wrap:wrap; margin:0 0 24px; }
#                 .brand { font-size:23px; font-weight:800; color:var(--ink); text-decoration:none; }
#                 .brand span { color:var(--blue); }
#                 nav { display:flex; gap:16px; flex-wrap:wrap; }
#                 nav a { color:#40516a; text-decoration:none; font-size:14px; font-weight:700; }
#                 .intro { background:linear-gradient(120deg,#142944,#315fba); color:white; padding:30px; border-radius:22px; }
#                 .intro h1 { margin:0 0 8px; font-size:clamp(28px,4vw,40px); }
#                 .intro p { margin:0; color:#e0eaff; line-height:1.6; }
#                 .filters { background:white; border:1px solid var(--line); border-radius:18px; padding:20px; margin:20px 0; box-shadow:0 8px 24px #1a2b4808; }
#                 .filters h2 { margin:0 0 16px; font-size:18px; }
#                 .filter-grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:14px; }
#                 label { display:block; font-size:13px; font-weight:700; margin-bottom:7px; }
#                 input, select { width:100%; min-width:0; padding:11px 12px; border:1px solid #ccd5e2; border-radius:9px; font-size:14px; background:white; color:var(--ink); }
#                 .filter-actions { display:flex; align-items:center; flex-wrap:wrap; gap:12px; margin-top:17px; }
#                 .btn { border:0; border-radius:10px; background:var(--blue); color:white; padding:12px 17px; font-weight:750; text-decoration:none; cursor:pointer; }
#                 .clear { color:var(--blue); font-size:14px; font-weight:700; text-decoration:none; }
#                 .count { color:var(--muted); margin:24px 0 14px; font-size:14px; }
#                 .rooms { display:grid; grid-template-columns:repeat(auto-fit,minmax(255px,1fr)); gap:18px; }
#                 .card { background:white; border:1px solid var(--line); border-radius:17px; padding:14px; overflow:hidden; box-shadow:0 6px 22px #1a2b4808; }
#                 .card img, .no-photo { width:100%; height:190px; object-fit:cover; border-radius:11px; background:#edf1f7; }
#                 .no-photo { display:grid; place-items:center; color:var(--muted); }
#                 .card h2 { font-size:19px; margin:15px 0 8px; overflow-wrap:anywhere; }
#                 .rent { color:#087443; font-size:22px; font-weight:800; margin:0 0 12px; }
#                 .meta { color:#56657a; font-size:14px; line-height:1.55; overflow-wrap:anywhere; }
#                 .status { display:inline-block; padding:5px 9px; border-radius:999px; background:#e7f8ee; color:#137342; font-size:12px; font-weight:800; }
#                 .status.off { background:#fff0e8; color:#a34a12; }
#                 .details { display:inline-block; margin-top:8px; background:var(--blue); color:white; padding:10px 13px; border-radius:9px; text-decoration:none; font-weight:750; font-size:14px; }
#                 .empty { background:white; padding:28px; border-radius:16px; grid-column:1/-1; }
#                 @media(max-width:850px) { .filter-grid { grid-template-columns:repeat(2,minmax(0,1fr)); } }
#                 @media(max-width:520px) { body { padding:14px; } .intro { padding:23px; } .filter-grid { grid-template-columns:1fr; } }
#             </style>
#         </head>
#         <body>
#         <div class="wrap">
#             <header>
#                 <a class="brand" href="/">Room<span>Finder</span></a>
#                 <nav><a href="/">Home</a><a href="/dashboard">Dashboard</a><a href="/logout">Logout</a></nav>
#             </header>
#             <section class="intro">
#                 <h1>Find a room that fits your life.</h1>
#                 <p>Filter by location, monthly budget, room type and furnishing to find a suitable place.</p>
#             </section>
#             <form class="filters" action="/browse-rooms" method="GET">
#                 <h2>Refine your search</h2>
#                 <div class="filter-grid">
#                     <div><label for="city">City</label><input id="city" name="city" type="text" placeholder="e.g. Indore" value="{{ city }}"></div>
#                     <div><label for="pincode">PIN code</label><input id="pincode" name="pincode" type="text" inputmode="numeric" pattern="[0-9]{6}" maxlength="6" placeholder="6-digit PIN code" value="{{ pincode }}"></div>
#                     <div><label for="min_rent">Minimum monthly rent (₹)</label><input id="min_rent" name="min_rent" type="number" min="0" step="any" placeholder="e.g. 3000" value="{{ min_rent_text }}"></div>
#                     <div><label for="max_rent">Maximum monthly rent (₹)</label><input id="max_rent" name="max_rent" type="number" min="0" step="any" placeholder="e.g. 8000" value="{{ max_rent_text }}"></div>
#                     <div><label for="room_type">Room type</label><input id="room_type" name="room_type" type="text" placeholder="e.g. Single, Shared, 1BHK" value="{{ room_type }}"></div>
#                     <div><label for="furnished">Furnishing</label><select id="furnished" name="furnished"><option value="" {{ 'selected' if not furnished else '' }}>Any</option><option value="yes" {{ 'selected' if furnished == 'yes' else '' }}>Furnished</option><option value="no" {{ 'selected' if furnished == 'no' else '' }}>Unfurnished</option></select></div>
#                     <div><label for="availability">Availability</label><select id="availability" name="availability"><option value="available" {{ 'selected' if availability == 'available' else '' }}>Available only</option><option value="all" {{ 'selected' if availability == 'all' else '' }}>All listings</option></select></div>
#                 </div>
#                 <div class="filter-actions"><button class="btn" type="submit">Search rooms</button><a class="clear" href="/browse-rooms">Clear all filters</a></div>
#             </form>
#             <p class="count">Found <strong>{{ rooms|length }}</strong> room(s) matching your filters.</p>
#             <section class="rooms">
#                 {% for room in rooms %}
#                 <article class="card">
#                     {% if room.photo_path %}<img src="{{ url_for('uploaded_file', filename=room.photo_path) }}" alt="Photo of {{ room.title }}">{% else %}<div class="no-photo">No photo uploaded yet</div>{% endif %}
#                     <h2>{{ room.title }}</h2>
#                     <p class="rent">₹{{ room.rent }} <span style="font-size:13px;font-weight:500;color:#68778b">/ month</span></p>
#                     <span class="status {{ 'off' if not room.available else '' }}">{{ 'Available' if room.available else 'Unavailable' }}</span>
#                     <p class="meta"><b>Room type:</b> {{ room.room_type or 'Not specified' }}<br><b>Furnished:</b> {{ 'Yes' if room.furnished else 'No' }}<br><b>City:</b> {{ room.city or 'Not provided' }}<br><b>State:</b> {{ room.state or 'Not provided' }}<br><b>Colony:</b> {{ room.colony or 'Not provided' }}<br><b>PIN code:</b> {{ room.pincode or 'Not provided' }}</p>
#                     {% if room.description %}<p class="meta">{{ room.description }}</p>{% endif %}
#                     <a class="details" href="{{ url_for('room_details', room_id=room.room_id) }}">View details →</a>
#                 </article>
#                 {% else %}
#                 <div class="empty"><h2>No rooms found</h2><p>Try increasing your budget or removing one or more filters.</p><a class="details" href="/browse-rooms">Clear filters</a></div>
#                 {% endfor %}
#             </section>
#         </div>
#         </body>
#         </html>
#         """, rooms=rooms, city=city, pincode=pincode,
#             min_rent_text=min_rent_text, max_rent_text=max_rent_text,
#             room_type=room_type, furnished=furnished, availability=availability)
#     finally:
#         cursor.close()
#         connection.close()


# @app.errorhandler(413)
# def file_too_large(error):
#     return "Photo size must be 5 MB or less.", 413

# @app.route("/room/<int:room_id>")
# def room_details(room_id):
#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)

#     try:
#         cursor.execute("""
#             SELECT
#                 r.room_id,
#                 r.owner_id,
#                 r.title,
#                 r.description,
#                 r.rent,
#                 r.room_type,
#                 r.furnished,
#                 l.city,
#                 l.state,
#                 l.colony,
#                 l.address,
#                 l.pincode,
#                 u.name AS owner_name,
#                 u.email AS owner_email,
#                 u.phone AS owner_phone
#             FROM rooms r
#             LEFT JOIN locations l
#                 ON r.room_id = l.room_id
#             LEFT JOIN users u
#                 ON r.owner_id = u.user_id
#             WHERE r.room_id = %s
#               AND r.available = TRUE
#         """, (room_id,))

#         room = cursor.fetchone()

#         if room is None:
#             return "Room not found or no longer available.", 404

#         cursor.execute("""
#             SELECT photo_path
#             FROM room_photos
#             WHERE room_id = %s
#             ORDER BY photo_id DESC
#         """, (room_id,))

#         photos = cursor.fetchall()

#         return render_template_string("""
#         <!DOCTYPE html>
#         <html lang="en">
#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport"
#                   content="width=device-width, initial-scale=1">
#             <title>{{ room.title }} - Room Finder</title>
#             <style>
#                 body {
#                     font-family: Arial, sans-serif;
#                     background: #f3f5f8;
#                     margin: 0;
#                     padding: 24px;
#                     color: #202938;
#                 }
#                 .container {
#                     max-width: 850px;
#                     margin: auto;
#                     background: white;
#                     padding: 24px;
#                     border-radius: 14px;
#                 }
#                 .gallery {
#                     display: grid;
#                     grid-template-columns:
#                         repeat(auto-fit, minmax(220px, 1fr));
#                     gap: 12px;
#                 }
#                 .gallery img {
#                     width: 100%;
#                     height: 230px;
#                     object-fit: cover;
#                     border-radius: 10px;
#                 }
#                 .rent {
#                     color: #087443;
#                     font-size: 26px;
#                     font-weight: bold;
#                 }
#                 .owner {
#                     background: #f0f5ff;
#                     padding: 18px;
#                     border-radius: 10px;
#                     margin-top: 24px;
#                 }
#                 .contact {
#                     display: inline-block;
#                     background: #1769e0;
#                     color: white;
#                     padding: 11px 16px;
#                     border-radius: 7px;
#                     text-decoration: none;
#                     margin: 5px 5px 5px 0;
#                 }
#                 .back {
#                     display: inline-block;
#                     margin-bottom: 20px;
#                 }
#                 @media (max-width: 600px) {
#                     body { padding: 12px; }
#                     .container { padding: 16px; }
#                 }
#             </style>
#         </head>
#         <body>
#             <main class="container">
#                 <a class="back" href="/browse-rooms">
#                     &larr; Back to rooms
#                 </a>

#                 <h1>{{ room.title }}</h1>

#                 <div class="gallery">
#                     {% for photo in photos %}
#                         <img
#                             src="{{ url_for(
#                                 'uploaded_file',
#                                 filename=photo.photo_path
#                             ) }}"
#                             alt="Room photo">
#                     {% else %}
#                         <p>No photos available for this room.</p>
#                     {% endfor %}
#                 </div>

#                 <p class="rent">Rs {{ room.rent }} / month</p>
#                 <p><b>Room type:</b> {{ room.room_type }}</p>
#                 <p><b>Description:</b>
#                     {{ room.description or 'Not provided' }}</p>
#                 <p><b>Furnished:</b>
#                     {{ 'Yes' if room.furnished else 'No' }}</p>

#                 <h2>Location Details</h2>
#                 <p><b>City:</b> {{ room.city or 'Not provided' }}</p>
#                 <p><b>State:</b> {{ room.state or 'Not provided' }}</p>
#                 <p><b>Colony:</b> {{ room.colony or 'Not provided' }}</p>
#                 <p><b>Address:</b> {{ room.address or 'Not provided' }}</p>
#                 <p><b>Pincode:</b> {{ room.pincode or 'Not provided' }}</p>

#                 <section class="owner">
#                     <h2>Contact Room Owner</h2>
#                     <p><b>Name:</b> {{ room.owner_name }}</p>
#                     <p><b>Email:</b> {{ room.owner_email }}</p>
#                     <p><b>Phone:</b>
#                         {{ room.owner_phone or 'Not provided' }}</p>

#                     {% if room.owner_phone %}
#                         <a class="contact"
#                            href="tel:{{ room.owner_phone }}">
#                             Call Owner
#                         </a>
#                     {% endif %}

#                     <a class="contact"
#                        href="mailto:{{ room.owner_email }}">
#                         Email Owner
#                     </a>
#                 </section>
#             </main>
#         </body>
#         </html>
#         """, room=room, photos=photos)

#     finally:
#         cursor.close()
#         connection.close()

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         email = request.form.get("email", "").strip().lower()
#         password = request.form.get("password", "")

#         if not email or not password:
#             return "Please enter email and password.", 400

#         connection = get_db_connection()
#         cursor = connection.cursor(dictionary=True)

#         try:
#             cursor.execute(
#                 "SELECT user_id, name, email, password, role "
#                 "FROM users WHERE email = %s",
#                 (email,)
#             )
#             user = cursor.fetchone()

#             if not user or not check_password_hash(
#                 user["password"], password
#             ):
#                 return "Invalid email or password.", 401

#             session.clear()
#             session["user_id"] = user["user_id"]
#             session["user_name"] = user["name"]
#             session["user_role"] = user["role"]

#             return redirect(url_for("dashboard"))

#         finally:
#             cursor.close()
#             connection.close()

#     return """
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1">
#         <title>Login - Room Finder</title>
#     </head>
#     <body>
#         <h1>Login to Room Finder</h1>

#         <form method="POST" action="/login">
#             <label>Email</label><br>
#             <input type="email" name="email" required>
#             <br><br>

#             <label>Password</label><br>
#             <input type="password" name="password" required>
#             <br><br>

#             <button type="submit">Login</button>
#         </form>

#         <p>New user? <a href="/register">Create account</a></p>
#         <a href="/">Home</a>
#     </body>
#     </html>
#     """


# @app.route("/dashboard")
# def dashboard():
#     if "user_id" not in session:
#         return redirect(url_for("login"))

#     if session.get("user_role") == "OWNER":
#         return redirect(url_for("owner_dashboard"))

#     return render_template_string("""
#     <!DOCTYPE html><html lang="en"><head>
#       <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
#       <title>Dashboard | Room Finder</title>
#       <style>
#         body{margin:0;background:#f4f7fb;font-family:Arial,sans-serif;color:#17243a}
#         .wrap{max-width:850px;margin:45px auto;padding:24px}
#         .card{background:#fff;border:1px solid #e3e9f2;border-radius:18px;padding:28px;box-shadow:0 10px 30px #1422380d}
#         a{display:inline-block;margin:8px 8px 0 0;padding:12px 16px;border-radius:10px;text-decoration:none;background:#315efb;color:white;font-weight:bold}
#         a.secondary{background:#eaf0ff;color:#2448c7}
#       </style></head><body><main class="wrap"><section class="card">
#       <h1>Welcome, {{ user_name }}!</h1><p>Your account type: <b>{{ role|title }}</b></p>
#       <p>Browse available rooms and find a place that suits your needs.</p>
#       <a href="{{ url_for('browse_rooms') }}">Browse Rooms</a>
#       <a class="secondary" href="{{ url_for('home') }}">Home</a>
#       <a class="secondary" href="{{ url_for('logout') }}">Logout</a>
#       </section></main></body></html>
#     """, user_name=session.get("user_name", "User"), role=session.get("user_role", "TENANT"))


# @app.route("/logout")
# def logout():
#     session.clear()
#     return redirect(url_for("login"))

# # Owner dashboard: only show rooms owned by the logged-in owner.
# @app.route("/owner-dashboard")
# def owner_dashboard():
#     if "user_id" not in session:
#         return redirect(url_for("login"))
#     if session.get("user_role") != "OWNER":
#         return "Only room owners can access this page.", 403

#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)
#     try:
#         cursor.execute("""
#             SELECT r.room_id, r.title, r.description, r.rent,
#                    r.room_type, r.furnished, r.available, r.created_at,
#                    l.city, l.state, l.pincode,
#                    (SELECT rp.photo_path FROM room_photos rp
#                     WHERE rp.room_id = r.room_id
#                     ORDER BY rp.photo_id DESC LIMIT 1) AS cover_photo,
#                    (SELECT COUNT(*) FROM room_photos rp2
#                     WHERE rp2.room_id = r.room_id) AS photo_count
#             FROM rooms r
#             LEFT JOIN locations l ON l.room_id = r.room_id
#             WHERE r.owner_id = %s
#             ORDER BY r.room_id DESC
#         """, (session["user_id"],))
#         rooms = cursor.fetchall()
#         total = len(rooms)
#         available_count = sum(1 for room in rooms if room["available"])
#         unavailable_count = total - available_count
#         return render_template_string(r"""
#         <!DOCTYPE html><html lang="en"><head>
#           <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
#           <title>Owner Dashboard | Room Finder</title>
#           <style>
#             :root{--blue:#315efb;--navy:#17243a;--muted:#6b778b;--line:#e4eaf3;--bg:#f4f7fb}
#             *{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--navy);font-family:Arial,sans-serif}
#             header{background:#fff;border-bottom:1px solid var(--line)}.nav{max-width:1160px;margin:auto;padding:18px 22px;display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap}
#             .brand{font-size:22px;font-weight:800;color:var(--navy);text-decoration:none}.brand span{color:var(--blue)}.nav a.link{color:#42516a;text-decoration:none;margin-left:14px;font-weight:700;font-size:14px}
#             .wrap{max-width:1160px;margin:28px auto;padding:0 22px 50px}.top{display:flex;justify-content:space-between;align-items:center;gap:18px;flex-wrap:wrap;margin-bottom:22px}
#             h1{margin:0 0 8px;font-size:clamp(27px,4vw,36px)}.muted{color:var(--muted);margin:0;line-height:1.6}
#             .btn{display:inline-block;border:0;border-radius:10px;padding:11px 14px;background:var(--blue);color:#fff;text-decoration:none;font-weight:750;font-size:13px;cursor:pointer}.btn.light{background:#eaf0ff;color:#2448c7}.btn.danger{background:#fff0f0;color:#b42318}.btn.gray{background:#edf1f7;color:#344054}
#             .stats{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:20px 0 26px}.stat{background:#fff;border:1px solid var(--line);border-radius:15px;padding:20px}.stat span{display:block;color:var(--muted);font-size:13px;margin-bottom:9px}.stat strong{font-size:28px}
#             .room{display:grid;grid-template-columns:190px 1fr;gap:20px;background:#fff;border:1px solid var(--line);border-radius:17px;padding:16px;margin:14px 0;box-shadow:0 7px 20px #17243a08}.photo{width:100%;height:150px;object-fit:cover;border-radius:11px;background:#eef2f8}.placeholder{height:150px;border-radius:11px;background:#eef2f8;display:grid;place-items:center;color:#78869c;font-size:14px}
#             .roomhead{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;flex-wrap:wrap}.room h2{font-size:20px;margin:2px 0 8px}.rent{font-size:21px;font-weight:800;color:#087443;white-space:nowrap}.details{color:var(--muted);font-size:14px;line-height:1.7;margin:8px 0 14px}.badge{display:inline-block;border-radius:999px;padding:6px 9px;font-size:12px;font-weight:800}.yes{background:#e8f8ee;color:#087443}.no{background:#fff0e8;color:#a54800}.actions{display:flex;gap:8px;flex-wrap:wrap}.actions form{margin:0}.empty{background:#fff;border:1px dashed #cbd5e1;border-radius:16px;padding:34px;text-align:center}
#             @media(max-width:650px){.stats{grid-template-columns:1fr}.room{grid-template-columns:1fr}.photo,.placeholder{height:210px}.nav a.link{margin-left:0;margin-right:12px}}
#           </style></head><body>
#           <header><nav class="nav"><a class="brand" href="/">Room<span>Finder</span></a><div><a class="link" href="/browse-rooms">Browse rooms</a><a class="link" href="/add-room-page">Add room</a><a class="link" href="/upload-photo-page">Upload photo</a><a class="link" href="/logout">Logout</a></div></nav></header>
#           <main class="wrap"><div class="top"><div><h1>Owner Dashboard</h1><p class="muted">Welcome, {{ owner_name }}. Manage the rooms listed from your account.</p></div><a class="btn" href="/add-room-page">＋ Add new room</a></div>
#           <section class="stats"><div class="stat"><span>Total listings</span><strong>{{ total }}</strong></div><div class="stat"><span>Available now</span><strong>{{ available_count }}</strong></div><div class="stat"><span>Marked unavailable</span><strong>{{ unavailable_count }}</strong></div></section>
#           <h2>Your rooms</h2><p class="muted">You can edit a listing, change its availability, or delete it. Deleted listings cannot be restored.</p>
#           {% for room in rooms %}<article class="room"><div>{% if room.cover_photo %}<img class="photo" src="{{ url_for('uploaded_file', filename=room.cover_photo) }}" alt="Room photo">{% else %}<div class="placeholder">No photo yet</div>{% endif %}</div><div><div class="roomhead"><div><h2>{{ room.title }}</h2><span class="badge {{ 'yes' if room.available else 'no' }}">{{ 'Available' if room.available else 'Unavailable' }}</span></div><div class="rent">₹{{ '%.2f'|format(room.rent|float) }}<small style="font-size:12px;color:#6b778b;font-weight:500"> / month</small></div></div>
#           <p class="details"><b>Room type:</b> {{ room.room_type }} · <b>Furnished:</b> {{ 'Yes' if room.furnished else 'No' }}<br><b>Location:</b> {{ room.city or 'City not added' }}, {{ room.state or '' }} {% if room.pincode %}· PIN {{ room.pincode }}{% endif %}<br><b>Photos:</b> {{ room.photo_count }}<br>{{ room.description or 'No description added.' }}</p>
#           <div class="actions"><a class="btn" href="{{ url_for('edit_room', room_id=room.room_id) }}">Edit details</a><a class="btn light" href="{{ url_for('room_details', room_id=room.room_id) }}">View listing</a><a class="btn gray" href="/upload-photo-page?room_id={{ room.room_id }}">Upload photo</a>
#           <form method="post" action="{{ url_for('toggle_room_availability', room_id=room.room_id) }}"><button class="btn light" type="submit">Mark {{ 'unavailable' if room.available else 'available' }}</button></form>
#           <form method="post" action="{{ url_for('delete_room', room_id=room.room_id) }}" onsubmit="return confirm('Delete this room listing permanently?');"><button class="btn danger" type="submit">Delete</button></form></div></div></article>
#           {% else %}<div class="empty"><h3>You haven't listed any rooms yet.</h3><p class="muted">Add your first room and it will appear here.</p><br><a class="btn" href="/add-room-page">Add your first room</a></div>{% endfor %}
#           <p style="margin-top:25px"><a class="btn light" href="/">← Back to home</a></p></main></body></html>
#         """, owner_name=session.get("user_name", "Owner"), rooms=rooms, total=total,
#             available_count=available_count, unavailable_count=unavailable_count)
#     finally:
#         cursor.close()
#         connection.close()


# @app.route("/owner/room/<int:room_id>/edit", methods=["GET", "POST"])
# def edit_room(room_id):
#     if "user_id" not in session:
#         return redirect(url_for("login"))
#     if session.get("user_role") != "OWNER":
#         return "Only room owners can edit listings.", 403

#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)
#     try:
#         cursor.execute("""
#             SELECT r.room_id, r.title, r.description, r.rent, r.room_type,
#                    r.furnished, l.city, l.state, l.colony, l.address, l.pincode
#             FROM rooms r LEFT JOIN locations l ON l.room_id = r.room_id
#             WHERE r.room_id = %s AND r.owner_id = %s
#         """, (room_id, session["user_id"]))
#         room = cursor.fetchone()
#         if room is None:
#             return "Room not found, or it does not belong to your account.", 404

#         if request.method == "POST":
#             title = request.form.get("title", "").strip()
#             description = request.form.get("description", "").strip() or None
#             rent = request.form.get("rent", type=float)
#             room_type = request.form.get("room_type", "").strip()
#             furnished = request.form.get("furnished") == "true"
#             city = request.form.get("city", "").strip()
#             state = request.form.get("state", "").strip()
#             colony = request.form.get("colony", "").strip() or None
#             address = request.form.get("address", "").strip() or None
#             pincode = request.form.get("pincode", "").strip() or None

#             if not title or rent is None or rent < 0 or not room_type or not city or not state:
#                 return "Please enter a title, valid rent, room type, city and state.", 400
#             if pincode and (len(pincode) != 6 or not pincode.isdigit()):
#                 return "PIN code must contain exactly 6 digits.", 400

#             cursor.execute("""
#                 UPDATE rooms SET title=%s, description=%s, rent=%s,
#                     room_type=%s, furnished=%s
#                 WHERE room_id=%s AND owner_id=%s
#             """, (title, description, rent, room_type, furnished, room_id, session["user_id"]))
#             cursor.execute("""
#                 UPDATE locations SET city=%s, state=%s, colony=%s,
#                     address=%s, pincode=%s WHERE room_id=%s
#             """, (city, state, colony, address, pincode, room_id))
#             connection.commit()
#             return redirect(url_for("owner_dashboard"))

#         return render_template_string(r"""
#         <!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Edit room | Room Finder</title>
#         <style>body{margin:0;background:#f4f7fb;font-family:Arial,sans-serif;color:#17243a;padding:24px}.box{max-width:760px;margin:20px auto;background:#fff;padding:28px;border:1px solid #e3e9f2;border-radius:18px}h1{margin-top:0}.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}.field label{display:block;font-weight:700;font-size:14px;margin-bottom:7px}.field input,.field textarea,.field select{width:100%;padding:12px;border:1px solid #ccd5e2;border-radius:9px;font:inherit;box-sizing:border-box}.field.full{grid-column:1/-1}.actions{display:flex;gap:10px;margin-top:20px;flex-wrap:wrap}.btn{padding:12px 16px;border:0;border-radius:9px;background:#315efb;color:white;font-weight:bold;text-decoration:none;cursor:pointer}.btn.alt{background:#eaf0ff;color:#2448c7}@media(max-width:600px){.grid{grid-template-columns:1fr}.field.full{grid-column:auto}.box{padding:18px}}</style></head><body>
#         <main class="box"><h1>Edit room listing</h1><p>Update the details and save your changes.</p><form method="post"><div class="grid">
#         <div class="field full"><label>Room title *</label><input name="title" maxlength="150" required value="{{ room.title }}"></div>
#         <div class="field full"><label>Description</label><textarea name="description" rows="4">{{ room.description or '' }}</textarea></div>
#         <div class="field"><label>Monthly rent (₹) *</label><input type="number" name="rent" min="0" step="0.01" required value="{{ room.rent }}"></div>
#         <div class="field"><label>Room type *</label><input name="room_type" required value="{{ room.room_type }}"></div>
#         <div class="field"><label>City *</label><input name="city" required value="{{ room.city or '' }}"></div>
#         <div class="field"><label>State *</label><input name="state" required value="{{ room.state or '' }}"></div>
#         <div class="field"><label>Colony / area</label><input name="colony" value="{{ room.colony or '' }}"></div>
#         <div class="field"><label>PIN code</label><input name="pincode" pattern="[0-9]{6}" maxlength="6" value="{{ room.pincode or '' }}"></div>
#         <div class="field full"><label>Full address</label><input name="address" value="{{ room.address or '' }}"></div>
#         <div class="field"><label>Furnished?</label><select name="furnished"><option value="false" {{ 'selected' if not room.furnished else '' }}>No</option><option value="true" {{ 'selected' if room.furnished else '' }}>Yes</option></select></div>
#         </div><div class="actions"><button class="btn" type="submit">Save changes</button><a class="btn alt" href="{{ url_for('owner_dashboard') }}">Cancel</a></div></form></main></body></html>
#         """, room=room)
#     except Exception:
#         connection.rollback()
#         app.logger.exception("Room update failed")
#         return "Could not update this room. Check the server log.", 500
#     finally:
#         cursor.close()
#         connection.close()


# @app.route("/owner/room/<int:room_id>/availability", methods=["POST"])
# def toggle_room_availability(room_id):
#     if "user_id" not in session:
#         return redirect(url_for("login"))
#     if session.get("user_role") != "OWNER":
#         return "Only room owners can change availability.", 403
#     connection = get_db_connection()
#     cursor = connection.cursor()
#     try:
#         cursor.execute("""
#             UPDATE rooms SET available = NOT available
#             WHERE room_id = %s AND owner_id = %s
#         """, (room_id, session["user_id"]))
#         if cursor.rowcount == 0:
#             connection.rollback()
#             return "Room not found, or it does not belong to your account.", 404
#         connection.commit()
#         return redirect(url_for("owner_dashboard"))
#     except Exception:
#         connection.rollback()
#         app.logger.exception("Availability update failed")
#         return "Could not update room availability.", 500
#     finally:
#         cursor.close()
#         connection.close()


# @app.route("/owner/room/<int:room_id>/delete", methods=["POST"])
# def delete_room(room_id):
#     if "user_id" not in session:
#         return redirect(url_for("login"))
#     if session.get("user_role") != "OWNER":
#         return "Only room owners can delete listings.", 403
#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)
#     try:
#         cursor.execute("SELECT photo_path FROM room_photos WHERE room_id = %s", (room_id,))
#         photo_paths = [row["photo_path"] for row in cursor.fetchall()]
#         cursor.execute("DELETE FROM rooms WHERE room_id = %s AND owner_id = %s", (room_id, session["user_id"]))
#         if cursor.rowcount == 0:
#             connection.rollback()
#             return "Room not found, or it does not belong to your account.", 404
#         connection.commit()
#         # Remove the associated files after the database delete succeeds.
#         for photo_path in photo_paths:
#             safe_name = os.path.basename(photo_path)
#             file_path = os.path.join(app.config["UPLOAD_FOLDER"], safe_name)
#             if os.path.isfile(file_path):
#                 try:
#                     os.remove(file_path)
#                 except OSError:
#                     app.logger.warning("Could not remove old room photo: %s", safe_name)
#         return redirect(url_for("owner_dashboard"))
#     except Exception:
#         connection.rollback()
#         app.logger.exception("Room deletion failed")
#         return "Could not delete this room. Check the server log.", 500
#     finally:
#         cursor.close()
#         connection.close()


# if __name__ == "__main__":
#     app.run(debug=True)


from flask import session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import os
import uuid
from flask import (
    Flask, jsonify, request, send_from_directory,
    render_template_string
)
from werkzeug.utils import secure_filename
from db import get_db_connection

app = Flask(__name__)
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "dev-only-change-this-secret-before-deployment"
)
UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    logged_in = "user_id" in session
    user_name = session.get("user_name", "")
    user_role = session.get("user_role", "")

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Room Finder | Find a place to call home</title>
        <style>
            :root { --navy: #132238; --blue: #315efb; --muted: #68758a; --bg: #f5f7fb; --line: #e5eaf2; }
            * { box-sizing: border-box; }
            body { margin: 0; font-family: Inter, Arial, sans-serif; color: var(--navy); background: var(--bg); }
            a { text-decoration: none; }
            .nav { max-width: 1160px; margin: auto; padding: 22px 24px; display: flex; align-items: center; justify-content: space-between; gap: 18px; }
            .brand { color: var(--navy); font-size: 23px; font-weight: 800; letter-spacing: -.7px; }
            .brand span { color: var(--blue); }
            .navlinks { display: flex; align-items: center; flex-wrap: wrap; gap: 18px; }
            .navlinks a { color: #46546a; font-size: 14px; font-weight: 650; }
            .navlinks .nav-cta { background: var(--blue); color: white; padding: 11px 16px; border-radius: 11px; }
            .hero-wrap { padding: 28px 24px 58px; }
            .hero { max-width: 1112px; margin: auto; min-height: 390px; border-radius: 28px; padding: 56px; color: white; overflow: hidden; position: relative; background: linear-gradient(120deg, #142944 0%, #234d8e 62%, #3979d7 100%); box-shadow: 0 24px 60px rgba(26, 58, 104, .16); }
            .hero:after { content: ''; position: absolute; width: 360px; height: 360px; border: 1px solid rgba(255,255,255,.17); border-radius: 50%; right: -70px; top: 20px; box-shadow: 0 0 0 36px rgba(255,255,255,.035), 0 0 0 72px rgba(255,255,255,.025); }
            .eyebrow { display: inline-block; color: #dce7ff; background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.18); border-radius: 999px; padding: 8px 13px; font-size: 12px; font-weight: 750; letter-spacing: .8px; text-transform: uppercase; }
            h1 { max-width: 610px; margin: 22px 0 15px; font-size: clamp(36px, 5vw, 58px); line-height: 1.05; letter-spacing: -1.8px; }
            .hero p { max-width: 540px; color: #e0e9f8; line-height: 1.7; font-size: 16px; margin: 0 0 28px; }
            .actions { display: flex; flex-wrap: wrap; gap: 12px; }
            .btn { display: inline-flex; justify-content: center; align-items: center; border-radius: 12px; padding: 14px 19px; font-weight: 750; font-size: 14px; }
            .btn-light { background: white; color: #18345d; }
            .btn-outline { border: 1px solid rgba(255,255,255,.48); color: white; background: rgba(255,255,255,.07); }
            .content { max-width: 1112px; margin: 0 auto; padding: 0 24px 58px; }
            .section-head { display: flex; align-items: end; justify-content: space-between; gap: 16px; margin: 0 0 22px; }
            .section-head h2 { font-size: 25px; letter-spacing: -.6px; margin: 0 0 7px; }
            .section-head p { color: var(--muted); margin: 0; font-size: 14px; }
            .cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
            .card { background: white; border: 1px solid var(--line); border-radius: 18px; padding: 24px; box-shadow: 0 8px 26px rgba(22, 41, 71, .035); }
            .icon { width: 44px; height: 44px; border-radius: 13px; display: grid; place-items: center; background: #edf2ff; color: var(--blue); font-size: 21px; margin-bottom: 18px; }
            .card h3 { margin: 0 0 9px; font-size: 17px; }
            .card p { margin: 0 0 17px; color: var(--muted); line-height: 1.6; font-size: 14px; }
            .card a { color: var(--blue); font-weight: 750; font-size: 14px; }
            .welcome { max-width: 1112px; margin: 0 auto 20px; padding: 0 24px; color: #36516e; font-size: 14px; }
            footer { border-top: 1px solid var(--line); padding: 22px 24px; text-align: center; color: var(--muted); font-size: 12px; }
            @media (max-width: 760px) { .nav { align-items: flex-start; flex-direction: column; } .navlinks { gap: 13px; } .hero { padding: 34px 25px; min-height: auto; } .hero:after { right: -230px; opacity: .7; } .cards { grid-template-columns: 1fr; } .section-head { align-items: flex-start; flex-direction: column; } }
        </style>
    </head>
    <body>
        <header class="nav">
            <a class="brand" href="/">Room<span>Finder</span></a>
            <nav class="navlinks">
                <a href="/browse-rooms">Browse rooms</a>
                {% if logged_in %}
                    <a href="/dashboard">Dashboard</a>
                    {% if user_role == 'OWNER' %}<a href="/add-room-page">Add a room</a>{% endif %}
                    <a class="nav-cta" href="/logout">Logout</a>
                {% else %}
                    <a href="/login">Login</a>
                    <a class="nav-cta" href="/register">Create account</a>
                {% endif %}
            </nav>
        </header>

        {% if logged_in %}<div class="welcome">Welcome back, <strong>{{ user_name }}</strong> · Account type: {{ user_role|title }}</div>{% endif %}

        <main>
            <section class="hero-wrap">
                <div class="hero">
                    <span class="eyebrow">A simpler way to find your space</span>
                    <h1>Find a room that feels like home.</h1>
                    <p>Explore rooms by city, PIN code, budget, and nearby college or office. Compare rent, check room photos and contact the owner.</p>
                    <div class="actions">
                        <a class="btn btn-light" href="/browse-rooms">Explore available rooms &nbsp; →</a>
                        {% if logged_in and user_role == 'OWNER' %}
                            <a class="btn btn-outline" href="/add-room-page">List your room</a>
                        {% elif not logged_in %}
                            <a class="btn btn-outline" href="/register">Join Room Finder</a>
                        {% else %}
                            <a class="btn btn-outline" href="/dashboard">Open dashboard</a>
                        {% endif %}
                    </div>
                </div>
            </section>

            <section class="content">
                <div class="section-head">
                    <div><h2>Everything you need to get started</h2><p>Simple tools for room seekers and property owners.</p></div>
                </div>
                <div class="cards">
                    <article class="card">
                        <div class="icon">⌕</div><h3>Browse rooms</h3>
                        <p>Search available rooms by city, PIN code and maximum rent, then open a listing to see its details.</p>
                        <a href="/browse-rooms">Search rooms →</a>
                    </article>
                    <article class="card">
                        <div class="icon">⌂</div><h3>List your room</h3>
                        <p>Room owners can sign in, add a listing with location details and share photos of the room.</p>
                        {% if logged_in and user_role == 'OWNER' %}<a href="/add-room-page">Add a room →</a>{% elif not logged_in %}<a href="/register">Create an owner account →</a>{% else %}<a href="/dashboard">Open dashboard →</a>{% endif %}
                    </article>
                    <article class="card">
                        <div class="icon">◎</div><h3>Your account</h3>
                        <p>Use your dashboard to access account features. Sign in to continue or create an account to get started.</p>
                        {% if logged_in %}<a href="/dashboard">Go to dashboard →</a>{% else %}<a href="/login">Login or register →</a>{% endif %}
                    </article>
                </div>
            </section>
        </main>
        <footer>Room Finder · Search smarter. Find your space.</footer>
    </body>
    </html>
    """, logged_in=logged_in, user_name=user_name, user_role=user_role)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        role = request.form.get("role", "").upper()

        if not name or not email or not phone or not password:
            return "Please fill in all fields.", 400

        if password != confirm_password:
            return "Passwords do not match.", 400

        if len(password) < 8:
            return "Password must be at least 8 characters.", 400

        if role not in ("OWNER", "TENANT"):
            return "Please select a valid role.", 400

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                "SELECT user_id FROM users WHERE email = %s",
                (email,)
            )
            if cursor.fetchone():
                return "This email is already registered.", 409

            hashed_password = generate_password_hash(password)

            cursor.execute("""
                INSERT INTO users (name, email, phone, password, role)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, email, phone, hashed_password, role))

            connection.commit()

            return """
                <h2>Registration successful!</h2>
                <p>Your account has been created.</p>
                <a href="/login">Go to Login</a>
                <br><br><a href="/">Home</a>
            """, 201

        except Exception:
            connection.rollback()
            app.logger.exception("Registration failed")
            return "Registration failed. Please check the server log.", 500

        finally:
            cursor.close()
            connection.close()

    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Register - Room Finder</title>
    </head>
    <body>
        <h1>Create Your Account</h1>

        <form method="POST" action="/register">
            <label>Full Name</label><br>
            <input type="text" name="name" required maxlength="100">
            <br><br>

            <label>Email</label><br>
            <input type="email" name="email" required maxlength="255">
            <br><br>

            <label>Phone</label><br>
            <input type="tel" name="phone" required maxlength="20">
            <br><br>

            <label>Password (minimum 8 characters)</label><br>
            <input type="password" name="password"
                   minlength="8" required>
            <br><br>

            <label>Confirm Password</label><br>
            <input type="password" name="confirm_password"
                   minlength="8" required>
            <br><br>

            <label>Account Type</label><br>
            <select name="role" required>
                <option value="">Choose account type</option>
                <option value="OWNER">Room Owner</option>
                <option value="TENANT">Room Seeker (Tenant)</option>
            </select>
            <br><br>

            <button type="submit">Register</button>
        </form>

        <p>Already have an account? <a href="/login">Login</a></p>
        <a href="/">Home</a>
    </body>
    </html>
    """


# Return available rooms as JSON
@app.route("/rooms")
def get_rooms():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT r.room_id, r.title, r.description,
                   r.rent, r.room_type, r.furnished,
                   l.city, l.state, l.colony,
                   l.address, l.pincode
            FROM rooms r
            LEFT JOIN locations l ON r.room_id = l.room_id
            WHERE r.available = TRUE
            ORDER BY r.room_id DESC
        """)
        rooms = cursor.fetchall()

        for room in rooms:
            cursor.execute(
                "SELECT photo_path FROM room_photos WHERE room_id = %s",
                (room["room_id"],)
            )
            photos = cursor.fetchall()
            room["photos"] = [
                f"/uploads/{photo['photo_path']}" for photo in photos
            ]

        return jsonify(rooms)
    finally:
        cursor.close()
        connection.close()


# Display uploaded photos
@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# Page to add a room
@app.route("/add-room-page")
def add_room_page():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("user_role") != "OWNER":
        return "Only room owners can access this page.", 403

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add Room</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
        <h2>Add New Room</h2>
        <form action="/add-room" method="POST">
            Room Title:
            <input type="text" name="title" required>
            <br><br>

            Description:
            <input type="text" name="description">
            <br><br>

            Monthly Rent (Rs):
            <input type="number" name="rent" min="0" required>
            <br><br>

            Room Type:
            <input type="text" name="room_type"
                   placeholder="Single room, flat, PG" required>
            <br><br>

            City:
            <input type="text" name="city" required>
            <br><br>

            State:
            <input type="text" name="state" required>
            <br><br>

            Colony:
            <input type="text" name="colony">
            <br><br>

            Full Address:
            <input type="text" name="address">
            <br><br>

            Pincode:
            <input type="text" name="pincode"
                   pattern="[0-9]{6}"
                   title="Enter a 6-digit pincode">
            <br><br>

            Nearby College / University:
            <input type="text" name="nearby_college" maxlength="255"
                   placeholder="e.g. Chameli Devi Group of Institutions">
            <br><br>

            Nearby Office / Company:
            <input type="text" name="nearby_office" maxlength="255"
                   placeholder="e.g. Infosys, IT Park">
            <br><br>

            Furnished:
            <input type="checkbox" name="furnished" value="true">
            <br><br>

            <button type="submit">Add Room</button>
        </form>

        <br><a href="/browse-rooms">Browse Rooms</a>
    </body>
    </html>
    """


# Save room and its location in MySQL
@app.route("/add-room", methods=["POST"])
def add_room():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("user_role") != "OWNER":
        return "Only room owners can add rooms.", 403

    owner_id = session["user_id"]
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip() or None
    rent = request.form.get("rent", type=float)
    room_type = request.form.get("room_type", "").strip()
    furnished = request.form.get("furnished") == "true"

    city = request.form.get("city", "").strip()
    state = request.form.get("state", "").strip()
    colony = request.form.get("colony", "").strip() or None
    address = request.form.get("address", "").strip() or None
    pincode = request.form.get("pincode", "").strip() or None
    nearby_college = request.form.get("nearby_college", "").strip() or None
    nearby_office = request.form.get("nearby_office", "").strip() or None

    if not owner_id or not title or rent is None or rent < 0:
        return "Please enter a valid owner, title and rent.", 400

    if not room_type or not city or not state:
        return "Room type, city and state are required.", 400

    if pincode and (
        len(pincode) != 6 or not pincode.isdigit()
    ):
        return "Pincode must contain exactly 6 digits.", 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO rooms
                (owner_id, title, description, rent,
                 room_type, furnished)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            owner_id, title, description, rent,
            room_type, furnished
        ))

        room_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO locations
                (room_id, city, state, colony, address, pincode,
                 nearby_college, nearby_office)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            room_id, city, state, colony, address, pincode,
            nearby_college, nearby_office
        ))

        connection.commit()

        return f"""
        <!DOCTYPE html>
        <html>
        <body>
            <h2>Room added successfully!</h2>
            <p>Your Room ID is: {room_id}</p>
            <p>Remember this ID to upload its photo.</p>
            <a href="/upload-photo-page">Upload Room Photo</a><br><br>
            <a href="/browse-rooms">Browse Rooms</a><br><br>
            <a href="/">Home</a>
        </body>
        </html>
        """, 201

    except Exception as error:
        connection.rollback()
        app.logger.exception("Unable to add room")
        return f"Database error: {error}", 400

    finally:
        cursor.close()
        connection.close()


# Page to upload a room photo
@app.route("/upload-photo-page")
def upload_photo_page():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("user_role") != "OWNER":
        return "Only room owners can upload room photos.", 403

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Upload Room Photo</title>
    </head>
    <body>
        <h2>Upload Room Photo</h2>
        <form action="/upload-photo" method="POST"
              enctype="multipart/form-data">
            Room ID:
            <input type="number" name="room_id" min="1" required>
            <br><br>

            Select Photo:
            <input type="file" name="photo"
                   accept=".jpg,.jpeg,.png,.webp" required>
            <br><br>

            <button type="submit">Upload Photo</button>
        </form>
        <p>Allowed formats: JPG, JPEG, PNG, WEBP. Maximum size: 5 MB.</p>
        <a href="/browse-rooms">Browse Rooms</a>
    </body>
    </html>
    """


# Save photo to uploads folder and filename to MySQL
@app.route("/upload-photo", methods=["POST"])
def upload_photo():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("user_role") != "OWNER":
        return "Only room owners can upload room photos.", 403

    room_id = request.form.get("room_id", type=int)
    photo = request.files.get("photo")

    if not room_id or not photo or not photo.filename:
        return "Please provide a valid Room ID and photo.", 400

    original_name = secure_filename(photo.filename)

    if "." not in original_name:
        return "Invalid photo filename.", 400

    extension = original_name.rsplit(".", 1)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        return "Only JPG, JPEG, PNG and WEBP images are allowed.", 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    saved_path = None

    try:
        cursor.execute(
            "SELECT room_id FROM rooms WHERE room_id = %s AND owner_id = %s",
            (room_id, session["user_id"])
        )

        if cursor.fetchone() is None:
            return "Room not found, or this room does not belong to your account.", 404

        filename = f"{uuid.uuid4().hex}.{extension}"
        saved_path = os.path.join(
            app.config["UPLOAD_FOLDER"], filename
        )

        photo.save(saved_path)

        cursor.execute("""
            INSERT INTO room_photos (room_id, photo_path)
            VALUES (%s, %s)
        """, (room_id, filename))

        connection.commit()

        return f"""
        <!DOCTYPE html>
        <html>
        <body>
            <h2>Photo uploaded successfully!</h2>
            <img src="/uploads/{filename}"
                 width="350" alt="Uploaded room photo">
            <br><br>
            <a href="/browse-rooms">Browse Rooms</a><br><br>
            <a href="/upload-photo-page">Upload Another Photo</a>
        </body>
        </html>
        """

    except Exception as error:
        connection.rollback()

        if saved_path and os.path.exists(saved_path):
            os.remove(saved_path)

        app.logger.exception("Photo upload failed")
        return f"Photo upload failed: {error}", 400

    finally:
        cursor.close()
        connection.close()


# Browse rooms with advanced search filters
@app.route("/browse-rooms")
def browse_rooms():
    city = request.args.get("city", "").strip()
    pincode = request.args.get("pincode", "").strip()
    nearby_place = request.args.get("nearby_place", "").strip()
    min_rent_text = request.args.get("min_rent", "").strip()
    max_rent_text = request.args.get("max_rent", "").strip()
    room_type = request.args.get("room_type", "").strip()
    furnished = request.args.get("furnished", "").strip().lower()
    availability = request.args.get("availability", "available").strip().lower()

    if pincode and (len(pincode) != 6 or not pincode.isdigit()):
        return "Pincode must contain exactly 6 digits.", 400

    if furnished not in ("", "yes", "no"):
        return "Please choose a valid furnishing filter.", 400

    if availability not in ("available", "all"):
        return "Please choose a valid availability filter.", 400

    min_rent = None
    max_rent = None
    try:
        if min_rent_text:
            min_rent = float(min_rent_text)
            if min_rent < 0:
                return "Minimum rent cannot be negative.", 400
        if max_rent_text:
            max_rent = float(max_rent_text)
            if max_rent < 0:
                return "Maximum rent cannot be negative.", 400
    except ValueError:
        return "Please enter a valid rent amount.", 400

    if min_rent is not None and max_rent is not None and min_rent > max_rent:
        return "Minimum rent cannot be greater than maximum rent.", 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
            SELECT
                r.room_id,
                r.title,
                r.description,
                r.rent,
                r.room_type,
                r.furnished,
                r.available,
                l.city,
                l.state,
                l.colony,
                l.address,
                l.pincode,
                l.nearby_college,
                l.nearby_office,
                (
                    SELECT rp.photo_path
                    FROM room_photos rp
                    WHERE rp.room_id = r.room_id
                    ORDER BY rp.photo_id DESC
                    LIMIT 1
                ) AS photo_path
            FROM rooms r
            LEFT JOIN locations l ON l.room_id = r.room_id
            WHERE 1=1
        """
        conditions = []
        values = []

        if availability == "available":
            conditions.append("r.available = TRUE")
        if city:
            conditions.append("l.city LIKE %s")
            values.append(f"%{city}%")
        if pincode:
            conditions.append("l.pincode = %s")
            values.append(pincode)
        if nearby_place:
            conditions.append("(l.nearby_college LIKE %s OR l.nearby_office LIKE %s)")
            values.extend([f"%{nearby_place}%", f"%{nearby_place}%"])
        if min_rent is not None:
            conditions.append("r.rent >= %s")
            values.append(min_rent)
        if max_rent is not None:
            conditions.append("r.rent <= %s")
            values.append(max_rent)
        if room_type:
            conditions.append("r.room_type LIKE %s")
            values.append(f"%{room_type}%")
        if furnished == "yes":
            conditions.append("r.furnished = TRUE")
        elif furnished == "no":
            conditions.append("r.furnished = FALSE")

        if conditions:
            query += " AND " + " AND ".join(conditions)
        query += " ORDER BY r.room_id DESC"

        cursor.execute(query, tuple(values))
        rooms = cursor.fetchall()

        return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Browse Rooms | Room Finder</title>
            <style>
                :root { --ink:#17263c; --muted:#68778b; --blue:#315efb; --line:#e3e9f2; --bg:#f5f7fb; }
                * { box-sizing:border-box; }
                body { margin:0; padding:24px; background:var(--bg); color:var(--ink); font-family:Arial,sans-serif; }
                .wrap { max-width:1180px; margin:auto; }
                header { display:flex; justify-content:space-between; align-items:center; gap:16px; flex-wrap:wrap; margin:0 0 24px; }
                .brand { font-size:23px; font-weight:800; color:var(--ink); text-decoration:none; }
                .brand span { color:var(--blue); }
                nav { display:flex; gap:16px; flex-wrap:wrap; }
                nav a { color:#40516a; text-decoration:none; font-size:14px; font-weight:700; }
                .intro { background:linear-gradient(120deg,#142944,#315fba); color:white; padding:30px; border-radius:22px; }
                .intro h1 { margin:0 0 8px; font-size:clamp(28px,4vw,40px); }
                .intro p { margin:0; color:#e0eaff; line-height:1.6; }
                .filters { background:white; border:1px solid var(--line); border-radius:18px; padding:20px; margin:20px 0; box-shadow:0 8px 24px #1a2b4808; }
                .filters h2 { margin:0 0 16px; font-size:18px; }
                .filter-grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:14px; }
                label { display:block; font-size:13px; font-weight:700; margin-bottom:7px; }
                input, select { width:100%; min-width:0; padding:11px 12px; border:1px solid #ccd5e2; border-radius:9px; font-size:14px; background:white; color:var(--ink); }
                .filter-actions { display:flex; align-items:center; flex-wrap:wrap; gap:12px; margin-top:17px; }
                .btn { border:0; border-radius:10px; background:var(--blue); color:white; padding:12px 17px; font-weight:750; text-decoration:none; cursor:pointer; }
                .clear { color:var(--blue); font-size:14px; font-weight:700; text-decoration:none; }
                .count { color:var(--muted); margin:24px 0 14px; font-size:14px; }
                .rooms { display:grid; grid-template-columns:repeat(auto-fit,minmax(255px,1fr)); gap:18px; }
                .card { background:white; border:1px solid var(--line); border-radius:17px; padding:14px; overflow:hidden; box-shadow:0 6px 22px #1a2b4808; }
                .card img, .no-photo { width:100%; height:190px; object-fit:cover; border-radius:11px; background:#edf1f7; }
                .no-photo { display:grid; place-items:center; color:var(--muted); }
                .card h2 { font-size:19px; margin:15px 0 8px; overflow-wrap:anywhere; }
                .rent { color:#087443; font-size:22px; font-weight:800; margin:0 0 12px; }
                .meta { color:#56657a; font-size:14px; line-height:1.55; overflow-wrap:anywhere; }
                .status { display:inline-block; padding:5px 9px; border-radius:999px; background:#e7f8ee; color:#137342; font-size:12px; font-weight:800; }
                .status.off { background:#fff0e8; color:#a34a12; }
                .details { display:inline-block; margin-top:8px; background:var(--blue); color:white; padding:10px 13px; border-radius:9px; text-decoration:none; font-weight:750; font-size:14px; }
                .empty { background:white; padding:28px; border-radius:16px; grid-column:1/-1; }
                @media(max-width:850px) { .filter-grid { grid-template-columns:repeat(2,minmax(0,1fr)); } }
                @media(max-width:520px) { body { padding:14px; } .intro { padding:23px; } .filter-grid { grid-template-columns:1fr; } }
            </style>
        </head>
        <body>
        <div class="wrap">
            <header>
                <a class="brand" href="/">Room<span>Finder</span></a>
                <nav><a href="/">Home</a><a href="/dashboard">Dashboard</a><a href="/logout">Logout</a></nav>
            </header>
            <section class="intro">
                <h1>Find a room that fits your life.</h1>
                <p>Filter by location, monthly budget, room type, furnishing, or a nearby college / office name.</p>
            </section>
            <form class="filters" action="/browse-rooms" method="GET">
                <h2>Refine your search</h2>
                <div class="filter-grid">
                    <div><label for="city">City</label><input id="city" name="city" type="text" placeholder="e.g. Indore" value="{{ city }}"></div>
                    <div><label for="pincode">PIN code</label><input id="pincode" name="pincode" type="text" inputmode="numeric" pattern="[0-9]{6}" maxlength="6" placeholder="6-digit PIN code" value="{{ pincode }}"></div>
                    <div><label for="nearby_place">Nearby college / office</label><input id="nearby_place" name="nearby_place" type="text" placeholder="e.g. college or company name" value="{{ nearby_place }}"></div>
                    <div><label for="min_rent">Minimum monthly rent (₹)</label><input id="min_rent" name="min_rent" type="number" min="0" step="any" placeholder="e.g. 3000" value="{{ min_rent_text }}"></div>
                    <div><label for="max_rent">Maximum monthly rent (₹)</label><input id="max_rent" name="max_rent" type="number" min="0" step="any" placeholder="e.g. 8000" value="{{ max_rent_text }}"></div>
                    <div><label for="room_type">Room type</label><input id="room_type" name="room_type" type="text" placeholder="e.g. Single, Shared, 1BHK" value="{{ room_type }}"></div>
                    <div><label for="furnished">Furnishing</label><select id="furnished" name="furnished"><option value="" {{ 'selected' if not furnished else '' }}>Any</option><option value="yes" {{ 'selected' if furnished == 'yes' else '' }}>Furnished</option><option value="no" {{ 'selected' if furnished == 'no' else '' }}>Unfurnished</option></select></div>
                    <div><label for="availability">Availability</label><select id="availability" name="availability"><option value="available" {{ 'selected' if availability == 'available' else '' }}>Available only</option><option value="all" {{ 'selected' if availability == 'all' else '' }}>All listings</option></select></div>
                </div>
                <div class="filter-actions"><button class="btn" type="submit">Search rooms</button><a class="clear" href="/browse-rooms">Clear all filters</a></div>
            </form>
            <p class="count">Found <strong>{{ rooms|length }}</strong> room(s) matching your filters.</p>
            <section class="rooms">
                {% for room in rooms %}
                <article class="card">
                    {% if room.photo_path %}<img src="{{ url_for('uploaded_file', filename=room.photo_path) }}" alt="Photo of {{ room.title }}">{% else %}<div class="no-photo">No photo uploaded yet</div>{% endif %}
                    <h2>{{ room.title }}</h2>
                    <p class="rent">₹{{ room.rent }} <span style="font-size:13px;font-weight:500;color:#68778b">/ month</span></p>
                    <span class="status {{ 'off' if not room.available else '' }}">{{ 'Available' if room.available else 'Unavailable' }}</span>
                    <p class="meta"><b>Room type:</b> {{ room.room_type or 'Not specified' }}<br><b>Furnished:</b> {{ 'Yes' if room.furnished else 'No' }}<br><b>City:</b> {{ room.city or 'Not provided' }}<br><b>State:</b> {{ room.state or 'Not provided' }}<br><b>Colony:</b> {{ room.colony or 'Not provided' }}<br><b>PIN code:</b> {{ room.pincode or 'Not provided' }}<br><b>Nearby college:</b> {{ room.nearby_college or 'Not provided' }}<br><b>Nearby office:</b> {{ room.nearby_office or 'Not provided' }}</p>
                    {% if room.description %}<p class="meta">{{ room.description }}</p>{% endif %}
                    <a class="details" href="{{ url_for('room_details', room_id=room.room_id) }}">View details →</a>
                </article>
                {% else %}
                <div class="empty"><h2>No rooms found</h2><p>Try increasing your budget or removing one or more filters.</p><a class="details" href="/browse-rooms">Clear filters</a></div>
                {% endfor %}
            </section>
        </div>
        </body>
        </html>
        """, rooms=rooms, city=city, pincode=pincode,
            min_rent_text=min_rent_text, max_rent_text=max_rent_text,
            room_type=room_type, furnished=furnished, availability=availability,
            nearby_place=nearby_place)
    finally:
        cursor.close()
        connection.close()


@app.errorhandler(413)
def file_too_large(error):
    return "Photo size must be 5 MB or less.", 413

@app.route("/room/<int:room_id>")
def room_details(room_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                r.room_id,
                r.owner_id,
                r.title,
                r.description,
                r.rent,
                r.room_type,
                r.furnished,
                l.city,
                l.state,
                l.colony,
                l.address,
                l.pincode,
                l.nearby_college,
                l.nearby_office,
                u.name AS owner_name,
                u.email AS owner_email,
                u.phone AS owner_phone
            FROM rooms r
            LEFT JOIN locations l
                ON r.room_id = l.room_id
            LEFT JOIN users u
                ON r.owner_id = u.user_id
            WHERE r.room_id = %s
              AND r.available = TRUE
        """, (room_id,))

        room = cursor.fetchone()

        if room is None:
            return "Room not found or no longer available.", 404

        cursor.execute("""
            SELECT photo_path
            FROM room_photos
            WHERE room_id = %s
            ORDER BY photo_id DESC
        """, (room_id,))

        photos = cursor.fetchall()

        return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport"
                  content="width=device-width, initial-scale=1">
            <title>{{ room.title }} - Room Finder</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: #f3f5f8;
                    margin: 0;
                    padding: 24px;
                    color: #202938;
                }
                .container {
                    max-width: 850px;
                    margin: auto;
                    background: white;
                    padding: 24px;
                    border-radius: 14px;
                }
                .gallery {
                    display: grid;
                    grid-template-columns:
                        repeat(auto-fit, minmax(220px, 1fr));
                    gap: 12px;
                }
                .gallery img {
                    width: 100%;
                    height: 230px;
                    object-fit: cover;
                    border-radius: 10px;
                }
                .rent {
                    color: #087443;
                    font-size: 26px;
                    font-weight: bold;
                }
                .owner {
                    background: #f0f5ff;
                    padding: 18px;
                    border-radius: 10px;
                    margin-top: 24px;
                }
                .contact {
                    display: inline-block;
                    background: #1769e0;
                    color: white;
                    padding: 11px 16px;
                    border-radius: 7px;
                    text-decoration: none;
                    margin: 5px 5px 5px 0;
                }
                .back {
                    display: inline-block;
                    margin-bottom: 20px;
                }
                @media (max-width: 600px) {
                    body { padding: 12px; }
                    .container { padding: 16px; }
                }
            </style>
        </head>
        <body>
            <main class="container">
                <a class="back" href="/browse-rooms">
                    &larr; Back to rooms
                </a>

                <h1>{{ room.title }}</h1>

                <div class="gallery">
                    {% for photo in photos %}
                        <img
                            src="{{ url_for(
                                'uploaded_file',
                                filename=photo.photo_path
                            ) }}"
                            alt="Room photo">
                    {% else %}
                        <p>No photos available for this room.</p>
                    {% endfor %}
                </div>

                <p class="rent">Rs {{ room.rent }} / month</p>
                <p><b>Room type:</b> {{ room.room_type }}</p>
                <p><b>Description:</b>
                    {{ room.description or 'Not provided' }}</p>
                <p><b>Furnished:</b>
                    {{ 'Yes' if room.furnished else 'No' }}</p>

                <h2>Location Details</h2>
                <p><b>City:</b> {{ room.city or 'Not provided' }}</p>
                <p><b>State:</b> {{ room.state or 'Not provided' }}</p>
                <p><b>Colony:</b> {{ room.colony or 'Not provided' }}</p>
                <p><b>Address:</b> {{ room.address or 'Not provided' }}</p>
                <p><b>Pincode:</b> {{ room.pincode or 'Not provided' }}</p>

                <section class="owner">
                    <h2>Contact Room Owner</h2>
                    <p><b>Name:</b> {{ room.owner_name }}</p>
                    <p><b>Email:</b> {{ room.owner_email }}</p>
                    <p><b>Phone:</b>
                        {{ room.owner_phone or 'Not provided' }}</p>

                    {% if room.owner_phone %}
                        <a class="contact"
                           href="tel:{{ room.owner_phone }}">
                            Call Owner
                        </a>
                    {% endif %}

                    <a class="contact"
                       href="mailto:{{ room.owner_email }}">
                        Email Owner
                    </a>
                </section>
            </main>
        </body>
        </html>
        """, room=room, photos=photos)

    finally:
        cursor.close()
        connection.close()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            return "Please enter email and password.", 400

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                "SELECT user_id, name, email, password, role "
                "FROM users WHERE email = %s",
                (email,)
            )
            user = cursor.fetchone()

            if not user or not check_password_hash(
                user["password"], password
            ):
                return "Invalid email or password.", 401

            session.clear()
            session["user_id"] = user["user_id"]
            session["user_name"] = user["name"]
            session["user_role"] = user["role"]

            return redirect(url_for("dashboard"))

        finally:
            cursor.close()
            connection.close()

    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Login - Room Finder</title>
    </head>
    <body>
        <h1>Login to Room Finder</h1>

        <form method="POST" action="/login">
            <label>Email</label><br>
            <input type="email" name="email" required>
            <br><br>

            <label>Password</label><br>
            <input type="password" name="password" required>
            <br><br>

            <button type="submit">Login</button>
        </form>

        <p>New user? <a href="/register">Create account</a></p>
        <a href="/">Home</a>
    </body>
    </html>
    """


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("user_role") == "OWNER":
        return redirect(url_for("owner_dashboard"))

    return render_template_string("""
    <!DOCTYPE html><html lang="en"><head>
      <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Dashboard | Room Finder</title>
      <style>
        body{margin:0;background:#f4f7fb;font-family:Arial,sans-serif;color:#17243a}
        .wrap{max-width:850px;margin:45px auto;padding:24px}
        .card{background:#fff;border:1px solid #e3e9f2;border-radius:18px;padding:28px;box-shadow:0 10px 30px #1422380d}
        a{display:inline-block;margin:8px 8px 0 0;padding:12px 16px;border-radius:10px;text-decoration:none;background:#315efb;color:white;font-weight:bold}
        a.secondary{background:#eaf0ff;color:#2448c7}
      </style></head><body><main class="wrap"><section class="card">
      <h1>Welcome, {{ user_name }}!</h1><p>Your account type: <b>{{ role|title }}</b></p>
      <p>Browse available rooms and find a place that suits your needs.</p>
      <a href="{{ url_for('browse_rooms') }}">Browse Rooms</a>
      <a class="secondary" href="{{ url_for('home') }}">Home</a>
      <a class="secondary" href="{{ url_for('logout') }}">Logout</a>
      </section></main></body></html>
    """, user_name=session.get("user_name", "User"), role=session.get("user_role", "TENANT"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# Owner dashboard: only show rooms owned by the logged-in owner.
@app.route("/owner-dashboard")
def owner_dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session.get("user_role") != "OWNER":
        return "Only room owners can access this page.", 403

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT r.room_id, r.title, r.description, r.rent,
                   r.room_type, r.furnished, r.available, r.created_at,
                   l.city, l.state, l.pincode,
                   l.nearby_college, l.nearby_office,
                   (SELECT rp.photo_path FROM room_photos rp
                    WHERE rp.room_id = r.room_id
                    ORDER BY rp.photo_id DESC LIMIT 1) AS cover_photo,
                   (SELECT COUNT(*) FROM room_photos rp2
                    WHERE rp2.room_id = r.room_id) AS photo_count
            FROM rooms r
            LEFT JOIN locations l ON l.room_id = r.room_id
            WHERE r.owner_id = %s
            ORDER BY r.room_id DESC
        """, (session["user_id"],))
        rooms = cursor.fetchall()
        total = len(rooms)
        available_count = sum(1 for room in rooms if room["available"])
        unavailable_count = total - available_count
        return render_template_string(r"""
        <!DOCTYPE html><html lang="en"><head>
          <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
          <title>Owner Dashboard | Room Finder</title>
          <style>
            :root{--blue:#315efb;--navy:#17243a;--muted:#6b778b;--line:#e4eaf3;--bg:#f4f7fb}
            *{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--navy);font-family:Arial,sans-serif}
            header{background:#fff;border-bottom:1px solid var(--line)}.nav{max-width:1160px;margin:auto;padding:18px 22px;display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap}
            .brand{font-size:22px;font-weight:800;color:var(--navy);text-decoration:none}.brand span{color:var(--blue)}.nav a.link{color:#42516a;text-decoration:none;margin-left:14px;font-weight:700;font-size:14px}
            .wrap{max-width:1160px;margin:28px auto;padding:0 22px 50px}.top{display:flex;justify-content:space-between;align-items:center;gap:18px;flex-wrap:wrap;margin-bottom:22px}
            h1{margin:0 0 8px;font-size:clamp(27px,4vw,36px)}.muted{color:var(--muted);margin:0;line-height:1.6}
            .btn{display:inline-block;border:0;border-radius:10px;padding:11px 14px;background:var(--blue);color:#fff;text-decoration:none;font-weight:750;font-size:13px;cursor:pointer}.btn.light{background:#eaf0ff;color:#2448c7}.btn.danger{background:#fff0f0;color:#b42318}.btn.gray{background:#edf1f7;color:#344054}
            .stats{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:20px 0 26px}.stat{background:#fff;border:1px solid var(--line);border-radius:15px;padding:20px}.stat span{display:block;color:var(--muted);font-size:13px;margin-bottom:9px}.stat strong{font-size:28px}
            .room{display:grid;grid-template-columns:190px 1fr;gap:20px;background:#fff;border:1px solid var(--line);border-radius:17px;padding:16px;margin:14px 0;box-shadow:0 7px 20px #17243a08}.photo{width:100%;height:150px;object-fit:cover;border-radius:11px;background:#eef2f8}.placeholder{height:150px;border-radius:11px;background:#eef2f8;display:grid;place-items:center;color:#78869c;font-size:14px}
            .roomhead{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;flex-wrap:wrap}.room h2{font-size:20px;margin:2px 0 8px}.rent{font-size:21px;font-weight:800;color:#087443;white-space:nowrap}.details{color:var(--muted);font-size:14px;line-height:1.7;margin:8px 0 14px}.badge{display:inline-block;border-radius:999px;padding:6px 9px;font-size:12px;font-weight:800}.yes{background:#e8f8ee;color:#087443}.no{background:#fff0e8;color:#a54800}.actions{display:flex;gap:8px;flex-wrap:wrap}.actions form{margin:0}.empty{background:#fff;border:1px dashed #cbd5e1;border-radius:16px;padding:34px;text-align:center}
            @media(max-width:650px){.stats{grid-template-columns:1fr}.room{grid-template-columns:1fr}.photo,.placeholder{height:210px}.nav a.link{margin-left:0;margin-right:12px}}
          </style></head><body>
          <header><nav class="nav"><a class="brand" href="/">Room<span>Finder</span></a><div><a class="link" href="/browse-rooms">Browse rooms</a><a class="link" href="/add-room-page">Add room</a><a class="link" href="/upload-photo-page">Upload photo</a><a class="link" href="/logout">Logout</a></div></nav></header>
          <main class="wrap"><div class="top"><div><h1>Owner Dashboard</h1><p class="muted">Welcome, {{ owner_name }}. Manage the rooms listed from your account.</p></div><a class="btn" href="/add-room-page">＋ Add new room</a></div>
          <section class="stats"><div class="stat"><span>Total listings</span><strong>{{ total }}</strong></div><div class="stat"><span>Available now</span><strong>{{ available_count }}</strong></div><div class="stat"><span>Marked unavailable</span><strong>{{ unavailable_count }}</strong></div></section>
          <h2>Your rooms</h2><p class="muted">You can edit a listing, change its availability, or delete it. Deleted listings cannot be restored.</p>
          {% for room in rooms %}<article class="room"><div>{% if room.cover_photo %}<img class="photo" src="{{ url_for('uploaded_file', filename=room.cover_photo) }}" alt="Room photo">{% else %}<div class="placeholder">No photo yet</div>{% endif %}</div><div><div class="roomhead"><div><h2>{{ room.title }}</h2><span class="badge {{ 'yes' if room.available else 'no' }}">{{ 'Available' if room.available else 'Unavailable' }}</span></div><div class="rent">₹{{ '%.2f'|format(room.rent|float) }}<small style="font-size:12px;color:#6b778b;font-weight:500"> / month</small></div></div>
          <p class="details"><b>Room type:</b> {{ room.room_type }} · <b>Furnished:</b> {{ 'Yes' if room.furnished else 'No' }}<br><b>Location:</b> {{ room.city or 'City not added' }}, {{ room.state or '' }} {% if room.pincode %}· PIN {{ room.pincode }}{% endif %}<br><b>Nearby college:</b> {{ room.nearby_college or 'Not provided' }}<br><b>Nearby office:</b> {{ room.nearby_office or 'Not provided' }}<br><b>Photos:</b> {{ room.photo_count }}<br>{{ room.description or 'No description added.' }}</p>
          <div class="actions"><a class="btn" href="{{ url_for('edit_room', room_id=room.room_id) }}">Edit details</a><a class="btn light" href="{{ url_for('room_details', room_id=room.room_id) }}">View listing</a><a class="btn gray" href="/upload-photo-page?room_id={{ room.room_id }}">Upload photo</a>
          <form method="post" action="{{ url_for('toggle_room_availability', room_id=room.room_id) }}"><button class="btn light" type="submit">Mark {{ 'unavailable' if room.available else 'available' }}</button></form>
          <form method="post" action="{{ url_for('delete_room', room_id=room.room_id) }}" onsubmit="return confirm('Delete this room listing permanently?');"><button class="btn danger" type="submit">Delete</button></form></div></div></article>
          {% else %}<div class="empty"><h3>You haven't listed any rooms yet.</h3><p class="muted">Add your first room and it will appear here.</p><br><a class="btn" href="/add-room-page">Add your first room</a></div>{% endfor %}
          <p style="margin-top:25px"><a class="btn light" href="/">← Back to home</a></p></main></body></html>
        """, owner_name=session.get("user_name", "Owner"), rooms=rooms, total=total,
            available_count=available_count, unavailable_count=unavailable_count)
    finally:
        cursor.close()
        connection.close()


@app.route("/owner/room/<int:room_id>/edit", methods=["GET", "POST"])
def edit_room(room_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session.get("user_role") != "OWNER":
        return "Only room owners can edit listings.", 403

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT r.room_id, r.title, r.description, r.rent, r.room_type,
                   r.furnished, l.city, l.state, l.colony, l.address, l.pincode,
                   l.nearby_college, l.nearby_office
            FROM rooms r LEFT JOIN locations l ON l.room_id = r.room_id
            WHERE r.room_id = %s AND r.owner_id = %s
        """, (room_id, session["user_id"]))
        room = cursor.fetchone()
        if room is None:
            return "Room not found, or it does not belong to your account.", 404

        if request.method == "POST":
            title = request.form.get("title", "").strip()
            description = request.form.get("description", "").strip() or None
            rent = request.form.get("rent", type=float)
            room_type = request.form.get("room_type", "").strip()
            furnished = request.form.get("furnished") == "true"
            city = request.form.get("city", "").strip()
            state = request.form.get("state", "").strip()
            colony = request.form.get("colony", "").strip() or None
            address = request.form.get("address", "").strip() or None
            pincode = request.form.get("pincode", "").strip() or None
            nearby_college = request.form.get("nearby_college", "").strip() or None
            nearby_office = request.form.get("nearby_office", "").strip() or None

            if not title or rent is None or rent < 0 or not room_type or not city or not state:
                return "Please enter a title, valid rent, room type, city and state.", 400
            if pincode and (len(pincode) != 6 or not pincode.isdigit()):
                return "PIN code must contain exactly 6 digits.", 400

            cursor.execute("""
                UPDATE rooms SET title=%s, description=%s, rent=%s,
                    room_type=%s, furnished=%s
                WHERE room_id=%s AND owner_id=%s
            """, (title, description, rent, room_type, furnished, room_id, session["user_id"]))
            cursor.execute("""
                UPDATE locations SET city=%s, state=%s, colony=%s,
                    address=%s, pincode=%s, nearby_college=%s,
                    nearby_office=%s WHERE room_id=%s
            """, (city, state, colony, address, pincode,
                  nearby_college, nearby_office, room_id))
            connection.commit()
            return redirect(url_for("owner_dashboard"))

        return render_template_string(r"""
        <!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Edit room | Room Finder</title>
        <style>body{margin:0;background:#f4f7fb;font-family:Arial,sans-serif;color:#17243a;padding:24px}.box{max-width:760px;margin:20px auto;background:#fff;padding:28px;border:1px solid #e3e9f2;border-radius:18px}h1{margin-top:0}.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}.field label{display:block;font-weight:700;font-size:14px;margin-bottom:7px}.field input,.field textarea,.field select{width:100%;padding:12px;border:1px solid #ccd5e2;border-radius:9px;font:inherit;box-sizing:border-box}.field.full{grid-column:1/-1}.actions{display:flex;gap:10px;margin-top:20px;flex-wrap:wrap}.btn{padding:12px 16px;border:0;border-radius:9px;background:#315efb;color:white;font-weight:bold;text-decoration:none;cursor:pointer}.btn.alt{background:#eaf0ff;color:#2448c7}@media(max-width:600px){.grid{grid-template-columns:1fr}.field.full{grid-column:auto}.box{padding:18px}}</style></head><body>
        <main class="box"><h1>Edit room listing</h1><p>Update the details and save your changes.</p><form method="post"><div class="grid">
        <div class="field full"><label>Room title *</label><input name="title" maxlength="150" required value="{{ room.title }}"></div>
        <div class="field full"><label>Description</label><textarea name="description" rows="4">{{ room.description or '' }}</textarea></div>
        <div class="field"><label>Monthly rent (₹) *</label><input type="number" name="rent" min="0" step="0.01" required value="{{ room.rent }}"></div>
        <div class="field"><label>Room type *</label><input name="room_type" required value="{{ room.room_type }}"></div>
        <div class="field"><label>City *</label><input name="city" required value="{{ room.city or '' }}"></div>
        <div class="field"><label>State *</label><input name="state" required value="{{ room.state or '' }}"></div>
        <div class="field"><label>Colony / area</label><input name="colony" value="{{ room.colony or '' }}"></div>
        <div class="field"><label>PIN code</label><input name="pincode" pattern="[0-9]{6}" maxlength="6" value="{{ room.pincode or '' }}"></div>
        <div class="field full"><label>Full address</label><input name="address" value="{{ room.address or '' }}"></div>
        <div class="field"><label>Nearby college / university</label><input name="nearby_college" maxlength="255" value="{{ room.nearby_college or '' }}"></div>
        <div class="field"><label>Nearby office / company</label><input name="nearby_office" maxlength="255" value="{{ room.nearby_office or '' }}"></div>
        <div class="field"><label>Furnished?</label><select name="furnished"><option value="false" {{ 'selected' if not room.furnished else '' }}>No</option><option value="true" {{ 'selected' if room.furnished else '' }}>Yes</option></select></div>
        </div><div class="actions"><button class="btn" type="submit">Save changes</button><a class="btn alt" href="{{ url_for('owner_dashboard') }}">Cancel</a></div></form></main></body></html>
        """, room=room)
    except Exception:
        connection.rollback()
        app.logger.exception("Room update failed")
        return "Could not update this room. Check the server log.", 500
    finally:
        cursor.close()
        connection.close()


@app.route("/owner/room/<int:room_id>/availability", methods=["POST"])
def toggle_room_availability(room_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session.get("user_role") != "OWNER":
        return "Only room owners can change availability.", 403
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            UPDATE rooms SET available = NOT available
            WHERE room_id = %s AND owner_id = %s
        """, (room_id, session["user_id"]))
        if cursor.rowcount == 0:
            connection.rollback()
            return "Room not found, or it does not belong to your account.", 404
        connection.commit()
        return redirect(url_for("owner_dashboard"))
    except Exception:
        connection.rollback()
        app.logger.exception("Availability update failed")
        return "Could not update room availability.", 500
    finally:
        cursor.close()
        connection.close()


@app.route("/owner/room/<int:room_id>/delete", methods=["POST"])
def delete_room(room_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session.get("user_role") != "OWNER":
        return "Only room owners can delete listings.", 403
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT photo_path FROM room_photos WHERE room_id = %s", (room_id,))
        photo_paths = [row["photo_path"] for row in cursor.fetchall()]
        cursor.execute("DELETE FROM rooms WHERE room_id = %s AND owner_id = %s", (room_id, session["user_id"]))
        if cursor.rowcount == 0:
            connection.rollback()
            return "Room not found, or it does not belong to your account.", 404
        connection.commit()
        # Remove the associated files after the database delete succeeds.
        for photo_path in photo_paths:
            safe_name = os.path.basename(photo_path)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], safe_name)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                except OSError:
                    app.logger.warning("Could not remove old room photo: %s", safe_name)
        return redirect(url_for("owner_dashboard"))
    except Exception:
        connection.rollback()
        app.logger.exception("Room deletion failed")
        return "Could not delete this room. Check the server log.", 500
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    app.run(debug=True)


