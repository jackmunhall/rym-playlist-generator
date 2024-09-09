import requests
from bs4 import BeautifulSoup
import json

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

    print(url)

    cookies = {
        '_pubcid': 'fe20b9ba-099c-4b83-9dbe-8c42a53e42fe',
        '_pubcid_cst': 'zix7LPQsHA%3D%3D',
        '_lr_env_src_ats': 'false',
        'pbjs-unifiedid': '%7B%22TDID%22%3A%221a731514-10e5-45b2-af74-04dc141c0f5e%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222024-07-29T14%3A39%3A09%22%7D',
        'pbjs-unifiedid_cst': 'zix7LPQsHA%3D%3D',
        'sec_bs': '8541ef5391d62269c2509e19e33fc47c',
        'sec_ts': '1725884550',
        'sec_id': 'c301bfd82b35df12af98cf8d92e313f5',
        '__cf_bm': 'Lb55_wtna0lIRNjtx0gt40mPUdUxCK.5BEUg.VL_OlA-1725884550-1.0.1.1-5cn0nqvUqdgc2c5bHIBmfnfFLYYZ969_BiADYNy_iLPftUZWDdjAQUoyORNdxyFS2IgHMmWRkKY7GLw7RSY7Tg',
        '_gid': 'GA1.2.1733143105.1725884551',
        '_lr_retry_request': 'true',
        'cf_clearance': 'gzasu7QajlXJSDytWNd53V3ZRYJAkQU5arfYUpp2YUM-1725884552-1.2.1.1-.WkO4fmjWIBhpj_O2W9lut5TpHe.fJ_jbjbp8iV2gZmpn1oSEgtm0ccc7mzISYbyHgdCIezAhZ4ggf8vkqWbwI0DrSEmD48KGnQX7nbhe.0ZBuw0_2G9Fkb_erEtorLTGhh1_m7dXGcmR_vTPCGkElRYaBvx.2htkzoLgIxYcW5BUT_k2FFOYZMuNHTQ0loNv8.mfnb9RJttjBZWPMmJyGg4mSbQzuOdB69n_ThrZiezfHmyVpForX2h0aA8ZNZ.MRWwmDdKSXGWeY6GinjfILqnoMqFUfbWLYIllrXYg8Xwvbj3HYm8.OuGSdya4Ag.vqwursZD2CiGVpuKjJvC9ee6BkVfRiWlIpd5j4bG4IyMlF3A2wDH0mr9Val1C9_19954oIft2Sb4PUzTtub6cFCj9KQe1E1JyT_GIQAiKrqvekmNRjNYr15fowid1ZW9',
        '_ga': 'GA1.1.301988536.1724942349',
        '_ga_CPSL518SBG': 'GS1.1.1725884550.6.1.1725884583.27.0.0',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        # 'cookie': '_pubcid=fe20b9ba-099c-4b83-9dbe-8c42a53e42fe; _pubcid_cst=zix7LPQsHA%3D%3D; _lr_env_src_ats=false; pbjs-unifiedid=%7B%22TDID%22%3A%221a731514-10e5-45b2-af74-04dc141c0f5e%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222024-07-29T14%3A39%3A09%22%7D; pbjs-unifiedid_cst=zix7LPQsHA%3D%3D; sec_bs=8541ef5391d62269c2509e19e33fc47c; sec_ts=1725884550; sec_id=c301bfd82b35df12af98cf8d92e313f5; __cf_bm=Lb55_wtna0lIRNjtx0gt40mPUdUxCK.5BEUg.VL_OlA-1725884550-1.0.1.1-5cn0nqvUqdgc2c5bHIBmfnfFLYYZ969_BiADYNy_iLPftUZWDdjAQUoyORNdxyFS2IgHMmWRkKY7GLw7RSY7Tg; _gid=GA1.2.1733143105.1725884551; _lr_retry_request=true; cf_clearance=gzasu7QajlXJSDytWNd53V3ZRYJAkQU5arfYUpp2YUM-1725884552-1.2.1.1-.WkO4fmjWIBhpj_O2W9lut5TpHe.fJ_jbjbp8iV2gZmpn1oSEgtm0ccc7mzISYbyHgdCIezAhZ4ggf8vkqWbwI0DrSEmD48KGnQX7nbhe.0ZBuw0_2G9Fkb_erEtorLTGhh1_m7dXGcmR_vTPCGkElRYaBvx.2htkzoLgIxYcW5BUT_k2FFOYZMuNHTQ0loNv8.mfnb9RJttjBZWPMmJyGg4mSbQzuOdB69n_ThrZiezfHmyVpForX2h0aA8ZNZ.MRWwmDdKSXGWeY6GinjfILqnoMqFUfbWLYIllrXYg8Xwvbj3HYm8.OuGSdya4Ag.vqwursZD2CiGVpuKjJvC9ee6BkVfRiWlIpd5j4bG4IyMlF3A2wDH0mr9Val1C9_19954oIft2Sb4PUzTtub6cFCj9KQe1E1JyT_GIQAiKrqvekmNRjNYr15fowid1ZW9; _ga=GA1.1.301988536.1724942349; _ga_CPSL518SBG=GS1.1.1725884550.6.1.1725884583.27.0.0',
        'priority': 'u=0, i',
        'referer': 'https://rateyourmusic.com/charts/top/song/all-time/a:red%2dhouse%2dpainters/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"128.0.6613.115"',
        'sec-ch-ua-full-version-list': '"Chromium";v="128.0.6613.115", "Not;A=Brand";v="24.0.0.0", "Google Chrome";v="128.0.6613.115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }

    response = requests.get(url, cookies=cookies, headers=headers)

    if response.status_code != 200:
        return {"error": "Failed to retrieve data from RYM"}

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