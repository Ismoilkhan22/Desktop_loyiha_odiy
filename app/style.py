"""10-qadam: dasturning tashqi ko'rinishi (QSS = Qt uchun CSS). Mantiqqa tegmaydi."""

QSS = """
QWidget { background: #f1f5f9; color: #0f172a; font-size: 14px; }
QLabel { background: transparent; }

/* yon panel */
#sidebar { background: #1e293b; }
#brand { background: transparent; color: white; font-size: 17px; font-weight: 700; padding: 18px 16px 10px 16px; }
#menu { background: #1e293b; border: none; outline: none; padding: 6px; color: #cbd5e1; }
#menu::item { padding: 11px 14px; border-radius: 8px; margin: 2px 0; }
#menu::item:hover { background: #334155; }
#menu::item:selected { background: #2563eb; color: white; }

/* sahifa sarlavhasi va kartalar */
#title { font-size: 24px; font-weight: 700; }
#card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; }
#cardnum { color: #2563eb; font-size: 36px; font-weight: 700; }
#cardlabel { color: #64748b; font-size: 14px; }

/* jadval */
QTableWidget { background: white; alternate-background-color: #f8fafc; border: 1px solid #e2e8f0;
               border-radius: 10px; gridline-color: transparent; selection-background-color: #dbeafe;
               selection-color: #0f172a; outline: none; }
QTableWidget::item { padding: 6px 10px; }
QHeaderView { background: #f1f5f9; }
QHeaderView::section { background: #f1f5f9; color: #475569; padding: 10px; border: none;
                       border-bottom: 1px solid #e2e8f0; font-weight: 700; }

/* kiritish maydonlari */
QLineEdit, QSpinBox, QDateEdit, QComboBox { background: white; border: 1px solid #cbd5e1; border-radius: 8px;
                                            padding: 7px 10px; min-height: 20px; }
QLineEdit:focus, QSpinBox:focus, QDateEdit:focus, QComboBox:focus { border: 1px solid #2563eb; }
QComboBox QAbstractItemView { background: white; selection-background-color: #dbeafe; selection-color: #0f172a; }
QDialog { background: white; }

/* tugmalar */
QPushButton { background: #e2e8f0; border: none; border-radius: 8px; padding: 9px 18px; font-weight: 600; }
QPushButton:hover { background: #cbd5e1; }
QPushButton[kind="primary"] { background: #2563eb; color: white; }
QPushButton[kind="primary"]:hover { background: #1d4ed8; }
QPushButton[kind="danger"] { background: #fee2e2; color: #b91c1c; }
QPushButton[kind="danger"]:hover { background: #fecaca; }
"""
