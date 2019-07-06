# -*- coding: utf-8 -*-
import xlrd
import re


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


book = xlrd.open_workbook('City.xls')
first_sheet = book.sheet_by_index(0)
#
myfile = open('province.xml', 'a')
myfile.write('<?xml version="1.0" encoding="utf-8"?>' + '\n')
myfile.write('<odoo>' + '\n')
myfile.write('	<data noupdate="1">' + '\n')
#
for i in range(1, 64):
	code = first_sheet.cell(i,0)
	name = first_sheet.cell(i,1)
	level = first_sheet.cell(i,3)
	
	raw_code = name.value
	raw_code = raw_code.replace('Thành phố ', '')
	raw_code = raw_code.replace('Tỉnh ', '')
	raw_code = raw_code.replace(' - ', ' ')
	
	final_code = no_accent_vietnamese(get_code_state(raw_code))

	myfile.write('		<record id="' + 'vn_province_' + code.value + '" model="res.country.province">' + '\n')
	myfile.write('			<field name="name">' + name.value + '</field>' + '\n')
	myfile.write('			<field name="code">' + code.value + '</field>' + '\n')
	myfile.write('			<field name="active" eval="True"/>' + '\n')
	myfile.write('			<field name="country_id" ref="base.vn"/>' + '\n')
	myfile.write('		</record>' + '\n')
#
myfile.write('	</data>' + '\n')
myfile.write('</odoo>')
myfile.close()
