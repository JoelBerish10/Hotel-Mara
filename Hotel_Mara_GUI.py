import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

# ── Colour Palette ──────────────────────────────────────────────
BG_DARK     = "#0D0D1A"
BG_CARD     = "#14142B"
BG_PANEL    = "#1A1A35"
ACCENT      = "#C9A84C"
ACCENT2     = "#E8C46A"
TEXT_LIGHT  = "#F0EAD6"
TEXT_DIM    = "#8A8499"
RED_SOFT    = "#E05A5A"
GREEN_SOFT  = "#4CAF7D"
BORDER      = "#2A2A4A"

FONT_TITLE  = ("Georgia", 22, "bold")
FONT_HEADING= ("Georgia", 14, "bold")
FONT_BODY   = ("Helvetica", 10)
FONT_BODY_B = ("Helvetica", 10, "bold")
FONT_SMALL  = ("Helvetica", 9)
FONT_BTN    = ("Helvetica", 10, "bold")

MENU_FILE    = "Menu.csv"
DELETED_FILE = "DeletedRecords.csv"
BILL_FILE    = "bill.csv"

# ── Menu Data ───────────────────────────────────────────────────
MENU_DATA = [
    ["Balsamic Glazed Lamb Chops", 300,
     "Succulent lamb chops seared to perfection and coated in a tangy-sweet balsamic glaze with hints of garlic, honey, and rosemary.",
     "Hotel Sunshine Special"],
    ["Mango Tango Shrimp Tacos", 250,
     "Juicy shrimp infused with tropical mango salsa, nestled in warm tortillas, creating a vibrant explosion of flavours.",
     "Hotel Sunshine Special"],
    ["Garden Delight Stir-Fry", 150,
     "A vibrant medley of fresh vegetables stir-fried to perfection, seasoned with aromatic spices for a burst of flavour.",
     "Hotel Sunshine Special"],
    ["Savory Spinach and Ricotta Ravioli", 160,
     "Handmade ravioli stuffed with creamy ricotta cheese and spinach, served in a light herb-infused sauce.",
     "Hotel Sunshine Special"],
    ["Dreamy Chocolate Avalanche", 250,
     "Layers of indulgent chocolate bliss, topped with edible gold.",
     "Hotel Sunshine Special"],
    ["Blissful Berry Symphony", 270,
     "A harmonious medley of fresh berries layered atop delicate sponge cake, drizzled with a luscious berry reduction.",
     "Hotel Sunshine Special"],
    ["Chicken 65", 110,
     "Spicy, crispy fried chicken tossed with chilies, garlic, and aromatic spices for a bold, flavourful kick.",
     "Starters"],
    ["Chicken Wings", 120,
     "Juicy chicken wings, drenched and marinated, then deep-fried to perfection, offering a crispy and flavourful appetizer.",
     "Starters"],
    ["Chicken Tikka", 150,
     "Tender pieces of marinated chicken grilled to perfection, bursting with smoky and aromatic flavours.",
     "Starters"],
    ["Veg Crispy", 100,
     "Crispy and flavourful deep-fried vegetables coated in a crunchy batter, perfect as a crunchy appetizer.",
     "Starters"],
    ["Mushroom n Pepper Fry", 110,
     "Sauteed mushrooms and peppers seasoned with aromatic spices, offering a flavourful and savory dish.",
     "Starters"],
    ["Paneer Chilli", 120,
     "Cubes of paneer tossed in a spicy and tangy sauce with peppers and onions, offering a delicious Indo-Chinese dish.",
     "Starters"],
    ["Idli", 60,
     "Two idlis along with sambar and coconut chutney.",
     "South Indian"],
    ["Masala Dosa", 80,
     "Two masala dosas overloaded with potato filling along with chutney.",
     "South Indian"],
    ["Uttapam", 100,
     "Two uttapam with veggies on top along with tomato chutney.",
     "South Indian"],
    ["Medu Vada", 80,
     "4 medu vadas along with sambar and coconut chutney.",
     "South Indian"],
    ["Parotta with Mutton Curry", 160,
     "Four parottas with spicy mutton curry made from a blend of spices and tender mutton pieces.",
     "South Indian"],
    ["Chinese Bhel", 30,
     "Crispy noodles, colourful veggies, and tangy sauces, offering a unique twist on traditional Indian street food.",
     "Chinese Ching"],
    ["Momos", 70,
     "Savory dumplings filled with seasoned vegetables, steamed to perfection with a spicy dipping sauce.",
     "Chinese Ching"],
    ["Schezwan Fried Rice", 180,
     "A fiery blend of rice, vegetables, and spicy Schezwan sauce, wok-fried to perfection.",
     "Chinese Ching"],
    ["Hakka Noodles", 90,
     "Stir-fried noodles tossed with crispy vegetables and savory sauces, delivering a delightful fusion of flavours.",
     "Chinese Ching"],
    ["Manchurian Gravy", 120,
     "A savory and tangy Chinese-style sauce enveloping fried vegetable balls.",
     "Chinese Ching"],
    ["Palak Paneer", 150,
     "Creamy spinach curry with chunks of soft paneer, infused with aromatic spices.",
     "Vegetarian Verna"],
    ["Paneer Tikka Masala", 120,
     "Tender paneer cubes grilled and simmered in a rich, creamy tomato-based masala sauce.",
     "Vegetarian Verna"],
    ["Mutter Paneer", 110,
     "Soft paneer cubes and tender peas cooked in a flavourful tomato-based gravy.",
     "Vegetarian Verna"],
    ["Dal Tadka", 100,
     "Creamy lentils tempered with aromatic spices, offering a comforting and flavourful Indian staple.",
     "Vegetarian Verna"],
    ["Veg Biryani", 130,
     "Fragrant basmati rice cooked with an assortment of vegetables and aromatic spices.",
     "Vegetarian Verna"],
    ["Butter Chicken", 150,
     "Tender chicken pieces simmered in a creamy, tomato-based sauce infused with rich spices.",
     "Non-Vegetarian Delicacies"],
    ["Mutton Handi", 180,
     "Succulent pieces of mutton cooked in a rich and aromatic gravy, simmered in a traditional clay pot.",
     "Non-Vegetarian Delicacies"],
    ["Nalli Nihari", 190,
     "Tender lamb shanks slow-cooked in a flavourful gravy infused with aromatic spices.",
     "Non-Vegetarian Delicacies"],
    ["Chicken Biryani", 200,
     "Fragrant basmati rice cooked with succulent chicken pieces and aromatic spices.",
     "Non-Vegetarian Delicacies"],
    ["Gulab Jamun", 60,
     "Soft and syrupy milk-based balls infused with cardamom, rose water, and saffron.",
     "Desserts and Beverages"],
    ["Ras Malai", 80,
     "Soft and creamy cheese dumplings soaked in sweetened, flavoured milk, garnished with nuts.",
     "Desserts and Beverages"],
    ["Jalebi", 50,
     "Crispy, deep-fried swirls of dough soaked in sugary syrup with a hint of tanginess.",
     "Desserts and Beverages"],
    ["Citrus Splash", 120,
     "A refreshing blend of citrus fruits, bursting with tangy and zesty flavours.",
     "Desserts and Beverages"],
    ["Mango Mania", 140,
     "A tropical explosion of ripe mangoes, delivering a sweet and juicy burst of flavour.",
     "Desserts and Beverages"],
    ["Berry Blast Elixir", 160,
     "A vibrant fusion of assorted berries, creating a refreshing and invigorating drink.",
     "Desserts and Beverages"],
    ["Roti", 10,
     "Traditional Indian flatbread, perfectly baked to be soft and fluffy.",
     "Add Ons"],
    ["Kulcha", 15,
     "Soft, leavened bread, often served with a variety of dishes, including curries and dals.",
     "Add Ons"],
    ["Butter Naan", 15,
     "A rich and soft flatbread brushed with butter, perfect for scooping up flavourful curries.",
     "Add Ons"],
    ["Garlic Butter Naan", 18,
     "Delicious naan infused with garlic and a touch of butter, adding an extra layer of flavour.",
     "Add Ons"],
    ["Rumali Roti", 15,
     "Thin and soft Indian bread, known for its light texture and perfect for wrapping up food.",
     "Add Ons"],
    ["Parotta", 18,
     "Flaky and layered bread, known for its crispy texture and versatility with various dishes.",
     "Add Ons"],
]

CUISINES = [
    "Hotel Sunshine Special",
    "Starters",
    "South Indian",
    "Chinese Ching",
    "Vegetarian Verna",
    "Non-Vegetarian Delicacies",
    "Desserts and Beverages",
    "Add Ons",
]

ADMIN_CREDENTIALS = {
    "Jolebaba": "bankai",
    "Skibdi":   "bankai",
    "Joash":    "bankai",
}

# ── CSV helpers ─────────────────────────────────────────────────
def init_menu_csv():
    with open(MENU_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Item Name", "Price", "Description", "Cuisine"])
        w.writerows(MENU_DATA)


def read_menu():
    rows = []
    if not os.path.exists(MENU_FILE):
        init_menu_csv()
    with open(MENU_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) >= 4:
                rows.append(row)
    return rows


def write_menu(rows):
    with open(MENU_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Item Name", "Price", "Description", "Cuisine"])
        w.writerows(rows)


# ── Custom Widgets ───────────────────────────────────────────────
class RoundButton(tk.Canvas):
    """Canvas-based rounded rectangle button."""

    def __init__(self, parent, text, command=None, bg=ACCENT, fg=BG_DARK,
                 width=160, height=38, radius=10, **kwargs):
        try:
            pbg = parent["bg"]
        except Exception:
            pbg = BG_DARK
        super().__init__(parent, width=width, height=height,
                         bg=pbg, highlightthickness=0, **kwargs)
        self._bg = bg
        self._hover = self._lighten(bg)
        self._fg = fg
        self._text = text
        self._cmd = command
        self._r = radius
        self._width = width
        self._height = height
        self._draw(self._bg)
        self.bind("<Enter>", lambda e: self._draw(self._hover))
        self.bind("<Leave>", lambda e: self._draw(self._bg))
        self.bind("<Button-1>", lambda e: self._on_click())

    def _lighten(self, c):
        r = min(255, int(c[1:3], 16) + 30)
        g = min(255, int(c[3:5], 16) + 30)
        b = min(255, int(c[5:7], 16) + 30)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _draw(self, color):
        self.delete("all")
        r, w, h = self._r, self._width, self._height
        for x0, y0, x1, y1, s, e in [
            (0, 0, 2*r, 2*r, 90, 90),
            (w-2*r, 0, w, 2*r, 0, 90),
            (0, h-2*r, 2*r, h, 180, 90),
            (w-2*r, h-2*r, w, h, 270, 90),
        ]:
            self.create_arc(x0, y0, x1, y1, start=s, extent=e,
                            fill=color, outline=color)
        self.create_rectangle(r, 0, w-r, h, fill=color, outline=color)
        self.create_rectangle(0, r, w, h-r, fill=color, outline=color)
        self.create_text(w//2, h//2, text=self._text, fill=self._fg,
                         font=FONT_BTN, anchor="center")

    def _on_click(self):
        if self._cmd:
            self._cmd()


class HSep(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, height=1, bg=BORDER, **kw)


# ── Main Application ─────────────────────────────────────────────
class HotelMaraApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hotel Mara — Restaurant Management System")
        self.configure(bg=BG_DARK)
        self.resizable(True, True)
        w, h = 1150, 740
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        init_menu_csv()
        self.cart = []       # [[name, qty, unit_price], ...]
        self._build_ui()

    def _build_ui(self):
        # ─ Sidebar ────────────────────────────────────────────────
        self.sidebar = tk.Frame(self, bg=BG_PANEL, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        lf = tk.Frame(self.sidebar, bg=BG_PANEL, pady=20)
        lf.pack(fill="x")
        tk.Label(lf, text="Hotel Mara", font=("Georgia", 17, "bold"),
                 bg=BG_PANEL, fg=ACCENT).pack()
        tk.Label(lf, text="Near Thane Railway Station",
                 font=FONT_SMALL, bg=BG_PANEL, fg=TEXT_DIM).pack()

        HSep(self.sidebar).pack(fill="x", padx=16, pady=8)

        nav = [
            ("  Home",        self._show_home),
            ("  Order Food",  self._show_customer),
            ("  View Bill",   self._show_bill),
            ("  Admin Panel", self._show_admin_login),
        ]
        for label, cmd in nav:
            btn = tk.Label(self.sidebar, text=label, font=FONT_BODY_B,
                           bg=BG_PANEL, fg=TEXT_DIM, anchor="w",
                           padx=24, pady=12, cursor="hand2")
            btn.pack(fill="x")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#252550", fg=ACCENT))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=BG_PANEL, fg=TEXT_DIM))
            btn.bind("<Button-1>", lambda e, c=cmd: c())

        HSep(self.sidebar).pack(fill="x", padx=16, pady=8)
        self.cart_badge = tk.StringVar(value="Cart: 0 items")
        tk.Label(self.sidebar, textvariable=self.cart_badge,
                 font=FONT_SMALL, bg=BG_PANEL, fg=ACCENT2,
                 padx=24, pady=6).pack(fill="x")

        # ─ Content area ──────────────────────────────────────────
        self.content = tk.Frame(self, bg=BG_DARK)
        self.content.pack(side="left", fill="both", expand=True)

        self._frames = {}
        for Cls in (HomeFrame, CustomerFrame, BillFrame,
                    AdminLoginFrame, AdminPanelFrame):
            f = Cls(self.content, self)
            self._frames[Cls.__name__] = f
            f.place(relx=0, rely=0, relwidth=1, relheight=1)

        self._show_home()

    # ─ Navigation ────────────────────────────────────────────────
    def _show_frame(self, name):
        self._frames[name].tkraise()
        self._frames[name].on_show()

    def _show_home(self):        self._show_frame("HomeFrame")
    def _show_customer(self):    self._show_frame("CustomerFrame")
    def _show_bill(self):        self._show_frame("BillFrame")
    def _show_admin_login(self): self._show_frame("AdminLoginFrame")
    def show_admin_panel(self):  self._show_frame("AdminPanelFrame")

    def update_cart_badge(self):
        n = sum(i[1] for i in self.cart)
        self.cart_badge.set(f"Cart: {n} item{'s' if n != 1 else ''}")


# ── Home Frame ────────────────────────────────────────────────────
class HomeFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_DARK)
        self.app = app
        self._build()

    def _build(self):
        banner = tk.Frame(self, bg=BG_PANEL, pady=34)
        banner.pack(fill="x")
        tk.Label(banner, text="Hotel Mara", font=("Georgia", 30, "bold"),
                 bg=BG_PANEL, fg=ACCENT).pack()
        tk.Label(banner,
                 text='"Close to Thane Railway Station  |  Thane - 400614"',
                 font=("Georgia", 11, "italic"), bg=BG_PANEL, fg=TEXT_DIM).pack(pady=4)
        HSep(banner).pack(fill="x", padx=60, pady=10)
        tk.Label(banner, text="An exquisite culinary journey awaits you.",
                 font=("Helvetica", 12), bg=BG_PANEL, fg=TEXT_LIGHT).pack()

        row = tk.Frame(self, bg=BG_DARK)
        row.pack(pady=28, padx=40)

        cards = [
            ("Order Food",
             "Browse our menu by cuisine\nand add items to your cart.",
             self.app._show_customer, GREEN_SOFT),
            ("View Bill",
             "Review your cart and confirm\nor cancel your order.",
             self.app._show_bill, ACCENT),
            ("Admin Panel",
             "Manage menu items:\nadd, update, delete.",
             self.app._show_admin_login, RED_SOFT),
        ]
        for title, desc, cmd, color in cards:
            c = tk.Frame(row, bg=BG_CARD, padx=26, pady=26)
            c.pack(side="left", padx=16)
            tk.Label(c, text=title, font=FONT_HEADING, bg=BG_CARD,
                     fg=TEXT_LIGHT).pack(pady=(0, 6))
            tk.Label(c, text=desc, font=FONT_SMALL, bg=BG_CARD,
                     fg=TEXT_DIM, justify="center").pack(pady=(0, 14))
            RoundButton(c, text=f"Open {title}", command=cmd,
                        width=180, bg=color,
                        fg="white" if color != ACCENT else BG_DARK).pack()

        tf = tk.Frame(self, bg=BG_DARK)
        tf.pack(pady=14)
        tk.Label(tf, text="Available Cuisines", font=FONT_HEADING,
                 bg=BG_DARK, fg=ACCENT).pack(pady=(0, 8))
        r2 = tk.Frame(tf, bg=BG_DARK)
        r2.pack()
        for cuisine in CUISINES:
            tk.Label(r2, text=cuisine, font=FONT_SMALL,
                     bg=BG_PANEL, fg=ACCENT2, padx=10, pady=5).pack(
                         side="left", padx=4, pady=4)

    def on_show(self):
        pass


# ── Customer Frame ────────────────────────────────────────────────
class CustomerFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_DARK)
        self.app = app
        self._build()

    def _build(self):
        # Top bar
        topbar = tk.Frame(self, bg=BG_PANEL, pady=12)
        topbar.pack(fill="x")
        tk.Label(topbar, text="Order Food", font=FONT_TITLE,
                 bg=BG_PANEL, fg=ACCENT).pack(side="left", padx=20)
        RoundButton(topbar, text="View Bill", command=self.app._show_bill,
                    bg=GREEN_SOFT, fg="white", width=120, height=34).pack(
                        side="right", padx=20, pady=6)

        # Cuisine tab row
        tab_frame = tk.Frame(self, bg=BG_DARK, pady=6)
        tab_frame.pack(fill="x", padx=20)
        self._tab_btns = {}
        self._sel_cuisine = tk.StringVar(value=CUISINES[0])
        tabs_row = tk.Frame(tab_frame, bg=BG_DARK)
        tabs_row.pack(fill="x")
        for cuisine in CUISINES:
            btn = tk.Label(tabs_row, text=cuisine, font=FONT_SMALL,
                           bg=BG_PANEL, fg=TEXT_DIM, padx=10, pady=6,
                           cursor="hand2")
            btn.pack(side="left", padx=3)
            btn.bind("<Button-1>", lambda e, c=cuisine: self._select(c))
            self._tab_btns[cuisine] = btn

        # Body: menu list + cart
        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=10, pady=6)

        # Menu list (left)
        mf = tk.Frame(body, bg=BG_DARK)
        mf.pack(side="left", fill="both", expand=True, padx=(0, 6))
        tk.Label(mf, text="Menu Items", font=FONT_HEADING,
                 fg=ACCENT, bg=BG_DARK).pack(anchor="w", pady=(0, 6))

        mc = tk.Canvas(mf, bg=BG_DARK, highlightthickness=0)
        msb = ttk.Scrollbar(mf, orient="vertical", command=mc.yview)
        self.menu_inner = tk.Frame(mc, bg=BG_DARK)
        self.menu_inner.bind(
            "<Configure>",
            lambda e: mc.configure(scrollregion=mc.bbox("all")))
        mc.create_window((0, 0), window=self.menu_inner, anchor="nw")
        mc.configure(yscrollcommand=msb.set)
        mc.pack(side="left", fill="both", expand=True)
        msb.pack(side="right", fill="y")
        mc.bind_all("<MouseWheel>",
                    lambda e: mc.yview_scroll(-1*(e.delta//120), "units"))

        # Cart panel (right)
        cart_outer = tk.Frame(body, bg=BG_CARD, width=285)
        cart_outer.pack(side="right", fill="y", padx=(4, 0))
        cart_outer.pack_propagate(False)

        tk.Label(cart_outer, text="Your Cart", font=FONT_HEADING,
                 fg=ACCENT, bg=BG_CARD).pack(pady=(12, 4), padx=12, anchor="w")
        HSep(cart_outer).pack(fill="x", padx=10, pady=4)

        cc = tk.Canvas(cart_outer, bg=BG_CARD, highlightthickness=0, width=260)
        cs = ttk.Scrollbar(cart_outer, orient="vertical", command=cc.yview)
        self.cart_inner = tk.Frame(cc, bg=BG_CARD)
        self.cart_inner.bind(
            "<Configure>",
            lambda e: cc.configure(scrollregion=cc.bbox("all")))
        cc.create_window((0, 0), window=self.cart_inner, anchor="nw")
        cc.configure(yscrollcommand=cs.set)
        cc.pack(side="left", fill="both", expand=True)
        cs.pack(side="right", fill="y")

        HSep(cart_outer).pack(fill="x", padx=10, pady=4)
        self.total_var = tk.StringVar(value="Total: Rs.0.00")
        tk.Label(cart_outer, textvariable=self.total_var, font=FONT_BODY_B,
                 bg=BG_CARD, fg=ACCENT2).pack(pady=4)
        RoundButton(cart_outer, text="Proceed to Bill",
                    command=self.app._show_bill,
                    bg=GREEN_SOFT, fg="white", width=224, height=36).pack(pady=8)
        RoundButton(cart_outer, text="Clear Cart",
                    command=self._clear_cart,
                    bg=RED_SOFT, fg="white", width=224, height=36).pack(pady=(0, 12))

        self._select(CUISINES[0])

    # ─────────────────────────────────────────────────────────────
    def _select(self, cuisine):
        for c, btn in self._tab_btns.items():
            btn.config(
                bg=ACCENT if c == cuisine else BG_PANEL,
                fg=BG_DARK if c == cuisine else TEXT_DIM)
        self._sel_cuisine.set(cuisine)
        self._populate(cuisine)

    def _populate(self, cuisine):
        for w in self.menu_inner.winfo_children():
            w.destroy()
        items = [r for r in read_menu() if r[3].strip() == cuisine]
        if not items:
            tk.Label(self.menu_inner, text="No items for this cuisine.",
                     font=FONT_BODY, bg=BG_DARK, fg=TEXT_DIM).pack(pady=20)
            return
        for row in items:
            self._card(self.menu_inner, row[0], row[1], row[2])

    def _card(self, parent, name, price, desc):
        card = tk.Frame(parent, bg=BG_CARD)
        card.pack(fill="x", padx=6, pady=5, ipady=4, ipadx=4)

        left = tk.Frame(card, bg=BG_CARD)
        left.pack(side="left", fill="both", expand=True, padx=10, pady=6)
        tk.Label(left, text=name, font=FONT_BODY_B, bg=BG_CARD,
                 fg=TEXT_LIGHT, anchor="w").pack(anchor="w")
        tk.Label(left, text=f"Rs. {price}", font=("Helvetica", 11, "bold"),
                 bg=BG_CARD, fg=ACCENT, anchor="w").pack(anchor="w")
        tk.Label(left, text=desc, font=FONT_SMALL, bg=BG_CARD,
                 fg=TEXT_DIM, anchor="w", wraplength=470,
                 justify="left").pack(anchor="w", pady=(2, 0))

        right = tk.Frame(card, bg=BG_CARD)
        right.pack(side="right", padx=12, pady=10)

        qty_var = tk.IntVar(value=1)
        qf = tk.Frame(right, bg=BG_CARD)
        qf.pack(pady=4)
        tk.Button(qf, text="-", font=FONT_BODY_B, bg=BG_PANEL, fg=TEXT_LIGHT,
                  bd=0, padx=8, pady=2,
                  command=lambda: qty_var.set(max(1, qty_var.get()-1))).pack(side="left")
        tk.Label(qf, textvariable=qty_var, font=FONT_BODY_B,
                 bg=BG_CARD, fg=TEXT_LIGHT, width=3).pack(side="left")
        tk.Button(qf, text="+", font=FONT_BODY_B, bg=BG_PANEL, fg=TEXT_LIGHT,
                  bd=0, padx=8, pady=2,
                  command=lambda: qty_var.set(qty_var.get()+1)).pack(side="left")

        RoundButton(right, text="Add to Cart", width=110, height=30,
                    command=lambda n=name, p=price, q=qty_var:
                    self._add(n, int(p), q),
                    bg=ACCENT, fg=BG_DARK).pack(pady=4)

    def _add(self, name, price, qty_var):
        qty = qty_var.get()
        for item in self.app.cart:
            if item[0] == name:
                item[1] += qty
                self._refresh_cart()
                self.app.update_cart_badge()
                return
        self.app.cart.append([name, qty, price])
        self._refresh_cart()
        self.app.update_cart_badge()

    def _refresh_cart(self):
        for w in self.cart_inner.winfo_children():
            w.destroy()
        total = 0
        for item in self.app.cart:
            name, qty, price = item
            row = tk.Frame(self.cart_inner, bg=BG_CARD)
            row.pack(fill="x", padx=6, pady=3)
            tk.Label(row, text=name, font=FONT_SMALL, bg=BG_CARD,
                     fg=TEXT_LIGHT, anchor="w", wraplength=150).pack(
                         side="left", fill="x", expand=True)
            tk.Label(row, text=f"x{qty}  Rs.{qty*price}",
                     font=FONT_SMALL, bg=BG_CARD, fg=ACCENT2).pack(side="right")
            tk.Button(row, text="X", font=("Helvetica", 8),
                      bg=BG_CARD, fg=RED_SOFT, bd=0,
                      command=lambda n=name: self._remove(n)).pack(side="right")
            total += qty * price
        tax = total * 0.05
        grand = total + tax
        self.total_var.set(
            f"Sub: Rs.{total:.2f}  |  Total: Rs.{grand:.2f}")

    def _remove(self, name):
        self.app.cart = [i for i in self.app.cart if i[0] != name]
        self._refresh_cart()
        self.app.update_cart_badge()

    def _clear_cart(self):
        if messagebox.askyesno("Clear Cart", "Remove all items from cart?"):
            self.app.cart.clear()
            self._refresh_cart()
            self.app.update_cart_badge()

    def on_show(self):
        self._select(self._sel_cuisine.get())
        self._refresh_cart()


# ── Bill Frame ────────────────────────────────────────────────────
class BillFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_DARK)
        self.app = app
        self._build()

    def _build(self):
        topbar = tk.Frame(self, bg=BG_PANEL, pady=14)
        topbar.pack(fill="x")
        tk.Label(topbar, text="Your Bill", font=FONT_TITLE,
                 bg=BG_PANEL, fg=ACCENT).pack(side="left", padx=20)

        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=40, pady=20)

        # Table
        bill_frame = tk.Frame(body, bg=BG_CARD)
        bill_frame.pack(fill="both", expand=True)

        hdr = tk.Frame(bill_frame, bg=ACCENT)
        hdr.pack(fill="x")
        for col, w in [("Item Name", 40), ("Qty", 8),
                        ("Unit Price", 14), ("Amount", 14)]:
            tk.Label(hdr, text=col, font=FONT_BODY_B,
                     bg=ACCENT, fg=BG_DARK, width=w,
                     anchor="w", padx=8, pady=6).pack(side="left")

        tc = tk.Canvas(bill_frame, bg=BG_CARD, highlightthickness=0)
        ts = ttk.Scrollbar(bill_frame, orient="vertical", command=tc.yview)
        self.tbl_inner = tk.Frame(tc, bg=BG_CARD)
        self.tbl_inner.bind(
            "<Configure>",
            lambda e: tc.configure(scrollregion=tc.bbox("all")))
        tc.create_window((0, 0), window=self.tbl_inner, anchor="nw")
        tc.configure(yscrollcommand=ts.set)
        tc.pack(side="left", fill="both", expand=True)
        ts.pack(side="right", fill="y")

        # Totals
        totals_bar = tk.Frame(body, bg=BG_PANEL, pady=12)
        totals_bar.pack(fill="x", pady=(12, 0))
        self.sub_var   = tk.StringVar(value="Subtotal:    Rs.0.00")
        self.tax_var   = tk.StringVar(value="Tax (5%):    Rs.0.00")
        self.grand_var = tk.StringVar(value="Grand Total: Rs.0.00")
        tk.Label(totals_bar, textvariable=self.sub_var,
                 font=FONT_BODY_B, bg=BG_PANEL, fg=TEXT_LIGHT).pack(
                     anchor="e", padx=30)
        tk.Label(totals_bar, textvariable=self.tax_var,
                 font=FONT_BODY_B, bg=BG_PANEL, fg=TEXT_DIM).pack(
                     anchor="e", padx=30)
        tk.Label(totals_bar, textvariable=self.grand_var,
                 font=FONT_HEADING, bg=BG_PANEL, fg=ACCENT).pack(
                     anchor="e", padx=30)

        tk.Label(body,
                 text="Currently, only Cash on Delivery is available.",
                 font=FONT_SMALL, bg=BG_DARK, fg=TEXT_DIM).pack(pady=8)

        btn_row = tk.Frame(body, bg=BG_DARK)
        btn_row.pack(pady=6)
        RoundButton(btn_row, text="Confirm Order",
                    command=self._confirm,
                    bg=GREEN_SOFT, fg="white",
                    width=180, height=40).pack(side="left", padx=10)
        RoundButton(btn_row, text="Cancel Order",
                    command=self._cancel,
                    bg=RED_SOFT, fg="white",
                    width=180, height=40).pack(side="left", padx=10)
        RoundButton(btn_row, text="Back to Menu",
                    command=self.app._show_customer,
                    bg=BG_PANEL, fg=TEXT_LIGHT,
                    width=160, height=40).pack(side="left", padx=10)

    def _refresh(self):
        for w in self.tbl_inner.winfo_children():
            w.destroy()
        merged = {}
        for name, qty, price in self.app.cart:
            if name in merged:
                merged[name][0] += qty
            else:
                merged[name] = [qty, price]

        total = 0
        for idx, (name, (qty, price)) in enumerate(merged.items()):
            amt = qty * price
            total += amt
            rbg = BG_CARD if idx % 2 == 0 else BG_PANEL
            row = tk.Frame(self.tbl_inner, bg=rbg)
            row.pack(fill="x")
            for val, w in [(name, 40), (str(qty), 8),
                           (f"Rs.{price}", 14), (f"Rs.{amt}", 14)]:
                tk.Label(row, text=val, font=FONT_BODY,
                         bg=rbg, fg=TEXT_LIGHT, width=w,
                         anchor="w", padx=8, pady=5).pack(side="left")

        tax   = total * 0.05
        grand = total + tax
        self.sub_var.set(  f"Subtotal:    Rs.{total:.2f}")
        self.tax_var.set(  f"Tax (5%):    Rs.{tax:.2f}")
        self.grand_var.set(f"Grand Total: Rs.{grand:.2f}")

        if self.app.cart:
            with open(BILL_FILE, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["Item Name", "Quantity", "Unit Price", "Amount"])
                for name, (qty, price) in merged.items():
                    w.writerow([name, qty, price, qty*price])

    def _confirm(self):
        if not self.app.cart:
            messagebox.showinfo("Empty Cart", "Add some items first!")
            return
        messagebox.showinfo(
            "Order Confirmed",
            "Your order has been confirmed!\nThank you for dining with Hotel Mara.")
        self.app.cart.clear()
        self.app.update_cart_badge()
        self._refresh()
        self.app._show_home()

    def _cancel(self):
        if not self.app.cart:
            messagebox.showinfo("Empty Cart", "Nothing to cancel.")
            return
        if messagebox.askyesno("Cancel Order",
                               "Are you sure you want to cancel?"):
            self.app.cart.clear()
            self.app.update_cart_badge()
            self._refresh()
            messagebox.showinfo("Cancelled",
                                "Your order has been cancelled. Have a great day!")
            self.app._show_home()

    def on_show(self):
        self._refresh()


# ── Admin Login Frame ─────────────────────────────────────────────
class AdminLoginFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_DARK)
        self.app = app
        self._build()

    def _build(self):
        wrap = tk.Frame(self, bg=BG_DARK)
        wrap.place(relx=0.5, rely=0.5, anchor="center")

        card = tk.Frame(wrap, bg=BG_CARD, padx=50, pady=40)
        card.pack()

        tk.Label(card, text="Admin Login", font=("Georgia", 20, "bold"),
                 bg=BG_CARD, fg=ACCENT).pack(pady=(0, 20))

        tk.Label(card, text="Admin Username", font=FONT_BODY,
                 bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w")
        self.user_entry = tk.Entry(card, font=FONT_BODY, bg=BG_PANEL,
                                   fg=TEXT_LIGHT, insertbackground=ACCENT,
                                   bd=0, width=28)
        self.user_entry.pack(ipady=8, pady=(2, 12), fill="x")

        tk.Label(card, text="Password", font=FONT_BODY,
                 bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w")
        self.pass_entry = tk.Entry(card, font=FONT_BODY, bg=BG_PANEL,
                                   fg=TEXT_LIGHT, insertbackground=ACCENT,
                                   bd=0, width=28, show="*")
        self.pass_entry.pack(ipady=8, pady=(2, 18), fill="x")
        self.pass_entry.bind("<Return>", lambda e: self._login())

        self.err_var = tk.StringVar()
        tk.Label(card, textvariable=self.err_var, font=FONT_SMALL,
                 bg=BG_CARD, fg=RED_SOFT).pack(pady=(0, 8))

        RoundButton(card, text="Login", command=self._login,
                    bg=ACCENT, fg=BG_DARK, width=200, height=40).pack(pady=4)
        RoundButton(card, text="Back to Home",
                    command=self.app._show_home,
                    bg=BG_PANEL, fg=TEXT_LIGHT,
                    width=200, height=36).pack(pady=6)

        tk.Label(card, text="Authorised personnel only.",
                 font=FONT_SMALL, bg=BG_CARD, fg=TEXT_DIM).pack(pady=(10, 0))

    def _login(self):
        u = self.user_entry.get().strip()
        p = self.pass_entry.get().strip()
        if ADMIN_CREDENTIALS.get(u) == p:
            self.err_var.set("")
            self.user_entry.delete(0, "end")
            self.pass_entry.delete(0, "end")
            self.app.show_admin_panel()
        else:
            self.err_var.set("Wrong username or password. Access Denied.")

    def on_show(self):
        self.err_var.set("")
        self.user_entry.focus_set()


# ── Admin Panel Frame ─────────────────────────────────────────────
class AdminPanelFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_DARK)
        self.app = app
        self._built_tabs = {}
        self._upd_original_name = None
        self._build()

    def _build(self):
        topbar = tk.Frame(self, bg=BG_PANEL, pady=10)
        topbar.pack(fill="x")
        tk.Label(topbar, text="Admin Panel", font=FONT_TITLE,
                 bg=BG_PANEL, fg=ACCENT).pack(side="left", padx=20)
        RoundButton(topbar, text="Logout",
                    command=self.app._show_home,
                    bg=RED_SOFT, fg="white",
                    width=100, height=32).pack(side="right", padx=20, pady=8)

        # Tab bar
        tab_bar = tk.Frame(self, bg=BG_DARK)
        tab_bar.pack(fill="x", padx=10, pady=6)
        self._admin_tabs = {}
        for label, key in [
            ("Display Menu", "display"),
            ("Add Item",     "add"),
            ("Update Item",  "update"),
            ("Delete Item",  "delete"),
        ]:
            btn = tk.Label(tab_bar, text=label, font=FONT_BODY_B,
                           bg=BG_PANEL, fg=TEXT_DIM, padx=14, pady=8,
                           cursor="hand2")
            btn.pack(side="left", padx=4)
            btn.bind("<Button-1>", lambda e, k=key: self._show_tab(k))
            self._admin_tabs[key] = btn

        self.tab_content = tk.Frame(self, bg=BG_DARK)
        self.tab_content.pack(fill="both", expand=True, padx=10, pady=6)

        self._tab_builders = {
            "display": self._build_display_tab,
            "add":     self._build_add_tab,
            "update":  self._build_update_tab,
            "delete":  self._build_delete_tab,
        }
        self._show_tab("display")

    def _show_tab(self, key):
        for k, btn in self._admin_tabs.items():
            btn.config(
                bg=ACCENT if k == key else BG_PANEL,
                fg=BG_DARK if k == key else TEXT_DIM)
        if key not in self._built_tabs:
            frame = tk.Frame(self.tab_content, bg=BG_DARK)
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            self._tab_builders[key](frame)
            self._built_tabs[key] = frame
        self._built_tabs[key].tkraise()
        if key == "display":
            self._refresh_display()

    # ─ Display Tab ───────────────────────────────────────────────
    def _build_display_tab(self, frame):
        fb = tk.Frame(frame, bg=BG_DARK)
        fb.pack(fill="x", pady=6, padx=6)
        tk.Label(fb, text="Filter by cuisine:", font=FONT_BODY,
                 bg=BG_DARK, fg=TEXT_DIM).pack(side="left", padx=(0, 8))
        self.filter_var = tk.StringVar(value="All")
        fm = ttk.Combobox(fb, textvariable=self.filter_var,
                          values=["All"] + CUISINES,
                          state="readonly", width=24)
        fm.pack(side="left")
        fm.bind("<<ComboboxSelected>>", lambda e: self._refresh_display())
        RoundButton(fb, text="Refresh", command=self._refresh_display,
                    bg=BG_PANEL, fg=ACCENT, width=100, height=28).pack(
                        side="left", padx=10)

        hdr_frame = tk.Frame(frame, bg=ACCENT)
        hdr_frame.pack(fill="x", padx=6)
        for col, w in [("Item Name", 30), ("Price", 8),
                        ("Cuisine", 18), ("Description", 44)]:
            tk.Label(hdr_frame, text=col, font=FONT_BODY_B,
                     bg=ACCENT, fg=BG_DARK, width=w,
                     anchor="w", padx=4, pady=6).pack(side="left")

        canvas = tk.Canvas(frame, bg=BG_DARK, highlightthickness=0)
        sb = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        self.display_inner = tk.Frame(canvas, bg=BG_DARK)
        self.display_inner.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.display_inner, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True, padx=6)
        sb.pack(side="right", fill="y")

    def _refresh_display(self):
        if not hasattr(self, "display_inner"):
            return
        for w in self.display_inner.winfo_children():
            w.destroy()
        rows = read_menu()
        cf = self.filter_var.get()
        if cf != "All":
            rows = [r for r in rows if r[3].strip() == cf]
        for idx, (name, price, desc, cuisine) in enumerate(rows):
            bg = BG_CARD if idx % 2 == 0 else BG_PANEL
            r = tk.Frame(self.display_inner, bg=bg)
            r.pack(fill="x")
            for val, w in [(name, 30), (f"Rs.{price}", 8),
                           (cuisine, 18), (desc, 44)]:
                tk.Label(r, text=val, font=FONT_SMALL, bg=bg,
                         fg=TEXT_LIGHT, width=w, anchor="w",
                         padx=4, pady=5).pack(side="left")

    # ─ Add Tab ───────────────────────────────────────────────────
    def _build_add_tab(self, frame):
        wrap = tk.Frame(frame, bg=BG_DARK)
        wrap.place(relx=0.5, rely=0.5, anchor="center")
        card = tk.Frame(wrap, bg=BG_CARD, padx=40, pady=30)
        card.pack()
        tk.Label(card, text="Add New Menu Item", font=FONT_HEADING,
                 fg=ACCENT, bg=BG_CARD).pack(pady=(0, 16))

        self._add_vars = {}
        for label, key in [("Item Name", "name"),
                            ("Price (integer)", "price"),
                            ("Description", "desc"),
                            ("Cuisine", "cuisine")]:
            tk.Label(card, text=label, font=FONT_BODY,
                     bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w")
            if key == "desc":
                t = tk.Text(card, font=FONT_BODY, bg=BG_PANEL,
                            fg=TEXT_LIGHT, insertbackground=ACCENT,
                            bd=0, width=48, height=4)
                t.pack(ipady=4, pady=(2, 12), fill="x")
                self._add_vars[key] = t
            elif key == "cuisine":
                v = tk.StringVar(value=CUISINES[0])
                cb = ttk.Combobox(card, textvariable=v,
                                  values=CUISINES, state="readonly", width=46)
                cb.pack(ipady=4, pady=(2, 12), fill="x")
                self._add_vars[key] = v
            else:
                v = tk.StringVar()
                tk.Entry(card, textvariable=v, font=FONT_BODY,
                         bg=BG_PANEL, fg=TEXT_LIGHT,
                         insertbackground=ACCENT, bd=0, width=48).pack(
                             ipady=8, pady=(2, 12), fill="x")
                self._add_vars[key] = v

        self._add_msg = tk.StringVar()
        tk.Label(card, textvariable=self._add_msg, font=FONT_SMALL,
                 bg=BG_CARD, fg=GREEN_SOFT, wraplength=400).pack(pady=(0, 8))
        RoundButton(card, text="Add Item", command=self._do_add,
                    bg=ACCENT, fg=BG_DARK, width=220, height=40).pack()

    def _do_add(self):
        name    = self._add_vars["name"].get().strip()
        price_s = self._add_vars["price"].get().strip()
        desc_w  = self._add_vars["desc"]
        desc    = (desc_w.get("1.0", "end").strip()
                   if isinstance(desc_w, tk.Text) else desc_w.get().strip())
        cuisine = self._add_vars["cuisine"].get().strip()

        if not name or not price_s or not desc or not cuisine:
            self._add_msg.set("All fields are required.")
            return
        try:
            price = int(price_s)
        except ValueError:
            self._add_msg.set("Price must be an integer.")
            return
        for r in read_menu():
            if r[0].strip().lower() == name.lower():
                self._add_msg.set(f"'{name}' already exists in the menu.")
                return

        with open(MENU_FILE, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([name, price, desc, cuisine])
        self._add_msg.set(f"'{name}' added successfully!")
        self._add_vars["name"].set("")
        self._add_vars["price"].set("")
        if isinstance(desc_w, tk.Text):
            desc_w.delete("1.0", "end")

    # ─ Update Tab ────────────────────────────────────────────────
    def _build_update_tab(self, frame):
        left = tk.Frame(frame, bg=BG_DARK, width=280)
        left.pack(side="left", fill="y", padx=(10, 0), pady=10)
        left.pack_propagate(False)

        tk.Label(left, text="Select Item", font=FONT_HEADING,
                 fg=ACCENT, bg=BG_DARK).pack(anchor="w", pady=(0, 6))
        self.update_lb = tk.Listbox(
            left, bg=BG_CARD, fg=TEXT_LIGHT,
            selectbackground=ACCENT, selectforeground=BG_DARK,
            font=FONT_SMALL, bd=0, activestyle="none")
        self.update_lb.pack(fill="both", expand=True)
        self.update_lb.bind("<<ListboxSelect>>", self._load_update)
        RoundButton(left, text="Refresh List",
                    command=self._populate_update_list,
                    bg=BG_PANEL, fg=ACCENT, width=220, height=30).pack(pady=8)

        right = tk.Frame(frame, bg=BG_DARK)
        right.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        card = tk.Frame(right, bg=BG_CARD, padx=30, pady=20)
        card.pack(fill="both", expand=True)
        tk.Label(card, text="Edit Item Details", font=FONT_HEADING,
                 fg=ACCENT, bg=BG_CARD).pack(pady=(0, 14))

        self._upd_vars = {}
        for label, key in [("Item Name", "name"),
                            ("Price", "price"),
                            ("Description", "desc"),
                            ("Cuisine", "cuisine")]:
            tk.Label(card, text=label, font=FONT_BODY,
                     bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w")
            if key == "desc":
                t = tk.Text(card, font=FONT_BODY, bg=BG_PANEL,
                            fg=TEXT_LIGHT, insertbackground=ACCENT,
                            bd=0, width=52, height=4)
                t.pack(ipady=4, pady=(2, 10), fill="x")
                self._upd_vars[key] = t
            elif key == "cuisine":
                v = tk.StringVar()
                cb = ttk.Combobox(card, textvariable=v,
                                  values=CUISINES, state="readonly", width=50)
                cb.pack(ipady=4, pady=(2, 10), fill="x")
                self._upd_vars[key] = v
            else:
                v = tk.StringVar()
                tk.Entry(card, textvariable=v, font=FONT_BODY,
                         bg=BG_PANEL, fg=TEXT_LIGHT,
                         insertbackground=ACCENT, bd=0, width=52).pack(
                             ipady=8, pady=(2, 10), fill="x")
                self._upd_vars[key] = v

        self._upd_msg = tk.StringVar()
        tk.Label(card, textvariable=self._upd_msg, font=FONT_SMALL,
                 bg=BG_CARD, fg=GREEN_SOFT, wraplength=400).pack(pady=(0, 8))
        RoundButton(card, text="Save Changes", command=self._do_update,
                    bg=ACCENT, fg=BG_DARK, width=220, height=40).pack()

        self._populate_update_list()

    def _populate_update_list(self):
        self.update_lb.delete(0, "end")
        for row in read_menu():
            self.update_lb.insert("end", row[0])

    def _load_update(self, event=None):
        sel = self.update_lb.curselection()
        if not sel:
            return
        name = self.update_lb.get(sel[0])
        for row in read_menu():
            if row[0].strip() == name.strip():
                self._upd_original_name = row[0]
                self._upd_vars["name"].set(row[0])
                self._upd_vars["price"].set(row[1])
                dw = self._upd_vars["desc"]
                if isinstance(dw, tk.Text):
                    dw.delete("1.0", "end")
                    dw.insert("1.0", row[2])
                self._upd_vars["cuisine"].set(row[3])
                self._upd_msg.set("")
                break

    def _do_update(self):
        if not self._upd_original_name:
            self._upd_msg.set("Select an item from the list first.")
            return
        new_name = self._upd_vars["name"].get().strip()
        price_s  = self._upd_vars["price"].get().strip()
        dw       = self._upd_vars["desc"]
        new_desc = (dw.get("1.0", "end").strip()
                    if isinstance(dw, tk.Text) else dw.get().strip())
        new_cuisine = self._upd_vars["cuisine"].get().strip()

        if not new_name or not price_s or not new_desc or not new_cuisine:
            self._upd_msg.set("All fields are required.")
            return
        try:
            new_price = int(price_s)
        except ValueError:
            self._upd_msg.set("Price must be an integer.")
            return

        rows = read_menu()
        updated = [
            [new_name, new_price, new_desc, new_cuisine]
            if r[0].strip() == self._upd_original_name.strip() else r
            for r in rows
        ]
        write_menu(updated)
        self._upd_msg.set(f"'{self._upd_original_name}' updated successfully!")
        self._upd_original_name = new_name
        self._populate_update_list()

    # ─ Delete Tab ────────────────────────────────────────────────
    def _build_delete_tab(self, frame):
        wrap = tk.Frame(frame, bg=BG_DARK)
        wrap.place(relx=0.5, rely=0.5, anchor="center")
        card = tk.Frame(wrap, bg=BG_CARD, padx=50, pady=40)
        card.pack()
        tk.Label(card, text="Delete Menu Item", font=FONT_HEADING,
                 fg=ACCENT, bg=BG_CARD).pack(pady=(0, 14))
        tk.Label(card, text="Select Item to Delete", font=FONT_BODY,
                 bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w")
        self.del_var = tk.StringVar()
        self.del_combo = ttk.Combobox(
            card, textvariable=self.del_var,
            values=[r[0] for r in read_menu()],
            state="readonly", width=44)
        self.del_combo.pack(ipady=6, pady=(4, 16), fill="x")
        RoundButton(card, text="Refresh List",
                    command=self._refresh_del,
                    bg=BG_PANEL, fg=ACCENT, width=200, height=30).pack(pady=(0, 10))
        self._del_msg = tk.StringVar()
        tk.Label(card, textvariable=self._del_msg, font=FONT_SMALL,
                 bg=BG_CARD, fg=RED_SOFT, wraplength=400).pack(pady=(0, 8))
        RoundButton(card, text="Delete Item", command=self._do_delete,
                    bg=RED_SOFT, fg="white", width=220, height=40).pack()

    def _refresh_del(self):
        self.del_combo["values"] = [r[0] for r in read_menu()]
        self._del_msg.set("List refreshed.")

    def _do_delete(self):
        name = self.del_var.get().strip()
        if not name:
            self._del_msg.set("Please select an item first.")
            return
        if not messagebox.askyesno(
                "Confirm Delete",
                f"Delete '{name}' from the menu?\nA backup will be saved in DeletedRecords.csv."):
            return
        rows = read_menu()
        deleted_row = None
        new_rows = []
        for r in rows:
            if r[0].strip() == name.strip():
                deleted_row = r
            else:
                new_rows.append(r)
        if not deleted_row:
            self._del_msg.set("Item not found.")
            return
        write_menu(new_rows)
        with open(DELETED_FILE, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(deleted_row)
        self._del_msg.set(f"'{name}' deleted. Saved in DeletedRecords.csv.")
        self._refresh_del()
        self.del_var.set("")

    def on_show(self):
        self._refresh_display()
        self._populate_update_list()
        self._refresh_del()


# ── Entry Point ───────────────────────────────────────────────────
if __name__ == "__main__":
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass
    style.configure(
        "TScrollbar",
        troughcolor=BG_DARK, background=ACCENT,
        bordercolor=BG_DARK, arrowcolor=TEXT_LIGHT)
    style.configure(
        "TCombobox",
        fieldbackground=BG_PANEL, background=BG_PANEL,
        foreground=TEXT_LIGHT)
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", BG_PANEL)],
        foreground=[("readonly", TEXT_LIGHT)])

    app = HotelMaraApp()
    app.mainloop()
