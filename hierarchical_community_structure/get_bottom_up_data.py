from subprocess import Popen, PIPE
import xlsxwriter

workbook = xlsxwriter.Workbook('GetBottomUpData.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write(0, 0, 'Arg k')
worksheet.write(0, 1, 'Arg c')
worksheet.write(0, 2, 'Arg k_minus')
worksheet.write(0, 3, 'Level')
worksheet.write(0, 4, 'i')
worksheet.write(0, 5, 'k')
worksheet.write(0, 6, 'i/k')
worksheet.write(0, 7, 'q')


k_s = [1000, 200000000, 100, 5000]
c_s = [2, 3, 4, 5, 10, 100, 1000]
k_minuses = [0, 1, 2, 3, 4]

row = 1

for k in k_s:
	for c in c_s:
		for k_minus in k_minuses:
			col = 0
			process = Popen(['python', './generate_hierarchy_bottom_up.py', str(k), str(c)], stdout=PIPE)
			(output, err) = process.communicate()
			exit_code = process.wait()
			output = output.decode('utf-8')
			for line in output.splitlines():
				words = line.split(' ')
				worksheet.write(row, 0, k)
				worksheet.write(row, 1, c)
				worksheet.write(row, 2, k_minus)
				worksheet.write(row, 3, words[1])
				worksheet.write(row, 4, words[3])
				worksheet.write(row, 5, words[5])
				worksheet.write(row, 6, words[7])
				worksheet.write(row, 7, words[9])

			row = row + 1

workbook.close()
