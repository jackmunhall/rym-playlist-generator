import requests
from bs4 import BeautifulSoup
import json
from swiftshadow.classes import Proxy
from requests_ip_rotator import ApiGateway
import cloudscraper

def scrape_rym_top_songs(year="all-time", genre=None, artist=None):
    # Base URL for the chart
    base_url = f"https://rateyourmusic.com/charts/top/song/{year}"
    
    # Append artist filter to the URL if provided
    if artist:
        artist_filter = f"a:{artist.replace(' ', '%2d')}"
        url = f"{base_url}/{artist_filter}"
    else:
        url = base_url

    # Append genre filter to the URL if provided
    if genre:
        genre_filter = f"g:{genre.replace(' ', '%2d')}"
        url = f"{url}/{genre_filter}"

    cookie_value, user_agent = cloudscraper.get_cookie_string(url)

    headers = {
        'User-Agent': user_agent,
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://rateyourmusic.com/',
    }

    # cookies = {
    #     '__cf_bm': 'Q6LXgq.QCCFimMmg6Q0x_SxrQy0v16bvqcsx3ftnhWo-1725987228-1.0.1.1-hoeyV6gjrylRVibSOyClVIXOBs8IF50mOorGKN4J3Ym4Ngp4hwQEp6rZPXgEU8kEACx.Vecse5F2oMKQurAG9A',
    #     'sec_bs': 'f1cee8a5e817ac9088475088acb48538',
    #     'sec_ts': '1725987231',
    #     'sec_id': '4c063d18056514cfce590deee18c4277',
    #     '_gid': 'GA1.2.1349874962.1725987232',
    #     '_gat_gtag_UA_59057_1': '1',
    #     '_pubcid': '75f41ae1-b15c-414c-8910-1f22c51d20df',
    #     '_pubcid_cst': 'zix7LPQsHA%3D%3D',
    #     '_lr_retry_request': 'true',
    #     '_lr_env_src_ats': 'false',
    #     'pbjs-unifiedid': '%7B%22TDID%22%3A%22c1971c7c-0998-4b48-95f8-bd0ac2b7cef7%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222024-09-10T16%3A53%3A53%22%7D',
    #     'pbjs-unifiedid_cst': 'zix7LPQsHA%3D%3D',
    #     'cf_clearance': 'vbYgFzX3lFlzmymQ6fl5WSSwOZ_00gYp8yaBnAnBDng-1725987233-1.2.1.1-QTDRzHgAuRupzLiMtUA.ogLsEwWA8ZMij9Z7JSnPCW6uaVDLFYl0jbMPw3snpC0lDjWe.aeA8w3.sqkY4aY8ybQEX8BquCZsCi9If8zAfdqgk5z2s.KvsZ1L.d6JUyqQLPXDzcEi7hfNPcOBsbHnDg2kuYdJgph_1QDyPVHQFzcrW9BhDjjQY3izDwacGyUrMHH6zU5JuDl6Og3zg0MbiJzeY9VjvGJ2s_8SuUodtoSLQV5R.O91jfsLRcLXkXcfQNi9N9VSZ.jeWS9oNzrVv45Hzf4dIo3zJ0q0u3Zlek13FG5hN_Gy2a62Cpfoqv_kZZn93DdexpidWLtjnPyumXAexqCDZQ5aCk5m_pExvHaXCTMAzwSBVV0mFDtIcd57ABnYiHyol7aGbhp6Iz9yAa2a9mRnAhVFSxFwnL57l66_8f0i0wqnT7e5UlKzN_yV',
    #     '_ga': 'GA1.1.581297191.1725987232',
    #     '_ga_CPSL518SBG': 'GS1.1.1725987232.1.1.1725987233.59.0.0',
    # }

    # headers = {
    #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    #     'accept-language': 'en-US,en;q=0.9',
    #     'cache-control': 'max-age=0',
    #     # 'cookie': '__cf_bm=Q6LXgq.QCCFimMmg6Q0x_SxrQy0v16bvqcsx3ftnhWo-1725987228-1.0.1.1-hoeyV6gjrylRVibSOyClVIXOBs8IF50mOorGKN4J3Ym4Ngp4hwQEp6rZPXgEU8kEACx.Vecse5F2oMKQurAG9A; sec_bs=f1cee8a5e817ac9088475088acb48538; sec_ts=1725987231; sec_id=4c063d18056514cfce590deee18c4277; _gid=GA1.2.1349874962.1725987232; _gat_gtag_UA_59057_1=1; _pubcid=75f41ae1-b15c-414c-8910-1f22c51d20df; _pubcid_cst=zix7LPQsHA%3D%3D; _lr_retry_request=true; _lr_env_src_ats=false; pbjs-unifiedid=%7B%22TDID%22%3A%22c1971c7c-0998-4b48-95f8-bd0ac2b7cef7%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222024-09-10T16%3A53%3A53%22%7D; pbjs-unifiedid_cst=zix7LPQsHA%3D%3D; cf_clearance=vbYgFzX3lFlzmymQ6fl5WSSwOZ_00gYp8yaBnAnBDng-1725987233-1.2.1.1-QTDRzHgAuRupzLiMtUA.ogLsEwWA8ZMij9Z7JSnPCW6uaVDLFYl0jbMPw3snpC0lDjWe.aeA8w3.sqkY4aY8ybQEX8BquCZsCi9If8zAfdqgk5z2s.KvsZ1L.d6JUyqQLPXDzcEi7hfNPcOBsbHnDg2kuYdJgph_1QDyPVHQFzcrW9BhDjjQY3izDwacGyUrMHH6zU5JuDl6Og3zg0MbiJzeY9VjvGJ2s_8SuUodtoSLQV5R.O91jfsLRcLXkXcfQNi9N9VSZ.jeWS9oNzrVv45Hzf4dIo3zJ0q0u3Zlek13FG5hN_Gy2a62Cpfoqv_kZZn93DdexpidWLtjnPyumXAexqCDZQ5aCk5m_pExvHaXCTMAzwSBVV0mFDtIcd57ABnYiHyol7aGbhp6Iz9yAa2a9mRnAhVFSxFwnL57l66_8f0i0wqnT7e5UlKzN_yV; _ga=GA1.1.581297191.1725987232; _ga_CPSL518SBG=GS1.1.1725987232.1.1.1725987233.59.0.0',
    #     'priority': 'u=0, i',
    #     'referer': 'https://rateyourmusic.com/artist/radiohead',
    #     'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    #     'sec-ch-ua-arch': '"x86"',
    #     'sec-ch-ua-bitness': '"64"',
    #     'sec-ch-ua-full-version': '"128.0.6613.115"',
    #     'sec-ch-ua-full-version-list': '"Chromium";v="128.0.6613.115", "Not;A=Brand";v="24.0.0.0", "Google Chrome";v="128.0.6613.115"',
    #     'sec-ch-ua-mobile': '?0',
    #     'sec-ch-ua-model': '""',
    #     'sec-ch-ua-platform': '"Windows"',
    #     'sec-ch-ua-platform-version': '"10.0.0"',
    #     'sec-fetch-dest': 'document',
    #     'sec-fetch-mode': 'navigate',
    #     'sec-fetch-site': 'same-origin',
    #     'sec-fetch-user': '?1',
    #     'upgrade-insecure-requests': '1',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    # }

    gateway = ApiGateway("https://rateyourmusic.com")
    gateway.start()

    # scraper = cloudscraper.create_scraper()
    # scraper.mount('https://rateyourmusic.com', gateway)

    session = requests.Session()
    session.mount('https://rateyourmusic.com', gateway)

    session.headers.update(headers)
    session.headers.update({'Cookie': cookie_value})

    # response = session.get(url, headers=headers, cookies=cookies)
    response = session.get(url)

    # response = requests.get(url, headers=headers, cookies=cookies, proxies=proxies)

    if response.status_code != 200:
        gateway.shutdown()
        return {"error": "Failed to fetch data", "status_code": response.status_code, 'text': response.text}

    gateway.shutdown()
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all containers for songs
    song_containers = soup.find_all('div', class_='media_link_container')

    songs = []

    # Iterate through each song container
    for container in song_containers:
        # Check if the 'data-links' attribute exists
        data_links = container.get('data-links')
        
        if data_links:
            # Convert the data-links string into a dictionary
            links_json = json.loads(data_links)
            
            # Check if there is a Spotify link
            if 'spotify' in links_json:
                # Get the Spotify track ID
                track_id = list(links_json['spotify'].keys())[0]
                
                # Extract additional info like artists, album, etc.
                artists = container.get('data-artists')
                song = container.get('data-albums')
                
                # Add song details to the list
                songs.append({
                    "artists": artists,
                    "song": song,
                    "track_id": track_id
                })

    return songs

print(scrape_rym_top_songs(year="2022", genre="Rock"))