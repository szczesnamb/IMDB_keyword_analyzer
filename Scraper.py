from bs4 import BeautifulSoup
import requests

imdb_start_page = 'http://www.imdb.com'
storyline_directory = "/movies_txt_storylines"
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


def get_movies_for_genre(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    movie_links = [a.attrs.get('href') for a in soup.select('div.lister-item h3.lister-item-header a')]
    return movie_links[:movie_count_limit]


def clean_movie_link(link):
    return link.replace("?ref_=adv_li_tt", "")


def get_movie_storyline(link):
    response = requests.get(imdb_start_page + clean_movie_link(link) + "plotsummary")
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.select_one("li[id*=synopsis]").get_text()


print(get_movies_for_genre(romance_link))
print(get_movie_storyline(get_movies_for_genre(fantasy_link)[1]))

