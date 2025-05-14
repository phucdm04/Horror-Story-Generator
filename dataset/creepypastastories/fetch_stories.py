from bs4 import BeautifulSoup
import re   
import requests
from datetime import date, datetime
import pandas as pd

def fetch_one_page(url: str) -> dict:
    def get_rating_and_votes(text: str) -> tuple:
        match = re.search(r'Rating: (\d+\.\d+)/10\. From (\d+) vote[s]?\.', text)
        if match:
            rating = match.group(1)
            votes = match.group(2)
            return float(rating), int(votes)
        else:
            # print("Find nothing!")
            return None, None

    def get_date(text: str) -> str:
        match = re.search(r'Published on (\w+ \d{1,2}, \d{4})', text)

        if match:
            date_str = match.group(1)
            date_obj = datetime.strptime(date_str, '%B %d, %Y')
            formatted_date = date_obj.strftime('%m/%d/%Y')
            return formatted_date
        else:
            # print("Find nothing!")
            return None

    response = requests.get(url)
    page_soup = BeautifulSoup(response.content, 'html.parser')
    check_post = page_soup.find('div', class_='pt-cv-no-post')
    if check_post:
        # print("No post found")
        return 

    ################################################################################
    titles = []; contents = []; ratings = []; votes = []; authors = []; dates = []
    stories = page_soup.find_all('h4', class_='pt-cv-title')[:12]
    for story in stories:
        title = story.text
        try: 
            sub_url = story.find('a')['href']
            sub_response = requests.get(sub_url)
            sub_page_soup = BeautifulSoup(sub_response.content, 'html.parser')

            # content fetching
            post_text_inner = sub_page_soup.find('div', class_='post_text_inner')
            paragraphs = post_text_inner.find_all('p')[3:-2] # 3 to -2 is the range of content
            content = '\n'.join([paragraph.text for paragraph in paragraphs])

            rating_div = sub_page_soup.find('div', class_='gdrts-rating-text')
            rating, vote = get_rating_and_votes(rating_div.text) 

            # information fetching
            information_block = sub_page_soup.find('div', class_='code-block code-block-1')
            author = information_block.find_all('a')[0].text
            date = get_date(information_block.find('em').text)

            # print(title, rating, vote, author, date)   
            titles.append(title); contents.append(content); ratings.append(rating); votes.append(vote); authors.append(author); dates.append(date)
        except Exception as e:
            print(f"Error: {e} at {title}", sep=' ')


    one_page_data = {
        'titles': titles, 'contents': contents, 'ratings': ratings, 'votes': votes, 'authors': authors, 'dates': dates
    }

    return one_page_data




def main():
    final_data = {}
    is_able_to_fetch = True
    current_page = 1
    while is_able_to_fetch and current_page <= 18:
        print(f"Fetching data from page {current_page}.", end=' ')
        url = f"https://www.creepypastastories.com/?_orderby=date%2Cdesc&_page={current_page}"
        data = fetch_one_page(url)    
        if data:
            for key in data:
                if key in final_data:
                    final_data[key].extend(data[key])
                else:
                    final_data[key] = data[key]
            print("Done!")
            current_page += 1
        else:
            is_able_to_fetch = False
            print("No post found!")

    # Convert the final data to a DataFrame
    day = str(date.today()).replace('-', '_')
    df = pd.DataFrame(final_data)
    df.head()

    # remove duplicate
    df = df.drop_duplicates(subset=['titles'])

    # save to csv
    df.to_json(f'./dataset/creepypastastories/dataset_{day}.json', force_ascii=False)

if __name__ == "__main__":
    main()
