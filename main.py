from tqdm import tqdm
import requests
import re

def download_file(url, filename):
	headers = {
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
	}
	response = requests.get(url, headers=headers, stream=True)

	with open(filename, 'wb') as f:
			pbar = tqdm(unit="B", unit_scale=True, unit_divisor=1024, total=int(response.headers['Content-Length']))
			pbar.clear()  #  clear 0% info
			for chunk in response.iter_content(chunk_size=1024):
					if chunk: # filter out keep-alive new chunks
							pbar.update(len(chunk))
							f.write(chunk)
			pbar.close()
	return filename

def main():
	clip_url = input("Enter the Twitch Clip URL: ")
	response = requests.get(f"https://twiclips.com/twitch-download/clip?clip_url={clip_url}")
	response_json = response.json()
	if response_json["data"] == None:
		input("The URL is invalid!")
		exit()
	print(f'Downloading "{response_json["data"]["title"]}" by {response_json["data"]["info"]["clip_author"]}...')
	clip_url = response_json["data"]["info"]["play_url"]
	file_name = f'{response_json["data"]["title"]}.mp4'
	valid_file_name = re.sub(r'\\|\/|:|\*|\?|"|<|>|\|', "_", file_name)
	download_file(response_json["data"]["info"]["play_url"], valid_file_name)
	input("Downloaded complete!")

if __name__ == '__main__':
  main()