import os, sys, re, argparse
from colorama import init, Fore, Back, Style
import epub_meta
from chardet.universaldetector import UniversalDetector
from progress.bar import IncrementalBar 

# from PyPDF2 import PdfFileReader

'''
	TODO
	Добавить поддержку форматов pdf, epub, djvu, mobi, fb3 ... 
	Два реплейса заменить на один шаблон
	Добавить рекурсивный проход по дереву дирректорий (поумолчанию скрипт работает только в данной папке)
	Добавить конфиг 
	Проверить запускается ли с аргументом екзешник
	Подчинить прогрессбар
	Проверить програесс бар на большом количестве файлов на выход за границы массива
	Сделать так, что бы уже переименованые файлы больше непереименовывались
	Сделать команду для консоли 
	Сделать пунктв контекстном меню
'''

init(autoreset=True) #colorama

def createParser(): 
	parser = argparse.ArgumentParser()
	parser.add_argument('path', nargs='?', default = os.getcwd())
	return parser


parser = createParser()
args = parser.parse_args(sys.argv[1:])



print('PATH:  '+args.path)
print('----------------------------------------------------------------------')

bar = IncrementalBar('Файлы ' ,max = len(list(os.walk(args.path))))


for dirpath, dirnames, filenames in os.walk(args.path):
	dirpath+='\\'
	bar.next()
	for i in filenames:
		
		if re.findall('.fb2$',i):
			try:

				# Определение кодировки файла
				charset_detector = UniversalDetector()
				with open(dirpath+i, 'rb') as fh:
				    for line in fh:
				        charset_detector.feed(line)
				        if charset_detector.done:
				            break
				    charset_detector.close()
				
				file = open(dirpath+i, 'rt', encoding=charset_detector.result['encoding'])
				cont = file.read(1000)
				bookTitle =  re.findall('<book-title>[-—а-яА-Я0-9a-zA-Z.,?!:;_|/*<>\\\' ]+</book-title>', cont)[0].replace('<book-title>', '' ).replace('</book-title>', '')
				firstName = re.findall('<first-name>[-—а-яА-Я0-9a-zA-Z.,?!:;_|/*<>\\\' ]+</first-name>', cont)[0].replace('<first-name>', '' ).replace('</first-name>', '')
				lastName = re.findall('<last-name>[-—а-яА-Я0-9a-zA-Z.,?!:;_|/*<>\\\' ]+</last-name>', cont)[0].replace('<last-name>', '' ).replace('</last-name>', '')  

				newName = bookTitle +  ". " + firstName + " "+ lastName + '.fb2'
				newName = re.sub('[<?>:"\\|/*]', '', newName)
				file.close()

				if i!=newName: 
					os.rename(dirpath+i, dirpath + newName )					
					print(i+Fore.GREEN+' --> '+Fore.WHITE+newName)
			except UnicodeDecodeError:
				print(i+Fore.RED+' --> '+ '[ERROR] Файл не переименован. Неорректное содержимое')
			except IndexError:
				print(i+Fore.RED+' --> '+ '[ERROR] Файл не переименован. Отсутствуют необходимые данные')


		if re.findall('.epub$', i):
			try:	
				metadata = epub_meta.get_epub_metadata(dirpath+i)
				newName = metadata.title + '. '+', '.join(metadata.authors)+'.epub'

				if i != newName:
					os.rename(dirpath+i, dirpath+newName)
					print(i+Fore.GREEN+' --> '+Fore.WHITE+newName)
			except KeyError:
				print(i+Fore.RED+' --> '+ '[ERROR] Файл не переименован. Неорректное содержимое')
bar.finish()
			

	