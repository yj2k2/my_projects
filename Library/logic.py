import PyPDF2

class Pair:
	def __init__(self):
		self.left_page = ""
		self.right_page = ""


def page_extract(page_num, reader) :
	return reader.pages[page_num].extract_text()



def read_book(path) :
	file = open(path, 'rb')
	reader = PyPDF2.PdfReader(file)
	num_pages = len(reader.pages)
	pair = Pair()

	for i in range(0, num_pages, 2) :
		pair.left_page = page_extract(i, reader)
		pair.right_page = page_extract(i+1, reader)

		return pair