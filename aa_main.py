import requests
from bs4 import BeautifulSoup
import os
import re

# URL of the website
url = "https://www.newindianexpress.com/nation/2024/Mar/28/to-browbeat-and-bully-others-is-vintage-congress-culture-pm-modi-slams-party-for-lawyers-letter-to-cji"
# "https://www.marrowmatters.com/Aplastic-Anemia.html"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract text within <h1>, <h2>, <h3>, and <p> tags
    h1_texts = [h1.text.strip() for h1 in soup.find_all('h1')]
    h2_and_p_texts = []
    h3_and_p_texts = []

    # Iterate through each <h2> tag
    for h2 in soup.find_all('h2'):
        h2_text = h2.text.strip()
        p_texts = []

        # Find all <p> tags following the current <h2> tag
        next_sibling = h2.find_next_sibling()
        while next_sibling and (next_sibling.name == 'p' or next_sibling.name == 'h3'):
            if next_sibling.name == 'p':
                p_texts.append(next_sibling.text.strip())
            elif next_sibling.name == 'h3':
                h3_text = next_sibling.text.strip()
                h3_p_texts = []

                # Find all <p> tags following the current <h3> tag
                h3_next_sibling = next_sibling.find_next_sibling()
                while h3_next_sibling and h3_next_sibling.name == 'p':
                    h3_p_texts.append(h3_next_sibling.text.strip())
                    h3_next_sibling = h3_next_sibling.find_next_sibling()

                h3_and_p_texts.append((h3_text, h3_p_texts))

            next_sibling = next_sibling.find_next_sibling()

        h2_and_p_texts.append((h2_text, p_texts))

    # Determine the filename based on the first <h1> content
    filename = h1_texts[0] if h1_texts else "extracted_content"

    # Replace invalid characters in the filename
    filename = re.sub(r'[\\/:*?"<>|]', '_', filename)

    # Create the 'data_extracted' directory if it doesn't exist
    output_directory = "data_extracted"
    os.makedirs(output_directory, exist_ok=True)

    # Save the extracted content as a Markdown file
    output_path = os.path.join(output_directory, f"{filename}.md")
    with open(output_path, "w", encoding="utf-8") as file:
        file.write("# " + "\n# ".join(h1_texts) + "\n\n")

        for h2_text, p_texts in h2_and_p_texts:
            file.write(f"## {h2_text}\n")
            file.write("\n".join(f"{text}\n" for text in p_texts))

        for h3_text, h3_p_texts in h3_and_p_texts:
            file.write(f"### {h3_text}\n")
            file.write("\n".join(f"{text}\n" for text in h3_p_texts))

    print(f"Extraction and saving completed successfully. File saved as {filename}.md in {output_directory}")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
