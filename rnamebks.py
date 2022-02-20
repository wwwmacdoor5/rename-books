import os, sys, re, argparse
from colorama import init, Fore, Back, Style
import epub_meta
from chardet.universaldetector import UniversalDetector




'''
	TODO
	Добавить поддержку форматов pdf, epub, djvu, mobi, fb3 ... 
	Два реплейса заменить на один шаблон
	Добавить рекурсивный проход по дереву дирректорий (поумолчанию скрипт работает только в данной папке)
	Добавить конфиг 
	Проверить запускается ли с аргументом екзешник
	Подчинить прогрессбар
	Проверить програесс бар на большом количестве файлов на выход за границы массива
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



print('PATH:  '+args.path+'\n'+'-'*80)





for dirpath, dirnames, filenames in os.walk(args.path):
	dirpath+='\\'
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

				bookTitle = re.search('(?<=(book-title>))(.)+?(?=(</book-title>))', cont).group(0)
				bookTitle = bookTitle if bookTitle else re.search('(?<=(<book-name>))(.)+?(?=(</book-name>))', cont).group(0)
				firstName =  re.search('(?<=(<first-name>))(.)+?(?=(</first-name>))', cont).group(0)
				lastName =  re.search('(?<=(<last-name>))(.)+?(?=(</last-name>))', cont).group(0)
 			  

				newName = bookTitle +  ". " +firstName + ' ' + lastName + '.fb2'
				newName = re.sub('[<?>:"\\|/*]', '', newName)
				file.close()

				if i!=newName: 
					os.rename(dirpath+i, dirpath + newName )					
					print(i+Fore.GREEN+' --> '+Fore.WHITE+newName)
			except UnicodeDecodeError:
				print(i+Fore.RED+' --> '+ '[ERROR] Файл не переименован. Неорректное содержимое')
			except AttributeError:
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


	