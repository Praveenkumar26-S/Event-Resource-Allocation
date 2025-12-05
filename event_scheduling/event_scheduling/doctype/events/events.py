# Copyright (c) 2025, Praveen and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Events(Document):
	def validate(self):
		self.check_time()
		self.check_duplicates()

	def check_time(self):
		if self.start_time >= self.end_time:
			frappe.throw("Start time must be less than End time.")

	def check_duplicates(self):
		doc = frappe.get_all("Events",["title","start_time","end_time"],{"title":self.title,"start_time":self.start_time,"end_time":self.end_time})
		if doc:
			frappe.throw("An event with the same title and time already exists.")

