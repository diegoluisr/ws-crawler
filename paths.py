from pathlib import Path
from bs4 import BeautifulSoup
import os

def get_all_folders(path):
    return [str(p) for p in Path(path).rglob("*") if p.is_dir()]


def remove404(filename):
  try:
    with open(filename, 'r', encoding='utf-8') as file:
      if 'Page not found - 404' in file.read():
        file.close()
        os.remove(filename)
        return True
      else:
        return False
  except FileNotFoundError:
    print(f"File {filename} not found")
  except Exception as e:
    print(f"An error occurred: {str(e)}")
  return True

def clearFile(filename):
  try:
    # Read the file
    with open(filename, 'r', encoding='utf-8') as file:
      # Parse the HTML
      soup = BeautifulSoup(file, 'html.parser')

      # Find all div elements with role="alert"
      alert_divs = soup.find_all('div', attrs={'role': 'alert'})

      # Remove each alert div
      for div in alert_divs:
        div.decompose()

      # Write the modified content back to the file
      with open(filename, 'w', encoding='utf-8') as file:
        file.write(str(soup))

  except FileNotFoundError:
    print(f"File {filename} not found")
  except Exception as e:
    print(f"An error occurred: {str(e)}")


# Example usage
folders = get_all_folders("./data/help")

with open('paths.txt', 'w') as file:
  for folder in folders:
    # if not remove404(folder + '/index.html'):
    #   file.write(folder + '\n')
    clearFile(folder + '/index.html')
    file.write(folder + '\n')
