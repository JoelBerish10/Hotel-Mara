"""
Hotel Mara – Web Application
Uses ONLY Python standard-library modules:
  http.server, webbrowser, csv, json, urllib.parse, threading, os, time, datetime
Run:  python Hotel_Mara_Web.py
Then the browser opens automatically at http://localhost:8765
"""

import csv
import json
import os
import threading
import time
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

# ─────────────────────────────────────────────
#  FILE PATHS
# ─────────────────────────────────────────────
MENU_FILE    = "Menu.csv"
DELETED_FILE = "DeletedRecords.csv"
BILL_FILE    = "bill.csv"
ORDERS_FILE  = "orders.json"

ADMIN_CREDENTIALS = {"Jolebaba": "bankai", "Skibdi": "bankai", "Joash": "bankai"}

DEFAULT_MENU = [
    ["Balsamic Glazed Lamb Chops", 300, "Succulent lamb chops seared to perfection and coated in a tangy-sweet balsamic glaze with hints of garlic, honey, and rosemary.", "Hotel Sunshine Special"],
    ["Mango Tango Shrimp Tacos", 250, "Juicy shrimp infused with tropical mango salsa, nestled in warm tortillas, creating a vibrant explosion of flavors.", "Hotel Sunshine Special"],
    ["Garden Delight Stir-Fry", 150, "A vibrant medley of fresh vegetables stir-fried to perfection, seasoned with aromatic spices for a burst of flavor.", "Hotel Sunshine Special"],
    ["Savory Spinach and Ricotta Ravioli", 160, "Handmade ravioli stuffed with creamy ricotta cheese and spinach, served in a light herb-infused sauce.", "Hotel Sunshine Special"],
    ["Dreamy Chocolate Avalanche", 250, "Layers of indulgent chocolate bliss, topped with edible gold.", "Hotel Sunshine Special"],
    ["Blissful Berry Symphony", 270, "A harmonious medley of fresh berries layered atop delicate sponge cake, drizzled with a luscious berry reduction.", "Hotel Sunshine Special"],
    ["Chicken 65", 110, "Spicy, crispy fried chicken tossed with chilies, garlic, and aromatic spices for a bold, flavorful kick.", "Starters"],
    ["Chicken Wings", 120, "Juicy chicken wings, drenched and marinated, then deep-fried to perfection.", "Starters"],
    ["Chicken Tikka", 150, "Tender pieces of marinated chicken grilled to perfection, bursting with smoky and aromatic flavors.", "Starters"],
    ["Veg Crispy", 100, "Crispy and flavorful deep-fried vegetables coated in a crunchy batter.", "Starters"],
    ["Mushroom n Pepper Fry", 110, "Sauteed mushrooms and peppers seasoned with aromatic spices.", "Starters"],
    ["Paneer Chilli", 120, "Cubes of paneer tossed in a spicy and tangy sauce with peppers and onions.", "Starters"],
    ["Idli", 60, "Two idlis along with sambar and coconut chutney.", "South Indian"],
    ["Masala Dosa", 80, "Two masala dosas overloaded with potato filling along with chutney.", "South Indian"],
    ["Uttapam", 100, "Two uttapam with veggies on top along with tomato chutney.", "South Indian"],
    ["Medu Vada", 80, "4 medu vadas along with sambar and coconut chutney.", "South Indian"],
    ["Parotta with Mutton Curry", 160, "Four parottas with spicy mutton curry made from a blend of spices and tender mutton pieces.", "South Indian"],
    ["Chinese Bhel", 30, "Crispy noodles, colorful veggies, and tangy sauces - a unique twist on Indian street food.", "Chinese Ching"],
    ["Momos", 70, "Savory dumplings filled with seasoned vegetables, steamed to perfection with spicy dipping sauce.", "Chinese Ching"],
    ["Schezwan Fried Rice", 180, "A fiery blend of rice, vegetables, and spicy Schezwan sauce, wok-fried to perfection.", "Chinese Ching"],
    ["Hakka Noodles", 90, "Stir-fried noodles tossed with crispy vegetables and savory sauces.", "Chinese Ching"],
    ["Manchurian Gravy", 120, "A savory and tangy Chinese-style sauce enveloping fried vegetable balls.", "Chinese Ching"],
    ["Palak Paneer", 150, "Creamy spinach curry with chunks of soft paneer, infused with aromatic spices.", "Vegetarian Verna"],
    ["Paneer Tikka Masala", 120, "Tender paneer cubes grilled and simmered in a rich, creamy tomato-based masala sauce.", "Vegetarian Verna"],
    ["Mutter Paneer", 110, "Soft paneer cubes and tender peas cooked in a flavorful tomato-based gravy.", "Vegetarian Verna"],
    ["Dal Tadka", 100, "Creamy lentils tempered with aromatic spices.", "Vegetarian Verna"],
    ["Veg Biryani", 130, "Fragrant basmati rice cooked with an assortment of vegetables and aromatic spices.", "Vegetarian Verna"],
    ["Butter Chicken", 150, "Tender chicken simmered in a creamy, tomato-based sauce infused with rich spices.", "Non-Vegetarian Delicacies"],
    ["Mutton Handi", 180, "Succulent pieces of mutton cooked in a rich and aromatic gravy in a traditional clay pot.", "Non-Vegetarian Delicacies"],
    ["Nalli Nihari", 190, "Tender lamb shanks slow-cooked in a flavorful gravy infused with aromatic spices.", "Non-Vegetarian Delicacies"],
    ["Chicken Biryani", 200, "Fragrant basmati rice cooked with succulent chicken pieces and aromatic spices.", "Non-Vegetarian Delicacies"],
    ["Gulab Jamun", 60, "Soft and syrupy milk-based balls infused with cardamom, rose water, and saffron.", "Desserts and Beverages"],
    ["Ras Malai", 80, "Soft and creamy cheese dumplings soaked in sweetened, flavored milk, garnished with nuts.", "Desserts and Beverages"],
    ["Jalebi", 50, "Crispy, deep-fried swirls of dough soaked in sugary syrup.", "Desserts and Beverages"],
    ["Citrus Splash", 120, "A refreshing blend of citrus fruits, bursting with tangy and zesty flavors.", "Desserts and Beverages"],
    ["Mango Mania", 140, "A tropical explosion of ripe mangoes, delivering a sweet and juicy burst of flavor.", "Desserts and Beverages"],
    ["Berry Blast Elixir", 160, "A vibrant fusion of assorted berries, creating a refreshing and invigorating drink.", "Desserts and Beverages"],
    ["Roti", 10, "Traditional Indian flatbread, perfectly baked to be soft and fluffy.", "Add Ons"],
    ["Kulcha", 15, "Soft, leavened bread, often served with curries and dals.", "Add Ons"],
    ["Butter Naan", 15, "A rich and soft flatbread brushed with butter.", "Add Ons"],
    ["Garlic Butter Naan", 18, "Delicious naan infused with garlic and a touch of butter.", "Add Ons"],
    ["Rumali Roti", 15, "Thin and soft Indian bread, known for its light texture.", "Add Ons"],
    ["Parotta", 18, "Flaky and layered bread, known for its crispy texture.", "Add Ons"],
]

# ─────────────────────────────────────────────
#  STORAGE HELPERS
# ─────────────────────────────────────────────
def init_storage():
    if not os.path.exists(MENU_FILE):
        with open(MENU_FILE, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Item Name", "Price", "Description", "Cuisine"])
            w.writerows(DEFAULT_MENU)
    if not os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

def read_menu():
    init_storage()
    rows = []
    with open(MENU_FILE, "r", encoding="utf-8") as f:
        rd = csv.reader(f)
        next(rd, None)
        for row in rd:
            if len(row) >= 4:
                rows.append({"name": row[0], "price": row[1], "desc": row[2], "cuisine": row[3]})
    return rows

def write_menu_rows(rows):
    with open(MENU_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Item Name", "Price", "Description", "Cuisine"])
        for r in rows:
            w.writerow([r["name"], r["price"], r["desc"], r["cuisine"]])

def read_orders():
    init_storage()
    try:
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def write_orders(orders):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, indent=2, ensure_ascii=False)

def read_bill_csv():
    rows = []
    if os.path.exists(BILL_FILE):
        with open(BILL_FILE, "r", encoding="utf-8") as f:
            rd = csv.reader(f)
            next(rd, None)
            for row in rd:
                if len(row) >= 4:
                    rows.append({"name": row[0], "qty": row[1], "price": row[2], "amount": row[3]})
    return rows

def compute_order_status(order):
    """Compute dynamic order progression if not manually finalized."""
    if order.get("manual_status"):
        return order["manual_status"]
    
    elapsed = time.time() - order.get("created_at", time.time())
    is_delivery = order.get("order_type") == "delivery"

    if elapsed < 90:        # 0 to 1.5 mins
        return "Order Placed & Confirmed"
    elif elapsed < 300:     # 1.5 to 5 mins
        return "Preparing in Kitchen"
    elif elapsed < 600:     # 5 to 10 mins
        return "Packed & Quality Checked" if is_delivery else "Quality Check & Plating"
    elif elapsed < 900:     # 10 to 15 mins
        return "Out for Delivery (Rider on the Way)" if is_delivery else "Ready for Serving"
    else:
        return "Delivered to Customer" if is_delivery else "Served & Completed"

# ─────────────────────────────────────────────
#  HTML/CSS/JS SINGLE-PAGE APPLICATION
# ─────────────────────────────────────────────
HTML_PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Hotel Mara — Exquisite Dining, Online Food Delivery & Management</title>
<meta name="description" content="Hotel Mara Thane — order food online with doorstep delivery, live tracking, and Dine-In booking."/>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

  :root {
    --bg: #0B0E17;
    --card: #121829;
    --panel: #18223C;
    --panel-hover: #1F2C4E;
    --border: #233152;
    --border-light: #2D3E66;
    --text: #F1F5F9;
    --text-muted: #94A3B8;
    --gold: #D4AF37;
    --gold-light: #F3E5AB;
    --gold-glow: rgba(212, 175, 55, 0.25);
    --accent: #38BDF8;
    --green: #10B981;
    --red: #EF4444;
    --orange: #F59E0B;
    --shadow: 0 10px 30px -5px rgba(0,0,0,0.5);
    --font-serif: 'Playfair Display', Georgia, serif;
    --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  }

  body.light-theme {
    --bg: #F8FAFC;
    --card: #FFFFFF;
    --panel: #F1F5F9;
    --panel-hover: #E2E8F0;
    --border: #E2E8F0;
    --border-light: #CBD5E1;
    --text: #0F172A;
    --text-muted: #64748B;
    --gold: #B8860B;
    --gold-light: #805B00;
    --gold-glow: rgba(184, 134, 11, 0.2);
    --accent: #0284C7;
    --green: #059669;
    --red: #DC2626;
    --orange: #D97706;
    --shadow: 0 10px 30px -5px rgba(15,23,42,0.08);
  }

  * { margin:0; padding:0; box-sizing:border-box; transition: background-color 0.25s ease, border-color 0.25s ease, color 0.2s ease; }
  body {
    font-family: var(--font-sans);
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    overflow-x: hidden;
  }

  /* ── Sidebar ── */
  #sidebar {
    width: 250px;
    min-height: 100vh;
    background: var(--card);
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
    border-right: 1px solid var(--border);
    position: relative;
    z-index: 10;
  }
  #sidebar .logo {
    padding: 28px 22px 20px;
    border-bottom: 1px solid var(--border);
    background: linear-gradient(180deg, var(--panel) 0%, var(--card) 100%);
  }
  #sidebar .logo .badge {
    display: inline-block;
    font-size: 0.48rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.2px;
    color: var(--gold);
    background: var(--gold-glow);
    padding: 3px 5px;
    border-radius: 20px;
    margin-bottom: 6px;
    border: 1px solid var(--gold);
    white-space: nowrap;
  }
  #sidebar .logo h1 {
    font-family: var(--font-serif);
    color: var(--gold);
    font-size: 1.5rem;
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  #sidebar .logo p {
    font-size: 0.74rem;
    color: var(--text-muted);
    margin-top: 4px;
  }

  #sidebar nav {
    padding: 18px 12px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    flex: 1;
  }
  #sidebar nav a {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    color: var(--text-muted);
    text-decoration: none;
    font-size: 0.92rem;
    font-weight: 500;
    border-radius: 10px;
    transition: all 0.2s;
  }
  #sidebar nav a .icon { font-size: 1.15rem; }
  #sidebar nav a:hover {
    color: var(--text);
    background: var(--panel);
  }
  #sidebar nav a.active {
    color: var(--gold);
    background: var(--panel);
    font-weight: 600;
    box-shadow: inset 3px 0 0 var(--gold);
  }
  #sidebar .nav-bottom {
    padding: 16px 14px;
    border-top: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  /* ── Theme Switcher ── */
  .theme-toggle-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 9px 12px;
    color: var(--text);
    cursor: pointer;
    font-size: 0.85rem;
    font-weight: 600;
  }
  .theme-toggle-btn:hover {
    border-color: var(--gold);
    background: var(--panel-hover);
  }

  #staff-login-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    font-size: 0.78rem;
    color: var(--text-muted);
    background: transparent;
    border: 1px dashed var(--border);
    border-radius: 6px;
    padding: 8px;
    cursor: pointer;
    text-decoration: none;
  }
  #staff-login-btn:hover {
    color: var(--gold);
    border-color: var(--gold);
  }

  #cart-badge {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 0.85rem;
    color: var(--gold);
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
  }
  #cart-badge:hover {
    border-color: var(--gold);
    transform: translateY(-1px);
  }

  /* ── Main Content Area ── */
  #main {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    height: 100vh;
  }
  .page {
    display: none;
    flex: 1;
    flex-direction: column;
    animation: fadeIn 0.25s ease-out;
  }
  .page.active {
    display: flex;
  }
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(4px); }
    to { opacity: 1; transform: translateY(0); }
  }

  /* ── Topbar ── */
  .topbar {
    background: var(--card);
    padding: 16px 36px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 5;
  }
  .topbar h2 {
    font-family: var(--font-serif);
    color: var(--gold);
    font-size: 1.5rem;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .topbar-actions {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  /* ── Buttons ── */
  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 10px 22px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    font-family: var(--font-sans);
    font-size: 0.88rem;
    font-weight: 600;
    transition: all 0.2s;
    text-decoration: none;
  }
  .btn-gold {
    background: linear-gradient(135deg, #D4AF37 0%, #AA820A 100%);
    color: #0B0E17;
    box-shadow: 0 4px 14px var(--gold-glow);
  }
  .btn-gold:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4);
  }
  .btn-green { background: var(--green); color: #fff; }
  .btn-green:hover { filter: brightness(1.1); transform: translateY(-1px); }
  .btn-red { background: var(--red); color: #fff; }
  .btn-red:hover { filter: brightness(1.1); transform: translateY(-1px); }
  .btn-panel {
    background: var(--panel);
    color: var(--text);
    border: 1px solid var(--border);
  }
  .btn-panel:hover {
    border-color: var(--gold);
    color: var(--gold);
    background: var(--panel-hover);
  }
  .btn-sm { padding: 6px 14px; font-size: 0.82rem; }

  /* ── HOME PAGE ── */
  #home .hero {
    background: linear-gradient(180deg, var(--panel) 0%, var(--bg) 100%);
    padding: 56px 40px 48px;
    text-align: center;
    border-bottom: 1px solid var(--border);
    position: relative;
    overflow: hidden;
  }
  #home .hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: 50%;
    transform: translateX(-50%);
    width: 600px;
    height: 300px;
    background: radial-gradient(circle, var(--gold-glow) 0%, transparent 70%);
    pointer-events: none;
  }
  #home .hero .stars { color: var(--gold); font-size: 1.1rem; letter-spacing: 4px; margin-bottom: 8px; }
  #home .hero h1 {
    font-family: var(--font-serif);
    color: var(--gold);
    font-size: 2.9rem;
    letter-spacing: 1px;
    margin-bottom: 8px;
  }
  #home .hero p.location {
    color: var(--text-muted);
    font-size: 0.95rem;
    font-style: italic;
    margin-bottom: 12px;
  }
  #home .hero .tagline {
    color: var(--text);
    font-size: 1.1rem;
    max-width: 650px;
    margin: 0 auto 24px;
    font-weight: 400;
  }

  /* ── Quick Tracker Box on Home ── */
  .quick-tracker-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 24px;
    max-width: 550px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    gap: 12px;
    box-shadow: var(--shadow);
  }
  .quick-tracker-card input {
    flex: 1;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 14px;
    color: var(--text);
    font-size: 0.9rem;
    outline: none;
  }
  .quick-tracker-card input:focus { border-color: var(--gold); }

  /* ── Customer Feature Cards ── */
  .home-cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 24px;
    padding: 40px;
    max-width: 1200px;
    margin: 0 auto;
    width: 100%;
  }
  .home-feature-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 32px 28px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    box-shadow: var(--shadow);
    transition: all 0.25s;
    position: relative;
    overflow: hidden;
  }
  .home-feature-card:hover {
    transform: translateY(-6px);
    border-color: var(--gold);
    box-shadow: 0 16px 36px var(--gold-glow);
  }
  .home-feature-card .card-icon {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: var(--panel);
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
    margin-bottom: 20px;
    color: var(--gold);
  }
  .home-feature-card h3 {
    font-family: var(--font-serif);
    font-size: 1.4rem;
    color: var(--text);
    margin-bottom: 10px;
  }
  .home-feature-card p {
    color: var(--text-muted);
    font-size: 0.88rem;
    line-height: 1.6;
    margin-bottom: 24px;
    flex: 1;
  }

  .home-section-title {
    padding: 0 40px 12px;
    font-family: var(--font-serif);
    color: var(--gold);
    font-size: 1.25rem;
    max-width: 1200px;
    margin: 0 auto;
    width: 100%;
  }
  .tags-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    padding: 0 40px 48px;
    max-width: 1200px;
    margin: 0 auto;
    width: 100%;
  }
  .tag {
    background: var(--card);
    color: var(--gold);
    border: 1px solid var(--border);
    border-radius: 30px;
    padding: 8px 18px;
    font-size: 0.85rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
  }
  .tag:hover {
    background: var(--gold);
    color: #0B0E17;
    border-color: var(--gold);
  }

  /* ── ORDER FOOD PAGE ── */
  #order .body {
    display: flex;
    flex: 1;
    overflow: hidden;
  }
  #order .menu-area {
    flex: 1;
    overflow-y: auto;
    padding: 20px 28px;
  }
  .search-and-tabs {
    padding: 16px 28px 0;
    background: var(--card);
    border-bottom: 1px solid var(--border);
  }
  .menu-search-bar {
    margin-bottom: 14px;
    position: relative;
    max-width: 460px;
  }
  .menu-search-bar input {
    width: 100%;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 14px 10px 38px;
    color: var(--text);
    font-size: 0.88rem;
    outline: none;
  }
  .menu-search-bar input:focus { border-color: var(--gold); }
  .menu-search-bar .search-icon {
    position: absolute;
    left: 12px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-muted);
  }
  .cuisine-tabs {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    padding-bottom: 14px;
  }
  .ctab {
    padding: 7px 16px;
    border-radius: 20px;
    border: 1px solid var(--border);
    background: var(--panel);
    color: var(--text-muted);
    cursor: pointer;
    font-size: 0.82rem;
    font-weight: 500;
    transition: all 0.2s;
  }
  .ctab.active, .ctab:hover {
    background: var(--gold);
    color: #0B0E17;
    border-color: var(--gold);
    font-weight: 600;
  }

  .menu-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 16px;
  }
  .menu-item {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.2s;
    box-shadow: var(--shadow);
  }
  .menu-item:hover {
    border-color: var(--gold);
    transform: translateY(-2px);
  }
  .menu-item .info h4 {
    color: var(--text);
    font-size: 1.05rem;
    font-weight: 600;
    margin-bottom: 6px;
  }
  .menu-item .info .price {
    color: var(--gold);
    font-weight: 700;
    font-size: 1.15rem;
    margin-bottom: 8px;
  }
  .menu-item .info .desc {
    color: var(--text-muted);
    font-size: 0.82rem;
    line-height: 1.55;
    margin-bottom: 16px;
  }
  .menu-item .actions {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 12px;
    border-top: 1px solid var(--border);
  }
  .qty-ctrl {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .qty-ctrl button {
    width: 30px;
    height: 30px;
    border-radius: 6px;
    border: 1px solid var(--border);
    background: var(--panel);
    color: var(--text);
    cursor: pointer;
    font-size: 1.1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    transition: all 0.2s;
  }
  .qty-ctrl button:hover {
    background: var(--gold);
    color: #0B0E17;
    border-color: var(--gold);
  }
  .qty-ctrl span {
    min-width: 26px;
    text-align: center;
    font-weight: 700;
    font-size: 0.95rem;
  }

  /* ── Right Cart Panel ── */
  #cart-panel {
    width: 320px;
    background: var(--card);
    border-left: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  #cart-panel h3 {
    padding: 18px 20px;
    font-family: var(--font-serif);
    color: var(--gold);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  #cart-items {
    flex: 1;
    overflow-y: auto;
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .cart-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    padding: 10px 12px;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 8px;
  }
  .cart-row .cname { font-size: 0.84rem; font-weight: 500; color: var(--text); flex: 1; }
  .cart-row .camt { font-size: 0.85rem; font-weight: 700; color: var(--gold); white-space: nowrap; }
  .cart-row .cdel {
    background: none;
    border: none;
    cursor: pointer;
    color: var(--red);
    font-size: 1.1rem;
    padding: 2px 6px;
    border-radius: 4px;
  }
  .cart-row .cdel:hover { background: rgba(239,68,68,0.15); }
  #cart-total {
    padding: 16px 20px;
    border-top: 1px solid var(--border);
    font-size: 0.88rem;
    color: var(--text-muted);
    background: var(--panel);
    line-height: 1.6;
  }
  #cart-total strong { color: var(--gold); font-size: 1.15rem; }
  #cart-actions {
    padding: 14px 20px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    border-top: 1px solid var(--border);
  }

  /* ── BILL / CHECKOUT / INVOICE PAGE ── */
  #bill .inner {
    padding: 32px 40px;
    max-width: 860px;
    width: 100%;
    margin: 0 auto;
  }
  .checkout-section {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 24px;
    box-shadow: var(--shadow);
  }
  .checkout-section h3 {
    font-family: var(--font-serif);
    color: var(--gold);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  /* ── Order Type Switcher Tabs ── */
  .order-type-tabs {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
    margin-bottom: 20px;
  }
  .order-type-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 14px 10px;
    background: var(--panel);
    border: 2px solid var(--border);
    border-radius: 10px;
    color: var(--text-muted);
    cursor: pointer;
    font-weight: 600;
    font-size: 0.88rem;
    transition: all 0.2s;
  }
  .order-type-btn .type-icon { font-size: 1.5rem; }
  .order-type-btn.active {
    border-color: var(--gold);
    color: var(--gold);
    background: var(--gold-glow);
    box-shadow: 0 4px 16px rgba(212, 175, 55, 0.15);
  }

  .form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }
  .form-group { margin-bottom: 16px; }
  .form-group label {
    display: block;
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--text-muted);
    margin-bottom: 6px;
  }
  .form-group input, .form-group select, .form-group textarea {
    width: 100%;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 14px;
    color: var(--text);
    font-family: var(--font-sans);
    font-size: 0.9rem;
    outline: none;
    transition: border-color 0.2s;
  }
  .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
    border-color: var(--gold);
  }

  .bill-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 16px;
  }
  .bill-table th {
    background: var(--panel);
    color: var(--gold);
    padding: 12px 16px;
    text-align: left;
    font-size: 0.88rem;
    border-bottom: 1px solid var(--border);
  }
  .bill-table td {
    padding: 12px 16px;
    font-size: 0.88rem;
    border-bottom: 1px solid var(--border);
  }
  .bill-table tr:nth-child(even) td { background: rgba(0,0,0,0.03); }

  .totals-box {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px 24px;
    margin-bottom: 20px;
  }
  .totals-box .trow {
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
    font-size: 0.92rem;
    color: var(--text-muted);
  }
  .totals-box .trow.grand {
    color: var(--gold);
    font-family: var(--font-serif);
    font-size: 1.35rem;
    font-weight: 700;
    border-top: 1px solid var(--border);
    margin-top: 8px;
    padding-top: 12px;
  }

  /* ── ORDER TRACKING PAGE ── */
  #track .inner {
    padding: 32px 40px;
    max-width: 900px;
    width: 100%;
    margin: 0 auto;
  }
  .track-search-bar {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 24px;
    display: flex;
    gap: 12px;
    align-items: center;
    box-shadow: var(--shadow);
  }
  .track-search-bar input {
    flex: 1;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 14px;
    color: var(--text);
    font-size: 0.92rem;
    outline: none;
  }
  .track-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 32px;
    margin-bottom: 24px;
    box-shadow: var(--shadow);
  }
  .track-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border);
    padding-bottom: 20px;
    margin-bottom: 28px;
    flex-wrap: wrap;
    gap: 12px;
  }
  .track-header .order-num {
    font-family: var(--font-serif);
    font-size: 1.6rem;
    color: var(--gold);
  }
  .status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .status-placed { background: rgba(56, 189, 248, 0.15); color: #38BDF8; border: 1px solid #38BDF8; }
  .status-kitchen { background: rgba(245, 158, 11, 0.15); color: #F59E0B; border: 1px solid #F59E0B; }
  .status-plating { background: rgba(168, 85, 247, 0.15); color: #A855F7; border: 1px solid #A855F7; }
  .status-ready { background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid #10B981; }
  .status-delivered { background: rgba(16, 185, 129, 0.25); color: #10B981; border: 1px solid #10B981; }
  .status-cancelled { background: rgba(239, 68, 68, 0.15); color: #EF4444; border: 1px solid #EF4444; }

  /* ── Timeline Stepper ── */
  .timeline {
    display: flex;
    justify-content: space-between;
    position: relative;
    margin: 40px 0 32px;
  }
  .timeline::before {
    content: '';
    position: absolute;
    top: 22px;
    left: 40px;
    right: 40px;
    height: 4px;
    background: var(--border);
    z-index: 1;
  }
  .timeline-progress-bar {
    position: absolute;
    top: 22px;
    left: 40px;
    height: 4px;
    background: linear-gradient(90deg, var(--gold) 0%, var(--green) 100%);
    z-index: 2;
    transition: width 0.5s ease;
  }
  .step-node {
    position: relative;
    z-index: 3;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    width: 100px;
  }
  .step-circle {
    width: 46px;
    height: 46px;
    border-radius: 50%;
    background: var(--card);
    border: 3px solid var(--border);
    color: var(--text-muted);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    margin-bottom: 10px;
    transition: all 0.3s;
  }
  .step-node.active .step-circle {
    border-color: var(--gold);
    background: var(--panel);
    color: var(--gold);
    box-shadow: 0 0 15px var(--gold-glow);
    animation: pulse 2s infinite;
  }
  .step-node.completed .step-circle {
    border-color: var(--green);
    background: var(--green);
    color: #fff;
  }
  .step-title {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-muted);
  }
  .step-node.active .step-title { color: var(--gold); }
  .step-node.completed .step-title { color: var(--green); }

  @keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.08); }
    100% { transform: scale(1); }
  }

  /* ── ADMIN LOGIN ── */
  #admin-login .center {
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 1;
    padding: 40px;
  }
  #admin-login .login-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 42px 48px;
    width: 100%;
    max-width: 440px;
    box-shadow: var(--shadow);
  }
  #admin-login .login-card h2 {
    font-family: var(--font-serif);
    color: var(--gold);
    margin-bottom: 8px;
    text-align: center;
  }
  .err-msg { color: var(--red); font-size: 0.85rem; margin: 10px 0; font-weight: 500; }
  .ok-msg { color: var(--green); font-size: 0.85rem; margin: 10px 0; font-weight: 500; }

  /* ── ADMIN PANEL ── */
  #admin-panel .ap-body {
    display: flex;
    flex: 1;
    overflow: hidden;
  }
  .ap-tabs {
    display: flex;
    gap: 6px;
    padding: 14px 28px;
    background: var(--card);
    border-bottom: 1px solid var(--border);
    overflow-x: auto;
  }
  .aptab {
    padding: 9px 20px;
    border-radius: 8px;
    border: 1px solid var(--border);
    background: var(--panel);
    color: var(--text-muted);
    cursor: pointer;
    font-size: 0.88rem;
    font-weight: 600;
    transition: all 0.2s;
    white-space: nowrap;
  }
  .aptab.active, .aptab:hover {
    background: var(--gold);
    color: #0B0E17;
    border-color: var(--gold);
  }
  .ap-content {
    flex: 1;
    overflow-y: auto;
    padding: 24px 32px;
  }
  .menu-table {
    width: 100%;
    border-collapse: collapse;
    background: var(--card);
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--border);
  }
  .menu-table th {
    background: var(--panel);
    color: var(--gold);
    padding: 12px 16px;
    text-align: left;
    font-size: 0.85rem;
    font-weight: 600;
    border-bottom: 1px solid var(--border);
  }
  .menu-table td {
    padding: 12px 16px;
    font-size: 0.85rem;
    border-bottom: 1px solid var(--border);
    vertical-align: top;
  }
  .menu-table tr:nth-child(even) td { background: rgba(0,0,0,0.02); }

  /* ── Toast ── */
  #toast {
    position: fixed;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%) translateY(100px);
    background: var(--card);
    border: 1px solid var(--gold);
    border-radius: 10px;
    padding: 14px 26px;
    font-size: 0.92rem;
    color: var(--text);
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    transition: transform 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    z-index: 9999;
    font-weight: 500;
  }
  #toast.show { transform: translateX(-50%) translateY(0); }

  /* ── Responsive ── */
  @media(max-width: 820px) {
    #sidebar { display: none; }
    #cart-panel { width: 100%; border-left: none; border-top: 1px solid var(--border); }
    #order .body { flex-direction: column; }
    .form-row { grid-template-columns: 1fr; }
    .timeline { flex-wrap: wrap; gap: 20px; }
    .timeline::before, .timeline-progress-bar { display: none; }
    .order-type-tabs { grid-template-columns: 1fr; }
  }
</style>
</head>
<body>

<!-- SIDEBAR -->
<aside id="sidebar">
  <div class="logo">
    <span class="badge">Fine Dining & Express Delivery</span>
    <h1>&#127869; Hotel Mara</h1>
    <p>Near Thane Railway Station &bull; 400614</p>
  </div>
  <nav>
    <a href="#" class="active" id="nav-home" onclick="showPage('home',this)"><span class="icon">&#127968;</span> Home</a>
    <a href="#" id="nav-order" onclick="showPage('order',this)"><span class="icon">&#128722;</span> Order Food</a>
    <a href="#" id="nav-bill" onclick="showPage('bill',this)"><span class="icon">&#129534;</span> View Bill / Checkout</a>
    <a href="#" id="nav-track" onclick="showPage('track',this)"><span class="icon">&#128205;</span> Track Order</a>
  </nav>

  <div class="nav-bottom">
    <div id="cart-badge" onclick="showPage('order',null)">
      <span>&#128722; Basket</span>
      <span id="cart-count">0 items</span>
    </div>
    <button class="theme-toggle-btn" onclick="toggleTheme()">
      <span id="theme-icon">&#9728;&#65039;</span>
      <span id="theme-text">Light Mode</span>
    </button>
    <a href="#" id="staff-login-btn" onclick="showPage('admin-login',null)">&#128274; Staff / Admin Portal</a>
  </div>
</aside>

<!-- MAIN APP BODY -->
<main id="main">

  <!-- 1. HOME PAGE (Customer-Facing Only) -->
  <section id="home" class="page active">
    <div class="hero">
      <div class="stars">&#9733; &#9733; &#9733; &#9733; &#9733;</div>
      <h1>Hotel Mara</h1>
      <p class="location">"Close to Thane Railway Station &nbsp;|&nbsp; Thane — 400614"</p>
      <div class="tagline">An exquisite culinary journey with <strong>Doorstep Online Delivery</strong>, dine-in comfort, and authentic global specialties.</div>

      <!-- Quick Tracker Box -->
      <div class="quick-tracker-card">
        <input id="quick-track-id" type="text" placeholder="Have an Order ID? e.g. HM-1001" onkeydown="if(event.key==='Enter')trackQuickOrder()"/>
        <button class="btn btn-gold btn-sm" onclick="trackQuickOrder()">Track Order &#10140;</button>
      </div>
    </div>

    <!-- Feature Cards -->
    <div class="home-cards-grid">
      <div class="home-feature-card">
        <div class="card-icon">&#128757;</div>
        <h3>Online Home Delivery</h3>
        <p>Order your favorite meals online for fast, hot doorstep delivery anywhere in Thane with Cash on Delivery!</p>
        <button class="btn btn-green" onclick="selectedOrderType='delivery';showPage('order',null)">Order Online Now &#8594;</button>
      </div>

      <div class="home-feature-card">
        <div class="card-icon">&#129534;</div>
        <h3>View Bill & Invoice</h3>
        <p>Review your active basket, checkout with custom delivery address & phone number, or download past invoices.</p>
        <button class="btn btn-gold" onclick="showPage('bill',null)">View Your Bill &#8594;</button>
      </div>

      <div class="home-feature-card">
        <div class="card-icon">&#128205;</div>
        <h3>Live Order Tracking</h3>
        <p>Real-time delivery & kitchen tracking — see when your order is placed, prepared, and out for delivery!</p>
        <button class="btn btn-panel" onclick="showPage('track',null)">Track Order &#8594;</button>
      </div>
    </div>

    <div class="home-section-title">Explore Our Cuisines</div>
    <div class="tags-row" id="cuisine-tags"></div>
  </section>

  <!-- 2. ORDER FOOD PAGE -->
  <section id="order" class="page">
    <div class="topbar">
      <h2>&#128722; Order Food</h2>
      <div class="topbar-actions">
        <button class="btn btn-panel btn-sm" onclick="toggleTheme()">🌓 Toggle Mode</button>
        <button class="btn btn-green" onclick="showPage('bill',null)">Proceed to Bill & Checkout &#129534;</button>
      </div>
    </div>

    <div class="search-and-tabs">
      <div class="menu-search-bar">
        <span class="search-icon">&#128269;</span>
        <input id="menu-search-input" type="text" placeholder="Search dishes, ingredients, or cuisines..." oninput="filterMenuItems()"/>
      </div>
      <div class="cuisine-tabs" id="cuisine-tabs"></div>
    </div>

    <div class="body">
      <div class="menu-area" id="menu-area"></div>

      <!-- Live Cart Panel -->
      <div id="cart-panel">
        <h3>
          <span>&#128722; Your Basket</span>
          <span style="font-size:0.8rem;color:var(--text-muted);" id="cart-items-counter">0 items</span>
        </h3>
        <div id="cart-items"></div>
        <div id="cart-total">
          Subtotal: Rs. 0.00<br>
          GST (5%): Rs. 0.00<br>
          <strong>Total: Rs. 0.00</strong>
        </div>
        <div id="cart-actions">
          <button class="btn btn-green" style="width:100%" onclick="showPage('bill',null)">Checkout Bill &#10140;</button>
          <button class="btn btn-panel btn-sm" style="width:100%" onclick="clearCart()">Empty Basket</button>
        </div>
      </div>
    </div>
  </section>

  <!-- 3. VIEW BILL / CHECKOUT / INVOICE PAGE -->
  <section id="bill" class="page">
    <div class="topbar">
      <h2>&#129534; Order Summary & Checkout</h2>
      <div class="topbar-actions">
        <button class="btn btn-panel btn-sm" onclick="showPage('order',null)">&#8592; Back to Menu</button>
      </div>
    </div>

    <div class="inner" id="bill-container">
      <!-- Dynamically filled with either Online/Dine-In Checkout or Confirmed Order Invoice -->
    </div>
  </section>

  <!-- 4. LIVE ORDER TRACKING PAGE -->
  <section id="track" class="page">
    <div class="topbar">
      <h2>&#128205; Live Order Tracker</h2>
      <button class="btn btn-gold btn-sm" onclick="showPage('order',null)">+ New Order</button>
    </div>

    <div class="inner">
      <div class="track-search-bar">
        <span style="font-size:1.1rem;color:var(--gold);">&#128269;</span>
        <input id="track-search-input" type="text" placeholder="Enter Order ID to track (e.g. HM-1001)..."/>
        <button class="btn btn-gold btn-sm" onclick="lookupOrder()">Track</button>
      </div>

      <div id="track-result-container">
        <!-- Dynamically rendered active order tracking card -->
      </div>
    </div>
  </section>

  <!-- 5. ADMIN LOGIN (Protected Portal) -->
  <section id="admin-login" class="page">
    <div class="center">
      <div class="login-card">
        <div style="text-align:center;font-size:2.4rem;margin-bottom:8px;">&#128274;</div>
        <h2>Admin Portal</h2>
        <p style="text-align:center;color:var(--text-muted);font-size:0.84rem;margin-bottom:24px;">Hotel Mara Management & Kitchen Staff Access</p>

        <div class="form-group">
          <label>Admin Username</label>
          <input id="admin-user" type="text" placeholder="Enter username (e.g. Jolebaba)" onkeydown="if(event.key==='Enter')doLogin()"/>
        </div>
        <div class="form-group">
          <label>Secret Password</label>
          <input id="admin-pass" type="password" placeholder="Enter password" onkeydown="if(event.key==='Enter')doLogin()"/>
        </div>
        <div id="login-err" class="err-msg"></div>
        <button class="btn btn-gold" style="width:100%;margin-top:8px;" onclick="doLogin()">Authenticate & Open Dashboard</button>
        <button class="btn btn-panel" style="width:100%;margin-top:10px;" onclick="showPage('home',null)">&#8592; Back to Customer Home</button>
      </div>
    </div>
  </section>

  <!-- 6. ADMIN DASHBOARD -->
  <section id="admin-panel" class="page">
    <div class="topbar">
      <h2>&#128296; Hotel Mara Management</h2>
      <button class="btn btn-red btn-sm" onclick="logoutAdmin()">&#128274; Logout</button>
    </div>

    <div class="ap-tabs">
      <button class="aptab active" onclick="showApTab('orders',this)">&#128230; Live Orders & Deliveries</button>
      <button class="aptab" onclick="showApTab('display',this)">&#128203; Menu Inventory</button>
      <button class="aptab" onclick="showApTab('add',this)">&#10133; Add New Dish</button>
      <button class="aptab" onclick="showApTab('update',this)">&#9998; Edit Dish</button>
      <button class="aptab" onclick="showApTab('delete',this)">&#128465; Delete Dish</button>
    </div>

    <!-- Tab 1: Live Orders -->
    <div id="ap-orders" class="ap-content">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:18px;">
        <h3 style="font-family:var(--font-serif);color:var(--gold);">Incoming Orders & Deliveries</h3>
        <button class="btn btn-panel btn-sm" onclick="loadAdminOrders()">&#8635; Refresh Orders</button>
      </div>
      <div id="admin-orders-list"></div>
    </div>

    <!-- Tab 2: Display Menu -->
    <div id="ap-display" class="ap-content" style="display:none;">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;flex-wrap:wrap;">
        <label style="color:var(--text-muted);font-size:0.85rem;font-weight:600;">Filter by Cuisine:</label>
        <select id="disp-filter" onchange="loadDisplay()" style="background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:8px 12px;color:var(--text);"></select>
        <button class="btn btn-panel btn-sm" onclick="loadDisplay()">&#8635; Refresh</button>
      </div>
      <table class="menu-table">
        <thead><tr><th>Dish Name</th><th>Price (Rs.)</th><th>Cuisine</th><th>Description</th></tr></thead>
        <tbody id="disp-body"></tbody>
      </table>
    </div>

    <!-- Tab 3: Add Item -->
    <div id="ap-add" class="ap-content" style="display:none;max-width:580px;">
      <h3 style="font-family:var(--font-serif);color:var(--gold);margin-bottom:20px;">&#10133; Add Menu Item</h3>
      <div class="form-group"><label>Dish Name *</label><input id="a-name" type="text" placeholder="e.g. Paneer Butter Masala"/></div>
      <div class="form-group"><label>Price in INR (Rs.) *</label><input id="a-price" type="number" min="1" placeholder="e.g. 160"/></div>
      <div class="form-group"><label>Description *</label><textarea id="a-desc" rows="3" placeholder="Flavors, ingredients, serving notes..."></textarea></div>
      <div class="form-group"><label>Cuisine Category *</label><select id="a-cuisine"></select></div>
      <div id="add-msg" class="ok-msg"></div>
      <button class="btn btn-gold" onclick="doAddItem()">Add to Menu</button>
    </div>

    <!-- Tab 4: Update Item -->
    <div id="ap-update" class="ap-content" style="display:none;">
      <div style="display:flex;gap:24px;flex-wrap:wrap;">
        <div style="min-width:240px;max-width:280px;">
          <h4 style="color:var(--gold);margin-bottom:12px;">1. Select Dish</h4>
          <div id="update-list" style="background:var(--card);border:1px solid var(--border);border-radius:10px;overflow-y:auto;max-height:460px;"></div>
        </div>
        <div style="flex:1;min-width:280px;max-width:520px;">
          <h4 style="color:var(--gold);margin-bottom:12px;">2. Edit Details</h4>
          <div class="form-group"><label>Dish Name</label><input id="u-name" type="text"/></div>
          <div class="form-group"><label>Price (Rs.)</label><input id="u-price" type="number" min="1"/></div>
          <div class="form-group"><label>Description</label><textarea id="u-desc" rows="3"></textarea></div>
          <div class="form-group"><label>Cuisine</label><select id="u-cuisine"></select></div>
          <div id="upd-msg" class="ok-msg"></div>
          <button class="btn btn-gold" onclick="doUpdate()">Save Changes</button>
        </div>
      </div>
    </div>

    <!-- Tab 5: Delete Item -->
    <div id="ap-delete" class="ap-content" style="display:none;max-width:500px;">
      <h3 style="font-family:var(--font-serif);color:var(--gold);margin-bottom:20px;">&#128465; Delete Dish</h3>
      <p style="color:var(--text-muted);font-size:0.84rem;margin-bottom:16px;">Deleted items are safely archived in <code>DeletedRecords.csv</code> for recordkeeping.</p>
      <div class="form-group"><label>Select Dish to Remove</label><select id="del-select"></select></div>
      <div id="del-msg" class="ok-msg"></div>
      <button class="btn btn-red" onclick="doDelete()">Confirm & Archive Delete</button>
    </div>
  </section>

</main>

<!-- FLOATING TOAST -->
<div id="toast"></div>

<script>
// ─────────────────────────────────────────────
//  CLIENT STATE & CONFIG
// ─────────────────────────────────────────────
const CUISINES = [
  "Hotel Sunshine Special", "Starters", "South Indian", "Chinese Ching",
  "Vegetarian Verna", "Non-Vegetarian Delicacies", "Desserts and Beverages", "Add Ons"
];

let cart = {}; // { itemName: {qty, price} }
let menuCache = [];
let currentCuisine = CUISINES[0];
let updOrigName = null;
let activeTrackingOrderId = null;
let trackingInterval = null;
let selectedOrderType = "delivery"; // 'delivery' | 'dinein' | 'takeaway'

// ── Theme Switcher ───────────────────────────
function initTheme() {
  const saved = localStorage.getItem('hm_theme') || 'dark';
  if (saved === 'light') {
    document.body.classList.add('light-theme');
    document.getElementById('theme-icon').textContent = '🌙';
    document.getElementById('theme-text').textContent = 'Dark Mode';
  } else {
    document.body.classList.remove('light-theme');
    document.getElementById('theme-icon').textContent = '☀️';
    document.getElementById('theme-text').textContent = 'Light Mode';
  }
}

function toggleTheme() {
  const isLight = document.body.classList.toggle('light-theme');
  localStorage.setItem('hm_theme', isLight ? 'light' : 'dark');
  document.getElementById('theme-icon').textContent = isLight ? '🌙' : '☀️';
  document.getElementById('theme-text').textContent = isLight ? 'Dark Mode' : 'Light Mode';
  toast(isLight ? 'Switched to Light Mode' : 'Switched to Dark Mode');
}

// ── Page Router ──────────────────────────────
function showPage(id, linkEl) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  const target = document.getElementById(id);
  if (target) target.classList.add('active');

  document.querySelectorAll('#sidebar nav a').forEach(a => a.classList.remove('active'));
  const navLink = linkEl || document.getElementById('nav-' + id);
  if (navLink) navLink.classList.add('active');

  if (id === 'order') { loadMenu(); renderCart(); }
  if (id === 'bill') { refreshBill(); }
  if (id === 'track') { renderTrackView(); }
  if (id === 'admin-panel') { loadAdminOrders(); loadDisplay(); loadUpdateList(); loadDeleteList(); }
}

// ── Toast Notification ───────────────────────
function toast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}

// ── Home Cuisines ────────────────────────────
function buildHomeTags() {
  const el = document.getElementById('cuisine-tags');
  el.innerHTML = CUISINES.map(c =>
    `<span class="tag" onclick="currentCuisine='${c}';showPage('order',null);">${c}</span>`
  ).join('');
}

// ── Cuisine Tabs & Menu ──────────────────────
function buildTabs() {
  const el = document.getElementById('cuisine-tabs');
  el.innerHTML = CUISINES.map(c =>
    `<button class="ctab${c===currentCuisine?' active':''}" onclick="selectCuisine('${c}',this)">${c}</button>`
  ).join('');
}

function selectCuisine(c, btn) {
  currentCuisine = c;
  document.querySelectorAll('.ctab').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderMenu();
}

async function loadMenu() {
  const res = await fetch('/api/menu');
  menuCache = await res.json();
  buildTabs();
  renderMenu();
}

function filterMenuItems() {
  renderMenu();
}

function renderMenu() {
  const area = document.getElementById('menu-area');
  const search = (document.getElementById('menu-search-input')?.value || '').trim().toLowerCase();

  let items = menuCache;
  if (search) {
    items = items.filter(i => i.name.toLowerCase().includes(search) || i.desc.toLowerCase().includes(search) || i.cuisine.toLowerCase().includes(search));
  } else {
    items = items.filter(i => i.cuisine.trim() === currentCuisine);
  }

  if (!items.length) {
    area.innerHTML = `<div style="text-align:center;padding:48px 20px;color:var(--text-muted)">
      <h3>No items found</h3>
      <p>Try searching with another keyword or pick another category.</p>
    </div>`;
    return;
  }

  area.innerHTML = `<div class="menu-grid">` + items.map(item => {
    const key = btoa(encodeURIComponent(item.name)).replace(/=/g,'');
    return `
      <div class="menu-item">
        <div class="info">
          <h4>${esc(item.name)}</h4>
          <div class="price">Rs. ${item.price}</div>
          <div class="desc">${esc(item.desc)}</div>
        </div>
        <div class="actions">
          <div class="qty-ctrl">
            <button onclick="adjQty('${key}', -1)">&#8722;</button>
            <span id="qty-${key}">1</span>
            <button onclick="adjQty('${key}', 1)">+</button>
          </div>
          <button class="btn btn-gold btn-sm" onclick="addToCart('${esc(item.name)}', ${item.price}, '${key}')">
            Add to Basket
          </button>
        </div>
      </div>
    `;
  }).join('') + `</div>`;
}

function adjQty(key, delta) {
  const el = document.getElementById('qty-' + key);
  if (!el) return;
  const v = Math.max(1, parseInt(el.textContent) + delta);
  el.textContent = v;
}

// ── Cart Operations ──────────────────────────
function addToCart(name, price, key) {
  const el = document.getElementById('qty-' + key);
  const qty = el ? parseInt(el.textContent) : 1;
  if (cart[name]) cart[name].qty += qty;
  else cart[name] = { qty, price };
  renderCart();
  toast(`Added ${qty}× "${name}" to basket`);
}

function removeFromCart(name) {
  delete cart[name];
  renderCart();
}

function clearCart() {
  if (!Object.keys(cart).length) { toast('Basket is already empty.'); return; }
  if (confirm('Clear all items from your basket?')) {
    cart = {};
    renderCart();
    toast('Basket cleared.');
  }
}

function renderCart() {
  const items = Object.entries(cart);
  const count = items.reduce((s, [, v]) => s + v.qty, 0);
  document.getElementById('cart-count').textContent = `${count} items`;
  document.getElementById('cart-items-counter').textContent = `${count} items`;

  const el = document.getElementById('cart-items');
  if (!items.length) {
    el.innerHTML = '<p style="color:var(--text-muted);font-size:0.85rem;padding:20px;text-align:center;">Your basket is empty.<br>Explore menu & add dishes.</p>';
  } else {
    el.innerHTML = items.map(([name, {qty, price}]) => `
      <div class="cart-row">
        <div class="cname">${esc(name)}</div>
        <div class="camt">${qty} × Rs.${price}</div>
        <button class="cdel" title="Remove item" onclick="removeFromCart('${esc(name)}')">&#10005;</button>
      </div>
    `).join('');
  }

  const total = items.reduce((s, [, v]) => s + v.qty * v.price, 0);
  const tax = total * 0.05;
  const grand = total + tax;
  document.getElementById('cart-total').innerHTML =
    `Subtotal: Rs. ${total.toFixed(2)}<br>GST (5%): Rs. ${tax.toFixed(2)}<br><strong>Grand Total: Rs. ${grand.toFixed(2)}</strong>`;
}

// ── Switch Order Type on Checkout ────────────
function setOrderType(type) {
  selectedOrderType = type;
  document.querySelectorAll('.order-type-btn').forEach(b => b.classList.remove('active'));
  const btn = document.getElementById('type-btn-' + type);
  if (btn) btn.classList.add('active');

  const deliveryFields = document.getElementById('delivery-fields');
  const dineinFields = document.getElementById('dinein-fields');
  const takeawayFields = document.getElementById('takeaway-fields');

  if (deliveryFields) deliveryFields.style.display = type === 'delivery' ? 'block' : 'none';
  if (dineinFields) dineinFields.style.display = type === 'dinein' ? 'block' : 'none';
  if (takeawayFields) takeawayFields.style.display = type === 'takeaway' ? 'block' : 'none';
}

// ── Smart View Bill & Checkout ───────────────
async function refreshBill() {
  const container = document.getElementById('bill-container');
  const items = Object.entries(cart);

  // CASE 1: User has items in active basket -> show Checkout & Order Confirmation Form
  if (items.length > 0) {
    let total = 0;
    const tableRows = items.map(([name, {qty, price}]) => {
      const amt = qty * price;
      total += amt;
      return `<tr><td><strong>${esc(name)}</strong></td><td>${qty}</td><td>Rs. ${price}</td><td><strong>Rs. ${amt}</strong></td></tr>`;
    }).join('');

    const tax = total * 0.05;
    const grand = total + tax;

    container.innerHTML = `
      <!-- Order Type Selector -->
      <div class="checkout-section">
        <h3>&#128757; Choose Order Type</h3>
        <div class="order-type-tabs">
          <div id="type-btn-delivery" class="order-type-btn ${selectedOrderType==='delivery'?'active':''}" onclick="setOrderType('delivery')">
            <span class="type-icon">&#128757;</span>
            <span>Online Home Delivery</span>
          </div>
          <div id="type-btn-dinein" class="order-type-btn ${selectedOrderType==='dinein'?'active':''}" onclick="setOrderType('dinein')">
            <span class="type-icon">&#127869;</span>
            <span>Dine-In Table</span>
          </div>
          <div id="type-btn-takeaway" class="order-type-btn ${selectedOrderType==='takeaway'?'active':''}" onclick="setOrderType('takeaway')">
            <span class="type-icon">&#128092;</span>
            <span>Self Pickup / Takeaway</span>
          </div>
        </div>

        <!-- 1. Online Delivery Fields -->
        <div id="delivery-fields" style="${selectedOrderType==='delivery'?'':'display:none;'}">
          <div class="form-row">
            <div class="form-group">
              <label>Full Name *</label>
              <input id="del-name" type="text" placeholder="e.g. ABC" required/>
            </div>
            <div class="form-group">
              <label>Phone Number (10 Digits) *</label>
              <input id="del-phone" type="tel" placeholder="e.g. 9876543210" maxlength="14" required/>
            </div>
          </div>
          <div class="form-group">
            <label>Full Delivery Address (Flat / House No., Society / Building, Street) *</label>
            <textarea id="del-address" rows="2" placeholder="e.g. Flat 402, Sunshine Heights, Station Road" required></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Area / Locality in Thane *</label>
              <select id="del-area">
                <option value="Thane West">Thane West (Near Station)</option>
                <option value="Naupada">Naupada</option>
                <option value="Panchpakhadi">Panchpakhadi</option>
                <option value="Majiwada">Majiwada</option>
                <option value="Ghodbunder Road">Ghodbunder Road</option>
                <option value="Vasant Vihar">Vasant Vihar</option>
                <option value="Thane East">Thane East</option>
                <option value="Kopri">Kopri</option>
                <option value="Wagle Estate">Wagle Estate</option>
              </select>
            </div>
            <div class="form-group">
              <label>Pincode *</label>
              <input id="del-pincode" type="text" placeholder="e.g. 400601" value="400614"/>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Nearby Landmark (Optional)</label>
              <input id="del-landmark" type="text" placeholder="e.g. Opp. Thane Station Platform 1"/>
            </div>
            <div class="form-group">
              <label>Special Instructions for Chef / Rider</label>
              <input id="del-notes" type="text" placeholder="e.g. Extra spicy, don't ring bell"/>
            </div>
          </div>
        </div>

        <!-- 2. Dine-In Fields -->
        <div id="dinein-fields" style="${selectedOrderType==='dinein'?'':'display:none;'}">
          <div class="form-row">
            <div class="form-group">
              <label>Guest Name *</label>
              <input id="di-name" type="text" placeholder="e.g. ABC" value="Guest"/>
            </div>
            <div class="form-group">
              <label>Phone Number *</label>
              <input id="di-phone" type="tel" placeholder="e.g. 9876543210"/>
            </div>
          </div>
          <div class="form-group">
            <label>Table Number *</label>
            <input id="di-table" type="text" placeholder="e.g. Table 4" value="Table 1"/>
          </div>
        </div>

        <!-- 3. Takeaway Fields -->
        <div id="takeaway-fields" style="${selectedOrderType==='takeaway'?'':'display:none;'}">
          <div class="form-row">
            <div class="form-group">
              <label>Customer Name *</label>
              <input id="ta-name" type="text" placeholder="e.g. ABC"/>
            </div>
            <div class="form-group">
              <label>Phone Number *</label>
              <input id="ta-phone" type="tel" placeholder="e.g. 9876543210"/>
            </div>
          </div>
          <div class="form-group">
            <label>Pickup Time Preference</label>
            <select id="ta-time">
              <option value="In 20-25 minutes">In 20-25 minutes</option>
              <option value="In 30-40 minutes">In 30-40 minutes</option>
              <option value="In 1 hour">In 1 hour</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Bill Breakdown -->
      <div class="checkout-section">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
          <h3 style="margin-bottom:0;">&#129534; Active Basket Breakdown</h3>
          <span class="tag" style="background:var(--gold-glow);border-color:var(--gold);color:var(--gold);">${items.length} items</span>
        </div>
        <table class="bill-table">
          <thead><tr><th>Dish</th><th>Quantity</th><th>Unit Price</th><th>Amount</th></tr></thead>
          <tbody>${tableRows}</tbody>
        </table>

        <div class="totals-box">
          <div class="trow"><span>Items Subtotal</span><span>Rs. ${total.toFixed(2)}</span></div>
          <div class="trow"><span>CGST (2.5%) + SGST (2.5%)</span><span>Rs. ${tax.toFixed(2)}</span></div>
          <div class="trow"><span>Doorstep Delivery Fee</span><span style="color:var(--green);font-weight:700;">FREE (Thane)</span></div>
          <div class="trow grand"><span>Grand Total (Payable)</span><span>Rs. ${grand.toFixed(2)}</span></div>
        </div>

        <p style="color:var(--text-muted);font-size:0.85rem;margin-bottom:20px;">
          &#128181; <strong>Payment Method:</strong> Cash on Delivery (COD) / Pay upon Receiving.
        </p>

        <div style="display:flex;gap:12px;flex-wrap:wrap;">
          <button class="btn btn-green" onclick="placeOrder()">&#10004; Confirm & Place Order</button>
          <button class="btn btn-red" onclick="cancelOrder()">&#10006; Empty Basket</button>
          <button class="btn btn-panel" onclick="showPage('order',null)">Add More Items</button>
        </div>
      </div>
    `;
    return;
  }

  // CASE 2: Basket is empty -> Check if user has a confirmed order to display the official Invoice Receipt
  const lastOrderId = activeTrackingOrderId || localStorage.getItem('hm_last_order');
  let orderData = null;

  if (lastOrderId) {
    try {
      const res = await fetch(`/api/orders/track?id=${encodeURIComponent(lastOrderId)}`);
      const data = await res.json();
      if (data.ok && data.order) {
        orderData = data.order;
        orderData.computed_status = data.computed_status;
      }
    } catch (e) {}
  }

  if (orderData) {
    let subtotal = 0;
    const tableRows = orderData.items.map(it => {
      const amt = it.qty * it.price;
      subtotal += amt;
      return `<tr><td><strong>${esc(it.name)}</strong></td><td>${it.qty}</td><td>Rs. ${it.price}</td><td><strong>Rs. ${amt}</strong></td></tr>`;
    }).join('');

    const tax = orderData.tax || (subtotal * 0.05);
    const grand = orderData.grand_total || (subtotal + tax);
    const isDelivery = orderData.order_type === 'delivery';

    container.innerHTML = `
      <div class="checkout-section">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:14px;border-bottom:1px solid var(--border);padding-bottom:18px;margin-bottom:20px;">
          <div>
            <span class="badge" style="display:inline-block;font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--green);background:rgba(16,185,129,0.15);padding:3px 10px;border-radius:20px;border:1px solid var(--green);margin-bottom:6px;">
              &#10004; ${isDelivery ? '🛵 Online Delivery Invoice' : '🍽️ Dine-In Bill'}
            </span>
            <h2 style="font-family:var(--font-serif);color:var(--gold);font-size:1.8rem;margin:4px 0;">Invoice #${esc(orderData.id)}</h2>
            <div style="font-size:0.85rem;color:var(--text-muted);">
              Hotel Mara &bull; Thane Station Branch &bull; ${esc(orderData.time)}
            </div>
          </div>
          <div style="text-align:right;">
            <div style="font-size:0.82rem;color:var(--text-muted);">Customer & Contact</div>
            <div style="font-weight:700;color:var(--text);font-size:1rem;">${esc(orderData.customer)}</div>
            <div style="font-size:0.85rem;color:var(--gold);">📞 ${esc(orderData.phone || 'N/A')}</div>
          </div>
        </div>

        ${isDelivery ? `
          <div style="background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:16px 20px;margin-bottom:20px;">
            <h4 style="color:var(--gold);font-size:0.92rem;margin-bottom:6px;">📍 Delivery Destination</h4>
            <p style="font-size:0.88rem;color:var(--text);line-height:1.5;">${esc(orderData.address)}, ${esc(orderData.area)} &bull; PIN: ${esc(orderData.pincode)}</p>
            ${orderData.landmark ? `<p style="font-size:0.8rem;color:var(--text-muted);margin-top:4px;">Landmark: ${esc(orderData.landmark)}</p>` : ''}
            ${orderData.notes ? `<p style="font-size:0.8rem;color:var(--accent);margin-top:4px;">Note: ${esc(orderData.notes)}</p>` : ''}
          </div>
        ` : `
          <div style="background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:14px 18px;margin-bottom:20px;">
            <span style="color:var(--gold);font-weight:600;">Table / Order Type:</span> ${esc(orderData.table || 'Dine-In Table')}
          </div>
        `}

        <h3 style="margin-bottom:14px;">&#129534; Tax Invoice Summary</h3>
        <table class="bill-table">
          <thead><tr><th>Item Name</th><th>Quantity</th><th>Unit Price</th><th>Amount</th></tr></thead>
          <tbody>${tableRows}</tbody>
        </table>

        <div class="totals-box">
          <div class="trow"><span>Items Subtotal</span><span>Rs. ${parseFloat(subtotal).toFixed(2)}</span></div>
          <div class="trow"><span>CGST (2.5%) + SGST (2.5%)</span><span>Rs. ${parseFloat(tax).toFixed(2)}</span></div>
          <div class="trow"><span>Delivery Charges</span><span style="color:var(--green);font-weight:700;">FREE</span></div>
          <div class="trow grand"><span>Grand Total Paid / Payable</span><span>Rs. ${parseFloat(grand).toFixed(2)}</span></div>
        </div>

        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;background:var(--panel);padding:14px 18px;border-radius:8px;border:1px solid var(--border);margin-bottom:24px;">
          <div style="font-size:0.85rem;color:var(--text);">
            &#128181; <strong>Payment Mode:</strong> Cash on Delivery (COD)<br>
            <span style="font-size:0.78rem;color:var(--text-muted);">Saved to bill.csv and store system</span>
          </div>
          <div>
            <span class="status-badge status-ready">&#9679; ${esc(orderData.computed_status || 'Order Placed')}</span>
          </div>
        </div>

        <div style="display:flex;gap:12px;flex-wrap:wrap;">
          <button class="btn btn-panel" onclick="window.print()">&#129534; Print Bill / Invoice</button>
          <button class="btn btn-gold" onclick="showPage('track',null)">&#128205; Track Order Live</button>
          <button class="btn btn-green" onclick="showPage('order',null)">+ Start New Order</button>
        </div>
      </div>
    `;
    return;
  }

  // CASE 3: No items in cart and no past order found
  container.innerHTML = `
    <div class="checkout-section" style="text-align:center;padding:56px 20px;">
      <div style="font-size:2.8rem;color:var(--gold);margin-bottom:12px;">&#129534;</div>
      <h3 style="justify-content:center;">No Active Bill Found</h3>
      <p style="color:var(--text-muted);margin:8px auto 24px;max-width:420px;">Your basket is currently empty and there are no active orders to display. Explore our menu to select delicious dishes for online delivery or dine-in!</p>
      <button class="btn btn-gold" onclick="showPage('order',null)">Browse Hotel Mara Menu &#10140;</button>
    </div>
  `;
}

// ── Order Placement ──────────────────────────
async function placeOrder() {
  const items = Object.entries(cart).map(([name, v]) => ({ name, qty: v.qty, price: v.price }));
  if (!items.length) {
    toast('Basket is empty — please add dishes first!');
    return;
  }

  let custName = "Guest";
  let phone = "";
  let address = "";
  let area = "Thane";
  let pincode = "400614";
  let landmark = "";
  let notes = "";
  let table = "Table 1";

  if (selectedOrderType === 'delivery') {
    custName = document.getElementById('del-name')?.value.trim();
    phone    = document.getElementById('del-phone')?.value.trim();
    address  = document.getElementById('del-address')?.value.trim();
    area     = document.getElementById('del-area')?.value || "Thane West";
    pincode  = document.getElementById('del-pincode')?.value.trim() || "400614";
    landmark = document.getElementById('del-landmark')?.value.trim();
    notes    = document.getElementById('del-notes')?.value.trim();

    if (!custName) { toast('Please enter your full name'); document.getElementById('del-name')?.focus(); return; }
    if (!phone || phone.length < 10) { toast('Please enter a valid 10-digit phone number'); document.getElementById('del-phone')?.focus(); return; }
    if (!address) { toast('Please enter your delivery address'); document.getElementById('del-address')?.focus(); return; }
  } else if (selectedOrderType === 'dinein') {
    custName = document.getElementById('di-name')?.value.trim() || "Guest";
    phone    = document.getElementById('di-phone')?.value.trim();
    table    = document.getElementById('di-table')?.value.trim() || "Table 1";
    if (!phone) { toast('Please enter your phone number'); document.getElementById('di-phone')?.focus(); return; }
  } else {
    custName = document.getElementById('ta-name')?.value.trim() || "Takeaway Customer";
    phone    = document.getElementById('ta-phone')?.value.trim();
    table    = "Takeaway (" + (document.getElementById('ta-time')?.value || "Pickup") + ")";
    if (!phone) { toast('Please enter your phone number'); document.getElementById('ta-phone')?.focus(); return; }
  }

  const total = items.reduce((s, it) => s + it.qty * it.price, 0);
  const tax = total * 0.05;
  const grand = total + tax;

  const res = await fetch('/api/orders/place', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      order_type: selectedOrderType,
      customer: custName,
      phone: phone,
      address: address,
      area: area,
      pincode: pincode,
      landmark: landmark,
      notes: notes,
      table: table,
      items: items,
      subtotal: total,
      tax: tax,
      grand_total: grand
    })
  });

  const data = await res.json();
  if (data.ok) {
    activeTrackingOrderId = data.order.id;
    localStorage.setItem('hm_last_order', data.order.id);
    cart = {};
    renderCart();
    toast(`Order #${data.order.id} placed! Tracking live.`);
    showPage('track', null);
  } else {
    toast('Failed to place order: ' + (data.error || 'Server error'));
  }
}

function cancelOrder() {
  if (!Object.keys(cart).length) { toast('Nothing to cancel.'); return; }
  if (confirm('Empty your current basket?')) {
    cart = {};
    renderCart();
    refreshBill();
    toast('Basket cleared.');
    showPage('home', null);
  }
}

// ── Order Tracking ───────────────────────────
const DELIVERY_STAGES = [
  { key: 'Order Placed & Confirmed', label: 'Order Confirmed', icon: '📝' },
  { key: 'Preparing in Kitchen', label: 'In Kitchen', icon: '👨‍🍳' },
  { key: 'Packed & Quality Checked', label: 'Packed & Sealed', icon: '📦' },
  { key: 'Out for Delivery (Rider on the Way)', label: 'Out for Delivery', icon: '🛵' },
  { key: 'Delivered to Customer', label: 'Delivered', icon: '🏡' }
];

const DINEIN_STAGES = [
  { key: 'Order Placed', label: 'Order Placed', icon: '📝' },
  { key: 'Preparing in Kitchen', label: 'In Kitchen', icon: '👨‍🍳' },
  { key: 'Quality Check & Plating', label: 'Plating & QA', icon: '✨' },
  { key: 'Ready for Serving', label: 'Ready to Serve', icon: '🚀' },
  { key: 'Served & Completed', label: 'Completed', icon: '🎉' }
];

function trackQuickOrder() {
  const qid = document.getElementById('quick-track-id').value.trim();
  if (!qid) { toast('Please enter an Order ID'); return; }
  activeTrackingOrderId = qid;
  showPage('track', null);
}

function lookupOrder() {
  const qid = document.getElementById('track-search-input').value.trim();
  if (!qid) { toast('Please enter an Order ID'); return; }
  activeTrackingOrderId = qid;
  renderTrackView();
}

async function renderTrackView() {
  const container = document.getElementById('track-result-container');
  const searchInput = document.getElementById('track-search-input');

  const orderId = activeTrackingOrderId || localStorage.getItem('hm_last_order');
  if (orderId && searchInput) searchInput.value = orderId;

  if (!orderId) {
    container.innerHTML = `
      <div class="track-card" style="text-align:center;padding:48px 24px;">
        <div style="font-size:2.4rem;color:var(--gold);margin-bottom:12px;">&#128205;</div>
        <h3>No Order Selected</h3>
        <p style="color:var(--text-muted);margin:8px 0 20px;">Enter your Order ID above or place an online delivery order from the menu.</p>
        <button class="btn btn-gold" onclick="showPage('order',null)">Explore Menu & Order &#10140;</button>
      </div>`;
    return;
  }

  const res = await fetch(`/api/orders/track?id=${encodeURIComponent(orderId)}`);
  const data = await res.json();

  if (!data.ok || !data.order) {
    container.innerHTML = `
      <div class="track-card" style="text-align:center;padding:40px 20px;">
        <h3 style="color:var(--red);">Order Not Found</h3>
        <p style="color:var(--text-muted);margin-top:8px;">We couldn't locate Order <strong>#${esc(orderId)}</strong>. Please verify the ID.</p>
      </div>`;
    return;
  }

  const order = data.order;
  const currStatus = data.computed_status;
  const isDelivery = order.order_type === 'delivery';
  const stageList = isDelivery ? DELIVERY_STAGES : DINEIN_STAGES;

  // Determine active step index
  let activeIdx = stageList.findIndex(s => s.key.toLowerCase() === currStatus.toLowerCase());
  if (activeIdx === -1) activeIdx = 0;
  const progressPercent = (activeIdx / (stageList.length - 1)) * 100;

  // Status class
  let statusBadgeClass = 'status-placed';
  if (currStatus.includes('Kitchen')) statusBadgeClass = 'status-kitchen';
  else if (currStatus.includes('Packed') || currStatus.includes('Plating')) statusBadgeClass = 'status-plating';
  else if (currStatus.includes('Delivery') || currStatus.includes('Ready')) statusBadgeClass = 'status-ready';
  else if (currStatus.includes('Delivered') || currStatus.includes('Served') || currStatus.includes('Completed')) statusBadgeClass = 'status-delivered';
  else if (currStatus.includes('Cancelled')) statusBadgeClass = 'status-cancelled';

  container.innerHTML = `
    <div class="track-card">
      <div class="track-header">
        <div>
          <div style="font-size:0.8rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:1px;">
            ${isDelivery ? '🛵 Online Delivery Order' : '🍽️ Restaurant Order'}
          </div>
          <div class="order-num">#${esc(order.id)}</div>
          <div style="font-size:0.84rem;color:var(--text-muted);margin-top:4px;">
            Customer: <strong>${esc(order.customer)}</strong> &bull; 📞 ${esc(order.phone || 'N/A')} &bull; ${esc(order.time)}
          </div>
        </div>
        <div>
          <span class="status-badge ${statusBadgeClass}">&#9679; ${esc(currStatus)}</span>
        </div>
      </div>

      <!-- Timeline Progress -->
      <div class="timeline">
        <div class="timeline-progress-bar" style="width: calc(${progressPercent}% * 0.85);"></div>
        ${stageList.map((s, idx) => {
          let nodeClass = '';
          if (idx < activeIdx) nodeClass = 'completed';
          else if (idx === activeIdx) nodeClass = 'active';
          return `
            <div class="step-node ${nodeClass}">
              <div class="step-circle">${idx < activeIdx ? '&#10004;' : s.icon}</div>
              <div class="step-title">${s.label}</div>
            </div>
          `;
        }).join('')}
      </div>

      <!-- Delivery / Table Information -->
      ${isDelivery ? `
        <div style="background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:18px 22px;margin:24px 0 16px;">
          <h4 style="font-family:var(--font-serif);color:var(--gold);margin-bottom:8px;">🛵 Doorstep Delivery Details</h4>
          <div style="font-size:0.88rem;color:var(--text);line-height:1.5;">
            <strong>Recipient:</strong> ${esc(order.customer)} &bull; 📞 ${esc(order.phone)}<br>
            <strong>Address:</strong> ${esc(order.address)}, ${esc(order.area)} (PIN: ${esc(order.pincode)})
            ${order.landmark ? `<br><strong>Landmark:</strong> ${esc(order.landmark)}` : ''}
            ${order.notes ? `<br><strong>Delivery Note:</strong> ${esc(order.notes)}` : ''}
          </div>
        </div>
      ` : ''}

      <!-- Order Items Detail -->
      <div style="background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:20px 24px;">
        <h4 style="font-family:var(--font-serif);color:var(--gold);margin-bottom:14px;">Order Summary</h4>
        <div style="display:flex;flex-direction:column;gap:8px;margin-bottom:16px;">
          ${order.items.map(it => `
            <div style="display:flex;justify-content:space-between;font-size:0.88rem;">
              <span>${esc(it.name)} × ${it.qty}</span>
              <span>Rs. ${it.qty * it.price}</span>
            </div>
          `).join('')}
        </div>
        <div style="border-top:1px solid var(--border);padding-top:12px;display:flex;justify-content:space-between;font-weight:700;color:var(--gold);font-size:1.1rem;">
          <span>Grand Total (Cash on Delivery):</span>
          <span>Rs. ${parseFloat(order.grand_total).toFixed(2)}</span>
        </div>
      </div>

      <div style="margin-top:20px;display:flex;gap:12px;justify-content:flex-end;flex-wrap:wrap;">
        <button class="btn btn-panel btn-sm" onclick="showPage('bill',null)">&#129534; View Full Bill & Invoice</button>
        <button class="btn btn-gold btn-sm" onclick="showPage('order',null)">Place Another Order</button>
      </div>
    </div>
  `;

  // Auto-refresh tracking status every 8 seconds
  if (trackingInterval) clearInterval(trackingInterval);
  trackingInterval = setInterval(() => {
    const trackPage = document.getElementById('track');
    if (trackPage && trackPage.classList.contains('active')) {
      renderTrackView();
    }
  }, 8000);
}

// ── Admin Login & Dashboard ──────────────────
async function doLogin() {
  const u = document.getElementById('admin-user').value.trim();
  const p = document.getElementById('admin-pass').value.trim();
  const res = await fetch('/api/admin/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: u, password: p })
  });
  const data = await res.json();
  if (data.ok) {
    document.getElementById('login-err').textContent = '';
    document.getElementById('admin-user').value = '';
    document.getElementById('admin-pass').value = '';
    toast('Admin access granted.');
    showPage('admin-panel', null);
  } else {
    document.getElementById('login-err').textContent = 'Invalid credentials. Access Denied.';
  }
}

function logoutAdmin() {
  toast('Logged out of Admin Portal.');
  showPage('home', null);
}

// ── Admin Live Orders ────────────────────────
async function loadAdminOrders() {
  const res = await fetch('/api/orders');
  const data = await res.json();
  const container = document.getElementById('admin-orders-list');

  if (!data.orders || !data.orders.length) {
    container.innerHTML = `<p style="color:var(--text-muted);padding:24px 0;">No orders received yet.</p>`;
    return;
  }

  container.innerHTML = `<div style="display:flex;flex-direction:column;gap:16px;">` +
    data.orders.slice().reverse().map(order => {
      const curr = order.computed_status || order.status;
      const isDelivery = order.order_type === 'delivery';
      const stageList = isDelivery ? DELIVERY_STAGES : DINEIN_STAGES;

      return `
        <div style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px 24px;">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;margin-bottom:12px;">
            <div>
              <span style="font-family:var(--font-serif);font-size:1.2rem;color:var(--gold);font-weight:700;">#${esc(order.id)}</span>
              <span class="tag" style="margin-left:8px;font-size:0.75rem;padding:2px 10px;background:var(--gold-glow);border-color:var(--gold);">
                ${isDelivery ? '🛵 Online Delivery' : '🍽️ ' + (order.table || 'Dine-In')}
              </span>
              <div style="color:var(--text-muted);font-size:0.85rem;margin-top:4px;">
                <strong>${esc(order.customer)}</strong> &bull; 📞 <a href="tel:${esc(order.phone)}" style="color:var(--accent);text-decoration:none;">${esc(order.phone || 'No phone')}</a> &bull; ${esc(order.time)}
              </div>
            </div>
            <div style="display:flex;align-items:center;gap:10px;">
              <span style="font-size:0.82rem;font-weight:700;color:var(--gold);">Status:</span>
              <select onchange="updateOrderStatus('${order.id}', this.value)" style="background:var(--panel);border:1px solid var(--border);border-radius:6px;padding:6px 10px;color:var(--text);font-size:0.82rem;">
                ${stageList.map(s => `<option value="${s.key}" ${curr===s.key?'selected':''}>${s.label}</option>`).join('')}
                <option value="Cancelled" ${curr==='Cancelled'?'selected':''}>Cancelled</option>
              </select>
            </div>
          </div>

          ${isDelivery ? `
            <div style="background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:10px 14px;margin-bottom:10px;font-size:0.84rem;color:var(--text);">
              📍 <strong>Delivery Address:</strong> ${esc(order.address)}, ${esc(order.area)} (${esc(order.pincode)})
              ${order.landmark ? ` &bull; <strong>Landmark:</strong> ${esc(order.landmark)}` : ''}
              ${order.notes ? `<br>💬 <strong>Special Note:</strong> ${esc(order.notes)}` : ''}
            </div>
          ` : ''}

          <div style="font-size:0.85rem;color:var(--text-muted);margin-bottom:8px;">
            ${order.items.map(i => `${esc(i.name)} (×${i.qty})`).join(', ')}
          </div>
          <div style="font-weight:700;color:var(--text);font-size:0.95rem;">
            Grand Total: Rs. ${parseFloat(order.grand_total).toFixed(2)} (Cash on Delivery)
          </div>
        </div>
      `;
    }).join('') + `</div>`;
}

async function updateOrderStatus(orderId, newStatus) {
  const res = await fetch('/api/orders/update_status', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: orderId, status: newStatus })
  });
  const data = await res.json();
  if (data.ok) {
    toast(`Order #${orderId} status changed to "${newStatus}"`);
    loadAdminOrders();
  }
}

// ── Admin Menu Display / Add / Update / Delete ──
async function loadDisplay() {
  const res = await fetch('/api/menu');
  const rows = await res.json();
  const filter = document.getElementById('disp-filter').value;
  const filtered = (filter === 'All' || !filter) ? rows : rows.filter(r => r.cuisine.trim() === filter);

  document.getElementById('disp-body').innerHTML = filtered.map(r =>
    `<tr><td><strong>${esc(r.name)}</strong></td><td>Rs. ${r.price}</td><td><span class="tag" style="padding:2px 10px;font-size:0.75rem;">${esc(r.cuisine)}</span></td><td>${esc(r.desc)}</td></tr>`
  ).join('') || '<tr><td colspan="4" style="color:var(--text-muted);text-align:center;padding:20px;">No items found.</td></tr>';
}

function fillCuisineSelects() {
  const opts = CUISINES.map(c => `<option value="${c}">${c}</option>`).join('');
  ['a-cuisine','u-cuisine','disp-filter'].forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    if (id === 'disp-filter') el.innerHTML = '<option value="All">All Cuisines</option>' + opts;
    else el.innerHTML = opts;
  });
}

async function doAddItem() {
  const name    = document.getElementById('a-name').value.trim();
  const price   = document.getElementById('a-price').value.trim();
  const desc    = document.getElementById('a-desc').value.trim();
  const cuisine = document.getElementById('a-cuisine').value;
  const msg     = document.getElementById('add-msg');

  if (!name || !price || !desc || !cuisine) { msg.className='err-msg'; msg.textContent='All fields are required.'; return; }
  if (isNaN(parseInt(price)) || parseInt(price) <= 0) { msg.className='err-msg'; msg.textContent='Price must be a positive integer.'; return; }

  const res = await fetch('/api/menu/add', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, price: parseInt(price), desc, cuisine })
  });
  const data = await res.json();
  if (data.ok) {
    msg.className = 'ok-msg';
    msg.textContent = `'${name}' added successfully to menu!`;
    document.getElementById('a-name').value = '';
    document.getElementById('a-price').value = '';
    document.getElementById('a-desc').value = '';
    toast('Dish added to menu.');
  } else {
    msg.className = 'err-msg';
    msg.textContent = data.error;
  }
}

async function loadUpdateList() {
  const res = await fetch('/api/menu');
  const rows = await res.json();
  const el = document.getElementById('update-list');
  el.innerHTML = rows.map(r =>
    `<div onclick="loadUpdateForm(${JSON.stringify(JSON.stringify(r))})" style="padding:10px 14px;cursor:pointer;border-bottom:1px solid var(--border);font-size:0.84rem;color:var(--text-muted);">${esc(r.name)}</div>`
  ).join('');
}

function loadUpdateForm(jsonStr) {
  const r = JSON.parse(jsonStr);
  updOrigName = r.name;
  document.getElementById('u-name').value = r.name;
  document.getElementById('u-price').value = r.price;
  document.getElementById('u-desc').value = r.desc;
  document.getElementById('u-cuisine').value = r.cuisine;
  document.getElementById('upd-msg').textContent = '';
}

async function doUpdate() {
  if (!updOrigName) {
    document.getElementById('upd-msg').className = 'err-msg';
    document.getElementById('upd-msg').textContent = 'Please select a dish from the left list first.';
    return;
  }
  const name    = document.getElementById('u-name').value.trim();
  const price   = document.getElementById('u-price').value.trim();
  const desc    = document.getElementById('u-desc').value.trim();
  const cuisine = document.getElementById('u-cuisine').value;
  const msg     = document.getElementById('upd-msg');

  if (!name || !price || !desc || !cuisine) { msg.className='err-msg'; msg.textContent='All fields are required.'; return; }

  const res = await fetch('/api/menu/update', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ orig_name: updOrigName, name, price: parseInt(price), desc, cuisine })
  });
  const data = await res.json();
  if (data.ok) {
    msg.className = 'ok-msg';
    msg.textContent = `'${name}' updated successfully!`;
    updOrigName = name;
    loadUpdateList();
    toast('Dish details saved.');
  } else {
    msg.className = 'err-msg';
    msg.textContent = data.error;
  }
}

async function loadDeleteList() {
  const res = await fetch('/api/menu');
  const rows = await res.json();
  const el = document.getElementById('del-select');
  el.innerHTML = `<option value="">-- Select dish to delete --</option>` +
    rows.map(r => `<option value="${esc(r.name)}">${esc(r.name)} (Rs. ${r.price})</option>`).join('');
  document.getElementById('del-msg').textContent = '';
}

async function doDelete() {
  const name = document.getElementById('del-select').value;
  const msg  = document.getElementById('del-msg');
  if (!name) { msg.className = 'err-msg'; msg.textContent = 'Please select a dish to remove.'; return; }
  if (!confirm(`Are you sure you want to delete '${name}'?\nIt will be archived in DeletedRecords.csv.`)) return;

  const res = await fetch('/api/menu/delete', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name })
  });
  const data = await res.json();
  if (data.ok) {
    msg.className = 'ok-msg';
    msg.textContent = `'${name}' was deleted and archived.`;
    loadDeleteList();
    loadUpdateList();
    toast('Dish deleted from menu.');
  } else {
    msg.className = 'err-msg';
    msg.textContent = data.error;
  }
}

function showApTab(id, btn) {
  ['orders','display','add','update','delete'].forEach(t => {
    document.getElementById('ap-'+t).style.display = t===id ? '' : 'none';
  });
  document.querySelectorAll('.aptab').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  if (id === 'orders') loadAdminOrders();
  if (id === 'display') loadDisplay();
  if (id === 'update') loadUpdateList();
  if (id === 'delete') loadDeleteList();
}

function esc(s) {
  return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}

// ── App Boot ─────────────────────────────────
initTheme();
buildHomeTags();
fillCuisineSelects();
loadMenu();
</script>
</body>
</html>
"""

# ─────────────────────────────────────────────
#  HTTP REQUEST HANDLER
# ─────────────────────────────────────────────
class HotelMaraHandler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        pass  # Suppress default noisy console logs

    def _json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _html(self, html):
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path in ("/", "/index.html"):
            self._html(HTML_PAGE)

        elif path == "/api/menu":
            self._json(read_menu())

        elif path == "/api/bill":
            self._json(read_bill_csv())

        elif path == "/api/orders":
            orders = read_orders()
            # Attach computed status
            for o in orders:
                o["computed_status"] = compute_order_status(o)
            self._json({"ok": True, "orders": orders})

        elif path == "/api/orders/track":
            order_id = query.get("id", [""])[0].strip()
            orders = read_orders()
            target = None
            if order_id:
                for o in orders:
                    if str(o["id"]).lower() == order_id.lower():
                        target = o
                        break
            elif orders:
                target = orders[-1]

            if target:
                comp_status = compute_order_status(target)
                self._json({"ok": True, "order": target, "computed_status": comp_status})
            else:
                self._json({"ok": False, "error": "Order not found"}, status=404)

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        path = urlparse(self.path).path

        if path == "/api/admin/login":
            data = self._read_json()
            ok = ADMIN_CREDENTIALS.get(data.get("username", "")) == data.get("password", "")
            self._json({"ok": ok})

        elif path == "/api/orders/place":
            data = self._read_json()
            orders = read_orders()
            next_num = 1001 + len(orders)
            order_id = f"HM-{next_num}"

            new_order = {
                "id": order_id,
                "order_type": data.get("order_type", "delivery"),
                "customer": data.get("customer", "Guest"),
                "phone": data.get("phone", ""),
                "address": data.get("address", ""),
                "area": data.get("area", "Thane West"),
                "pincode": data.get("pincode", "400614"),
                "landmark": data.get("landmark", ""),
                "notes": data.get("notes", ""),
                "table": data.get("table", "Online Delivery"),
                "items": data.get("items", []),
                "subtotal": data.get("subtotal", 0),
                "tax": data.get("tax", 0),
                "grand_total": data.get("grand_total", 0),
                "time": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                "created_at": time.time(),
                "manual_status": None
            }
            orders.append(new_order)
            write_orders(orders)

            # Update bill.csv
            with open(BILL_FILE, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["Item Name", "Quantity", "Unit Price", "Amount"])
                for it in new_order["items"]:
                    amt = int(it["qty"]) * int(it["price"])
                    w.writerow([it["name"], it["qty"], it["price"], amt])

            self._json({"ok": True, "order": new_order})

        elif path == "/api/orders/update_status":
            data = self._read_json()
            order_id = str(data.get("id", "")).strip()
            new_status = str(data.get("status", "")).strip()
            orders = read_orders()
            found = False
            for o in orders:
                if str(o["id"]).lower() == order_id.lower():
                    o["manual_status"] = new_status
                    found = True
                    break
            if found:
                write_orders(orders)
                self._json({"ok": True})
            else:
                self._json({"ok": False, "error": "Order ID not found"})

        elif path == "/api/menu/add":
            data = self._read_json()
            name    = str(data.get("name", "")).strip()
            price   = data.get("price")
            desc    = str(data.get("desc", "")).strip()
            cuisine = str(data.get("cuisine", "")).strip()
            if not name or not price or not desc or not cuisine:
                self._json({"ok": False, "error": "All fields are required."})
                return
            rows = read_menu()
            for r in rows:
                if r["name"].strip().lower() == name.lower():
                    self._json({"ok": False, "error": f"'{name}' already exists in menu."})
                    return
            with open(MENU_FILE, "a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow([name, int(price), desc, cuisine])
            self._json({"ok": True})

        elif path == "/api/menu/update":
            data = self._read_json()
            orig    = str(data.get("orig_name", "")).strip()
            name    = str(data.get("name", "")).strip()
            price   = data.get("price")
            desc    = str(data.get("desc", "")).strip()
            cuisine = str(data.get("cuisine", "")).strip()
            if not orig or not name or not price or not desc or not cuisine:
                self._json({"ok": False, "error": "All fields are required."})
                return
            rows = read_menu()
            found = False
            new_rows = []
            for r in rows:
                if r["name"].strip() == orig:
                    new_rows.append({"name": name, "price": int(price), "desc": desc, "cuisine": cuisine})
                    found = True
                else:
                    new_rows.append(r)
            if not found:
                self._json({"ok": False, "error": "Original dish not found."})
                return
            write_menu_rows(new_rows)
            self._json({"ok": True})

        elif path == "/api/menu/delete":
            data = self._read_json()
            name = str(data.get("name", "")).strip()
            rows = read_menu()
            deleted = None
            new_rows = []
            for r in rows:
                if r["name"].strip() == name:
                    deleted = r
                else:
                    new_rows.append(r)
            if not deleted:
                self._json({"ok": False, "error": "Dish not found."})
                return
            write_menu_rows(new_rows)
            with open(DELETED_FILE, "a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow([deleted["name"], deleted["price"], deleted["desc"], deleted["cuisine"]])
            self._json({"ok": True})

        else:
            self.send_response(404)
            self.end_headers()

# ─────────────────────────────────────────────
#  MAIN SERVER RUNNER
# ─────────────────────────────────────────────
def run():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    init_storage()

    HOST, PORT = "localhost", 8765
    server = HTTPServer((HOST, PORT), HotelMaraHandler)
    url = f"http://{HOST}:{PORT}"

    print("=" * 60)
    print("  ⭐ HOTEL MARA — Online Delivery & Restaurant System")
    print("=" * 60)
    print(f"  Serving at: {url}")
    print("  Opening browser automatically...")
    print("  Press Ctrl+C in terminal to stop.")
    print("=" * 60)

    threading.Timer(0.8, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nHotel Mara server closed. Have a great day!")
        server.server_close()

if __name__ == "__main__":
    run()
