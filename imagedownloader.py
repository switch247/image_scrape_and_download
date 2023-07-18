import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import csv
logs =[]
def scrape_images(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logs.append(f"Error accessing URL: {url} \n Error:{e}")
        print(f"Error accessing URL: {url}")
        print(e)
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Create a directory to store the images
    directory = urllib.parse.urlparse(url).netloc.replace(".", "_")
    os.makedirs(directory, exist_ok=True)
    
    # Find all image tags and download the images
    image_tags = soup.find_all('img')
    for img in image_tags:
        img_url = img['src']
        try:
            if img_url.startswith('http'):
                img_response = requests.get(img_url)
            else:
                img_response = requests.get(urllib.parse.urljoin(url, img_url))
            img_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logs.append(f"Error downloading image: {img_url} \n Error:{e}")
            print(f"Error downloading image: {img_url}")
            print(e)
            continue
        
        img_name = img_url.split('/')[-1]
        img_path = os.path.join(directory, img_name)
        print(img_name,img_path)
        try:
            with open(img_path, 'wb') as f:
                f.write(img_response.content)
            print(f"Downloaded image: {img_path}")
            logs.append(f"Downloaded image: {img_path}")
        except FileNotFoundError as e:
            logs.append(f"Error saving image: {img_path} \n Error:{e}")
            print(f"Error saving image: {img_path}")
            print(e)
            continue
    with open("logs.txt", "a") as file:
        log ="\n".join(logs)
        file.write("{" +f'{log}' +"}")

urls = []

# Function to read URLs from a CSV file
def read_urls_from_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            urls.append(row[0])

# Function to read URLs from a TXT file
def read_urls_from_txt(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            urls.append(line.strip())

# Example usage

def read_from_file(file_path = 'urls.csv'):
    try:
        if file_path.endswith('.csv'):
            read_urls_from_csv(file_path)
        elif file_path.endswith('.txt'):
            read_urls_from_txt(file_path)
    except FileNotFoundError as e:
                print(e)
    print (urls)
# Example usage
read_from_file()
# read_from_file(filepath)
 # Replace with the path to your CSV or TXT file
for url in urls:
    scrape_images(url)



