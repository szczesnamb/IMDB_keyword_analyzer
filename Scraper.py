import io

import re
from bs4 import BeautifulSoup
import requests

imdb_start_page = 'http://www.imdb.com'
storyline_directory = "movies_txt_storylines/"
movie_count_limit = 25
comedy_link = "http://www.imdb.com/search/title?genres=comedy&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_" \
              "p=3454807202&pf_rd_r=0T1FF6HQPTKMMRRV89T5&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=genre&sort=num_votes," \
              "desc&ref_=ft_gnr_pr1_i_1"
romance_link = "http://www.imdb.com/search/title?genres=romance&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_r" \
               "d_p=3454807222&pf_rd_r=0MVVH2XNR401HJZ01YJ1&pf_rd_s=center-2&pf_rd_t=15051&pf_rd_i=genre&sort=num_vot" \
               "es,desc&ref_=ft_gnr_pr2_i_1"
action_link = "http://www.imdb.com/search/title?genres=action&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_" \
              "p=3454807222&pf_rd_r=0MVVH2XNR401HJZ01YJ1&pf_rd_s=center-2&pf_rd_t=15051&pf_rd_i=genre&sort=num_votes," \
              "desc&ref_=ft_gnr_pr2_i_2"
fantasy_link = "http://www.imdb.com/search/title?genres=fantasy&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_" \
               "rd_p=3454807302&pf_rd_r=0MVVH2XNR401HJZ01YJ1&pf_rd_s=center-4&pf_rd_t=15051&pf_rd_i=genre&sort=num_" \
               "votes,desc&ref_=ft_gnr_pr4_i_3"
html_link_selector = 'div.lister-item h3.lister-item-header a'
link_pollution = "?ref_=adv_li_tt"
html_sypnosis_selector = "li[id*=synopsis]"
html_movie_title_selector = "div.title_wrapper h1"
html_original_title_selector = "div.title_wrapper div.originalTitle"


def get_movies_for_genre(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    movie_links = [a.attrs.get('href') for a in soup.select(html_link_selector)]
    return movie_links[:movie_count_limit]


def clean_movie_link(link):
    return link.replace(link_pollution, "")


def get_movie_storyline(link):
    response = requests.get(link + "plotsummary")
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.select_one(html_sypnosis_selector).get_text()


def get_movie_title(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.select_one(html_original_title_selector).get_text().replace("(original title)", "").replace(":", "")\
        if soup.select_one(html_original_title_selector) is not None \
        else re.sub(r'\([^)]*\)', '', soup.select_one(html_movie_title_selector).get_text())


def generate_movie_link(link):
    return imdb_start_page + clean_movie_link(link)


def save_to_file(text, filename):
    with io.open(filename, "w", encoding="utf-8") as f:
        f.write(text)


def generate_file_name(title, f_name_prefix, number):
    return storyline_directory + title + '_' + f_name_prefix + str(number) + '.txt'


movies = get_movies_for_genre(action_link)
for x in range(0, 25):
    movie_link = generate_movie_link(movies[x])
    title = get_movie_title(movie_link)[:-1].replace("\\.", "")
    filename = generate_file_name(title, 'action', x)
    save_to_file(get_movie_storyline(movie_link), filename)

