import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog
from tkcalendar import DateEntry, Calendar
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        # Create tables if they don't exist
        pass

    def insert_data(self, data):
        # Code to insert data
        pass

    def update_data(self, data):
        # Code to update data
        pass

    def delete_data(self, id):
        # Code to delete data
        pass

    def fetch_data(self):
        # Code to fetch all data
        pass

    def fetch_resit_data(self):
        # Code to fetch all resit data
        pass
