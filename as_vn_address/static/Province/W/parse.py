# -*- coding: utf-8 -*-
import xlrd
import re
import os.path


INTAB = "ạảãàáâậầấẩẫăắằặẳẵóòọõỏôộổỗồốơờớợởỡéèẻẹẽêếềệểễúùụủũưựữửừứíìịỉĩýỳỷỵỹđẠẢÃÀÁÂẬẦẤẨẪĂẮẰẶẲẴÓÒỌÕỎÔỘỔỖỒỐƠỜỚỢỞỠÉÈẺẸẼÊẾỀỆỂỄÚÙỤỦŨƯỰỮỬỪỨÍÌỊỈĨÝỲỶỴỸĐ"
INTAB = [str(ch) for ch in str(INTAB)]


OUTTAB = "a" * 17 + "o" * 17 + "e" * 11 + "u" * 11 + "i" * 5 + "y" * 5 + "d" + \
         "A" * 17 + "O" * 17 + "E" * 11 + "U" * 11 + "I" * 5 + "Y" * 5 + "D"

r = re.compile("|".join(INTAB))
replaces_dict = dict(zip(INTAB, OUTTAB))

def no_accent_vietnamese(utf8_str):
	return r.sub(lambda m: replaces_dict[m.group(0)], utf8_str)

def get_code_state(input):
	spl = input.split(' ')
	output = '_'.join(spl)
	return 'VN_' + output.upper()
#
myfile = open('ward.xml', 'a')
myfile.write('<?xml version="1.0" encoding="utf-8"?>' + '\n')
myfile.write('<odoo>' + '\n')
myfile.write('	<data noupdate="1">' + '\n')
#
file_name = '01.xls'
if os.path.isfile(file_name):
	book = xlrd.open_workbook(file_name)
	first_sheet = book.sheet_by_index(0)
	#
	print(first_sheet.nrows)
	for i in range(1, first_sheet.nrows):
		#
		name = first_sheet.cell(i,4).value
		code = first_sheet.cell(i,5).value
		district = first_sheet.cell(i,3).value
		#
		myfile.write('		<record id="' + 'ward_' + code + '" model="res.country.ward">' + '\n')
		myfile.write('			<field name="name">' + name + '</field>' + '\n')
		myfile.write('			<field name="code">' + code + '</field>' + '\n')
		myfile.write('			<field name="active" eval="True"/>' + '\n')
		myfile.write('			<field name="district_id" ref="district_' + district + '"/>' + '\n')
		myfile.write('		</record>' + '\n')
#

myfile.write('	</data>' + '\n')
myfile.write('</odoo>')
myfile.close()