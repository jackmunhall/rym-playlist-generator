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
        '_gid': 'GA1.2.1733143105.1725884551',
        '__cf_bm': 'EEZ_3DPimV6z5mHTVklc_Q51PH3d946GqR8bOJNwDjU-1725976379-1.0.1.1-TV2EregiOz1HCJSnHyKFm9mktI3eX2xKZncVyj0ZC7cygi1YVsPEgGK5gYwl0iQYRtlMPMeDJl7YnDKno4K.LA',
        'sec_bs': '0149f95ec9c40fe1453128a2f7d88b5e',
        'sec_ts': '1725976385',
        'sec_id': '4592ce26dbc180fbcb4e2592e73b2ada',
        '_lr_retry_request': 'true',
        'cf_clearance': '2IgQEfS.W139rXyl0Ay5dlX7fdhx2nWcwvnR_Pe_UJw-1725976386-1.2.1.1-ElZ7AphHPs_fMtgVC3_9LvyHvwqwVxARMLHaq1iP52zk8s1FkTVu5OAi5NSsOm96gGsCq5EahZF8QNpcup3CjSit3thqHyYPNjjCoTUbQtrZJFDiHpDdXkCbZUC8odQEdp.tCfNwfMt4OUxp.emVrQIWF4KqQG.xyWiNuoB3qGEGbrfGA9aBA_wynxLt0.bWLXKdSeKZ_cJmpGmKieL4O9dmM.EMRfHEXnjBl8MKqJW2CS8Uw7ey7.BJ0NwlT1yZBHKFIS2WWFaKJDFH8aJkQ3rMDZgLNDh1g0q57EmA4LfOxFZHEzHJrdGD77XQk7jbebkXM3ntZuqnw839bmJ6AN9XqNOMmiakNI.adZpJxMVfHkUK_rR1wgzRPuh5fuSCoZoBJGf0Ua0QhIAnpmcH6uFv5EQi4ioS..drufIfSD8vzQ0DLUzfuDmLLSVhdS6_',
        '_gat_gtag_UA_59057_1': '1',
        '_ga': 'GA1.1.301988536.1724942349',
        '_ga_CPSL518SBG': 'GS1.1.1725976385.9.1.1725977015.54.0.0',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        # 'cookie': '_pubcid=fe20b9ba-099c-4b83-9dbe-8c42a53e42fe; _pubcid_cst=zix7LPQsHA%3D%3D; _lr_env_src_ats=false; pbjs-unifiedid=%7B%22TDID%22%3A%221a731514-10e5-45b2-af74-04dc141c0f5e%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222024-07-29T14%3A39%3A09%22%7D; pbjs-unifiedid_cst=zix7LPQsHA%3D%3D; _gid=GA1.2.1733143105.1725884551; __cf_bm=EEZ_3DPimV6z5mHTVklc_Q51PH3d946GqR8bOJNwDjU-1725976379-1.0.1.1-TV2EregiOz1HCJSnHyKFm9mktI3eX2xKZncVyj0ZC7cygi1YVsPEgGK5gYwl0iQYRtlMPMeDJl7YnDKno4K.LA; sec_bs=0149f95ec9c40fe1453128a2f7d88b5e; sec_ts=1725976385; sec_id=4592ce26dbc180fbcb4e2592e73b2ada; _lr_retry_request=true; cf_clearance=2IgQEfS.W139rXyl0Ay5dlX7fdhx2nWcwvnR_Pe_UJw-1725976386-1.2.1.1-ElZ7AphHPs_fMtgVC3_9LvyHvwqwVxARMLHaq1iP52zk8s1FkTVu5OAi5NSsOm96gGsCq5EahZF8QNpcup3CjSit3thqHyYPNjjCoTUbQtrZJFDiHpDdXkCbZUC8odQEdp.tCfNwfMt4OUxp.emVrQIWF4KqQG.xyWiNuoB3qGEGbrfGA9aBA_wynxLt0.bWLXKdSeKZ_cJmpGmKieL4O9dmM.EMRfHEXnjBl8MKqJW2CS8Uw7ey7.BJ0NwlT1yZBHKFIS2WWFaKJDFH8aJkQ3rMDZgLNDh1g0q57EmA4LfOxFZHEzHJrdGD77XQk7jbebkXM3ntZuqnw839bmJ6AN9XqNOMmiakNI.adZpJxMVfHkUK_rR1wgzRPuh5fuSCoZoBJGf0Ua0QhIAnpmcH6uFv5EQi4ioS..drufIfSD8vzQ0DLUzfuDmLLSVhdS6_; username=jman777jman; _gat_gtag_UA_59057_1=1; _ga=GA1.1.301988536.1724942349; _ga_CPSL518SBG=GS1.1.1725976385.9.1.1725977015.54.0.0',
        'priority': 'u=0, i',
        'referer': 'https://rateyourmusic.com/artist/radiohead',
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
        return {"error": "Failed to fetch data", "status_code": response.status_code}

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

# Test the function
songs = scrape_rym_top_songs(year="all-time", artist="red house painters")
print(songs)