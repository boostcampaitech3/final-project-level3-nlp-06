import requests
from bs4 import BeautifulSoup
import time





### Page extraction
def page_extraction(target_url):
    page = requests.get(target_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    body_v = soup.find(class_='board_view')

    title = body_v.find(class_='title1')
    title = title.text
    paras = body_v.find_all('p')
    paragraph = paras[1].text

    print(title)
    f = open(f'./extractions/{title}.txt', 'w')
    f.write(paragraph)
    f.close()




if __name__ == '__main__': 
    page_list = []

    for i in range(1, 21):
        urls = f'http://18children.president.pa.go.kr/our_space/fairy_tales.php?srh%5Bcategory%5D=07&srh%5Bpage%5D={i}'
        pages = requests.get(urls)
        soup = BeautifulSoup(pages.content, 'html.parser')

        board_list = soup.find('div', class_='board_list')
        hrefs = board_list.find_all('a')

        for h in hrefs:
            #print(str(h))
            #print(str(h).find('Detail'))
            #print(str(h)[35:39]) # 35 36 37 38
            num = str(h)[35:39].strip(',')
            page_list.append(num)
        
    page_list = set(page_list)
    print(page_list, len(page_list))


    for p in page_list:
        time.sleep(3)
        target_url = f'http://18children.president.pa.go.kr/our_space/fairy_tales.php?srh%5Bcategory%5D=07&srh%5Bpage%5D=1&srh%5Bview_mode%5D=detail&srh%5Bseq%5D={p}'
        page_extraction(target_url)