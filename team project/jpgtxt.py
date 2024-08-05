from pdf2image import convert_from_path
import pytesseract
from PIL import Image

# Tesseract 경로 설정
pytesseract.pytesseract.tesseract_cmd = r'C:/Users/dev/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'

# PDF 파일 경로 설정
pdf_path = 'C:/Users/dev/Documents/GitHub/kakaobootcamp/team project/data/notion7.pdf'
poppler_path = r'C:/Users/dev/Documents/Python Scripts/Release-24.07.0-0/poppler-24.07.0/Library/bin'

# PDF 파일을 이미지로 변환
pages = convert_from_path(pdf_path, 300, poppler_path=poppler_path)

# 각 페이지에서 텍스트 추출
extracted_text = ""
for page in pages:
    text = pytesseract.image_to_string(page, lang='kor')
    extracted_text += text + "\n"

# 추출된 텍스트 출력 또는 파일로 저장
print(extracted_text)
with open('extracted_text.txt', 'w', encoding='utf-8') as f:
    f.write(extracted_text)
