import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog
from tkcalendar import DateEntry, Calendar
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
