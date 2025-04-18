## 🎯 هدف: طراحی Endpointهای مورد نیاز برای MVP

### 🧩 ماژول‌های اصلی MVP:
1. Auth (ورود/ثبت‌نام)
2. User Profile
3. Room (ساخت، پیوستن، لیست)
4. Message (چت متنی)
5. Music (آپلود، پخش، لیست)

---

## 🔐 1. Authentication (ثبت‌نام و ورود)

| Method | Endpoint | توضیح |
|--------|----------|-------|
| `POST` | `/auth/register` | ثبت‌نام کاربر جدید |
| `POST` | `/auth/login` | ورود کاربر (دریافت توکن) |
| `GET` | `/auth/me` | گرفتن اطلاعات کاربر لاگین‌شده |
| `POST` | `/auth/logout` | (در صورت نیاز) حذف توکن از سمت سرور |

---

## 👤 2. User Profile

| Method | Endpoint | توضیح |
|--------|----------|-------|
| `GET` | `/users/{id}` | دریافت اطلاعات پروفایل کاربر |
| `PATCH` | `/users/me` | آپدیت پروفایل (نام، عکس، رمز و...) |
| `GET` | `/users/me/friends` | (اختیاری برای MVP) لیست دوستان فیک یا دیتای ساختگی |

---

## 🏠 3. Voice Rooms

| Method | Endpoint | توضیح |
|--------|----------|-------|
| `GET` | `/rooms/` | لیست تمام روم‌ها (اکتیو) |
| `POST` | `/rooms/` | ساخت روم جدید |
| `GET` | `/rooms/{id}` | اطلاعات یک روم خاص |
| `POST` | `/rooms/{id}/join` | پیوستن به یک روم |
| `POST` | `/rooms/{id}/leave` | ترک کردن روم |

> داخل روم، اطلاعاتی مثل اسم، تعداد افراد، لیست اعضا و موزیک در حال پخش مهمه.

---

## 💬 4. Chat Messages (درون روم)

| Method | Endpoint | توضیح |
|--------|----------|-------|
| `GET` | `/rooms/{room_id}/messages` | گرفتن پیام‌های روم |
| `POST` | `/rooms/{room_id}/messages` | ارسال پیام جدید |
| `DELETE` | `/rooms/{room_id}/messages/{message_id}` | حذف پیام (در صورت نیاز) |

---

## 🎵 5. Music (آپلود و پخش)

| Method | Endpoint | توضیح |
|--------|----------|-------|
| `POST` | `/music/upload` | آپلود فایل موسیقی توسط کاربر |
| `GET` | `/music/` | لیست موزیک‌های آپلود شده |
| `GET` | `/music/{id}` | گرفتن یک فایل موسیقی خاص (برای پخش) |
| `DELETE` | `/music/{id}` | حذف یک موزیک (در صورت نیاز) |

---

## 📌 سایر Endpointهای اختیاری برای بعد از MVP:

- نوتیفیکیشن‌ها
- نقش‌ها و ACL
- دوستان واقعی و درخواست دوستی
- WebSocket endpoint برای چت یا موزیک real-time
- روم صوتی (WebRTC Signaling API)

## 🧱 **لیست Entityهای MVP**

### 1. `User`
اطلاعات حساب کاربری

| فیلد | نوع | توضیح |
|------|-----|--------|
| `id` | UUID |
| `username` | String |
| `email` | String |
| `password_hash` | String |
| `last_seen` | DateTime |
| `created_at` | DateTime |

---

### 2. `UserProfile`

| فیلد | نوع | توضیح |
|------|-----|--------|
| `id` | UUID / Integer | کلید اصلی |
| `user_id` | FK → User | ربط به یوزر |
| `display_name` | String | نام نمایشی |
| `bio` | Text | بیو |
| `avatar_url` | String | آواتار |
| `created_at` | DateTime | تاریخ ساخت پروفایل |
| `updated_at` | DateTime | زمان آخرین تغییرات |


---


### 3. `Room`
روم‌های صوتی/چت

| فیلد | نوع | توضیح |
|------|-----|--------|
| `id` | UUID / Integer | کلید اصلی |
| `name` | String | نام روم |
| `description` | String (nullable) | توضیح درباره روم |
| `is_private` | Boolean | آیا روم خصوصی است؟ |
| `owner_id` | FK → User | سازنده روم |
| `created_at` | DateTime | زمان ساخت روم |

---

### 4. `RoomMember`
عضویت کاربر در روم (برای پیوستن به روم)

| فیلد | نوع | توضیح |
|------|-----|--------|
| `id` | UUID / Integer | کلید اصلی |
| `room_id` | FK → Room | ربط به روم |
| `user_id` | FK → User | ربط به کاربر |
| `joined_at` | DateTime | زمان پیوستن |
| `is_muted` | Boolean | آیا کاربر میوت است؟ (برای آینده) |
| `is_admin` | Boolean | نقش مدیریت در روم (برای بعداً) |

---

### 5. `Message`
پیام‌های متنی داخل روم‌ها

| فیلد | نوع | توضیح |
|------|-----|--------|
| `id` | UUID / Integer | کلید اصلی |
| `room_id` | FK → Room | ربط به روم |
| `sender_id` | FK → User | فرستنده پیام |
| `content` | Text | محتوای پیام |
| `created_at` | DateTime | زمان ارسال پیام |

---

### 6. `Music`
موزیک‌هایی که توسط کاربران آپلود می‌شن

| فیلد | نوع | توضیح |
|------|-----|--------|
| `id` | UUID / Integer | کلید اصلی |
| `title` | String | عنوان موزیک |
| `file_url` | String | آدرس فایل آپلودشده |
| `uploaded_by_id` | FK → User | آپلودکننده موزیک |
| `room_id` | FK → Room (nullable) | اگه موزیک برای روم خاصی باشه |
| `uploaded_at` | DateTime | زمان آپلود |

---

## 🔗 روابط بین Entityها

```
User 1⟶∞ Room (owner_id)
User 1⟶1 UserProfile
User ∞⟷∞ Room (از طریق RoomMember)
Room 1⟶∞ Message
Room 1⟶∞ Music
User 1⟶∞ Message
User 1⟶∞ Music
```

---

## 🧠 نکات قابل توسعه در آینده:
- اضافه کردن `Role` به `RoomMember` برای ACL
- اضافه کردن `FriendRequest` برای دوستی واقعی
- اضافه کردن `Notification` برای نوتیف‌های رویدادها
- افزودن `PlaybackStatus` برای همگام‌سازی موزیک‌ها در روم

---

---

## 📎 نکته درباره وضعیت آنلاین

برای MVP، پیشنهاد می‌کنم فقط `last_seen` داشته باشیم و از رویش بفهمیم کی آنلاین بوده.  
در نسخه‌های بعد می‌تونی با WebSocket یا Redis Presence Tracking وضعیت آنلاین/آفلاین رو real-time نگه داری.

---
